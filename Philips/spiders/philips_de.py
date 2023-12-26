from codecs import BufferedIncrementalDecoder
import codecs
from re import L
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from twisted import logger
from ..utils import clean
from ..utils import translate_new

class PhilipSpider(CrawlSpider):
    name = 'Philip_de'
    allowed_domains = ['philips.de']
    start_urls = ['https://www.philips.de']

    rules = (
        Rule(LinkExtractor(restrict_css=['.p-n02v3__mlink--no-childs'])),
        # Rule(LinkExtractor(restrict_css=['.p-cta-link', '.p-view-all']), callback='parse_item'),
        Rule(LinkExtractor(allow='/c-p/'), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        item = {}
        item['Product_url'] = response.url
        item['Product_Name'] = self.parse_product_name(response)
        item['Product_Code'] = self.parse_product_code(response)
        item['Product_Price'] = self.parse_product_price(response)
        item['Primary_Image'] = self.parse_primary_image(response)
        item['Secondary_Image'] = self.parse_secondary_images(response)
        item['Description'] = self.parse_description(response)
        item['Breadcrums'] = self.parse_breadcrums(response)
        item['Web_Series_Links'] = self.parse_web_series_links(response)
        item['Reviews_Count'] = self.parse_reviews_count(response)
        item['Meta_Data'] = self.parse_meta_data(response)
        item['Product_Features'] = self.parse_product_features(response)
        item['Technical_Specifications'] = self.parse_Technical_Specifications(response)
        return item
    def parse_product_code(self, response):
        product_code = response.xpath('//div[@class="p-product-info "]//span[@class="p-product-ctn"]/text()').get()
        return product_code
    def parse_product_price(self, response):
        try:
            product_price = response.xpath('//meta[@name="PS_PRODUCT_PRICE"]/@content').get()
            euro_symbol = "€"
            f_price = euro_symbol +product_price
            return f_price
        except:
            return ""

    def parse_product_name(self, response):
        product_name = translate_new(clean(response.css('.p-sub-title ::text').get()))
        return product_name
    def parse_primary_image(self, response):
        p_image = response.xpath('//ul[@class="p-viewer"]//picture//img/@src').get()
        return p_image
    
    def parse_secondary_images(self, response):
        s_images = response.css(".p-slider-item img::attr(src)").getall()
        return s_images
    
    def parse_description(self, response):
        desc = translate_new(response.xpath("//meta[@name='description']/@content").get())
        return desc
    
    def parse_breadcrums(self, response):
        breadcrums = translate_new(clean(response.css(".p-n04v3-breadcrumb__link-title ::text").getall()))
        return breadcrums
    
    def parse_web_series_links(self, response):
        breadcrum_text = self.parse_breadcrums(response)
        breadcrum_links = response.xpath("//a[@data-track-navid='breadcrumbs']/@href").getall()
        breadcrum_links = breadcrum_links[1:]
        return dict(zip(breadcrum_text, breadcrum_links))
    
    def parse_meta_data(self, response):
        meta_title = translate_new(response.xpath("//title/text()").get())
        meta_description = translate_new(response.xpath("//meta[@property='og:description']/@content").get())
        meta_keywords = translate_new(response.xpath("//meta[@name='keywords']/@content").get())
        keys = ['meta_title','meta_description','meta_keywords']
        values = [meta_title, meta_description, meta_keywords]
        return dict(zip(keys, values))
    
    def parse_reviews_count(self, response):
        rev_count = translate_new(response.css('.p-user-reviews ::text').get())
        return rev_count
    
    def parse_product_features(self, response):
        images = clean(response.css(".p-s12__feature-item img ::attr(src)").getall())
        headings = translate_new(clean(response.css(".p-s12__feature-item h3 ::text").getall()))
        descriptions = translate_new(clean(response.css(".p-s12__feature-item p ::text").getall()))
        return [{"Heading":a,"Image":b,"Description":c} for a,b,c in zip(headings, images, descriptions)]
    
    def parse_Technical_Specifications(self, response):
        main_headings = translate_new(response.css(".p-s08__spec p::text").getall())
        main_data = response.css(".p-s08__spec dl")
        data_list = []
        for j in main_data:
            inner_keys = translate_new(clean(j.css("dt ::text").getall()))
            # values = clean(j.css("span ::text").getall())
            values = j.css("dd")
            new_values = [translate_new(clean(x.css('span ::text').getall())) for x in values]
            data_list.append(dict(zip(inner_keys, new_values)))
        return dict(zip(main_headings,data_list))
    
    def parse_related_products(self, response):
        product_links = response.css(".p-pc05v2__card .p-pc05v2__card-title-link ::attr(href)").getall()
        image_links = response.css(".p-pc05v2__card .p-pc05v2__card-image-link ::attr(href)").getall()
        name = translate_new(response.css(".p-pc05v2__card .p-pc05v2__card-title-link .p-heading-light ::text").getall())
        return [{"Product_name":a,"Image":b,"Link":c} for a,b,c in zip(name, image_links, product_links)]