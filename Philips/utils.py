from googletrans import Translator
import re

def translate_new(text):
        translator = Translator()
        if type(text) == str:
            translation = translator.translate(text, dest='en').text
            return translation
        elif type(text) == list:
            list_var = [translator.translate(var).text for var in text]
            return list_var

def _sanitize(input_val):
    pattern_re = r'\s+'
    repl_re = ' '
    return re.sub(pattern_re, repl_re, input_val, flags=0).strip()

def clean(lst_or_str):
    if not isinstance(lst_or_str, str) and getattr(
        lst_or_str, '__iter__', False
    ):  # if iterable and not a string like
        return [x for x in (_sanitize(y) for y in lst_or_str if y is not None) if x]
    return _sanitize(lst_or_str) if lst_or_str else None