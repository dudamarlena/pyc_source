# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/sogubaby/.virtualenvs/scrapy_middlewares/lib/python3.7/site-packages/scrapy_cabinet/spiders/cabinet_spider.py
# Compiled at: 2019-11-14 03:49:12
# Size of source mod 2**32: 819 bytes
import scrapy
from scrapy_cabinet.utils import load_object

class Spider(scrapy.Spider):
    custom_settings = {'list_key':'', 
     'url_key':'', 
     'title_key':'', 
     'key_map':dict(), 
     'extract_type':'scrapy_cabinet.constants.ExtractType.LIST', 
     'target_cls':''}

    def prepare(self, *args, **kwargs):
        return args[0].text

    def parse(self, response):
        item = dict()
        item['need_extract'] = load_object(self.crawler.settings.get('extract_type'))
        item['target_cls'] = load_object(self.crawler.settings.get('target_cls'))
        item['source_page'] = self.prepare(response)
        yield item