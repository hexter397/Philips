# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter, adapter
import itemadapter
from scrapy.exceptions import DropItem

class PhilipsPipeline:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        if adapter.get("Product_Name") == None or adapter.get("Product_Name") == "":
            raise DropItem(f"Missing Product Name in {item}")
        else:
            return item
