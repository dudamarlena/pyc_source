# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/zhanghang/Desktop/workspace/molbase/molbase_2017_7_3/release/easyspider/easyspider/core/easyScraper.py
# Compiled at: 2017-08-03 10:12:10
from scrapy.core.scraper import Scraper
from scrapy.utils.request import referer_str
from scrapy.utils.log import failure_to_exc_info

class easyScraper(Scraper):

    def handle_spider_error(self, _failure, request, response, spider):
        super(easyScraper, self).handle_spider_error(_failure, request, response, spider)
        spider.blocked_call_back(response, reason='Spider error processing %(request)s (referer: %(referer)s)' % {'request': request, 'referer': referer_str(request)}, exc_info=failure_to_exc_info(_failure), extra=self.__class__.__name__)