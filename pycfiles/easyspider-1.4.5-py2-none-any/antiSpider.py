# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/zhanghang/Desktop/workspace/molbase/molbase_2017_7_3/release/easyspider/middlewares/antiSpider.py
# Compiled at: 2017-08-24 09:47:41
import logging
from scrapy.exceptions import IgnoreRequest
logger = logging.getLogger(__name__)

class spiderIsAnti(IgnoreRequest):

    def __init__(self, response, *args, **kwargs):
        pass


class antiSpiderMiddleware(object):

    def process_spider_input(self, response, spider):
        if not hasattr(spider, 'is_blocked_spider'):
            return
        if not spider.is_blocked_spider(response):
            return
        if hasattr(spider, 'blocked_call_back'):
            spider.blocked_call_back(response)
        raise spiderIsAnti(response)

    def process_spider_exception(self, response, exception, spider):
        if isinstance(exception, spiderIsAnti):
            logger.info('Ignoring response %(response)r: Spider is blocked or not allowed', {'response': response}, extra={'spider': spider})
            return []