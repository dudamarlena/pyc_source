# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\soccer\tm\middlewares.py
# Compiled at: 2018-01-08 04:59:40
# Size of source mod 2**32: 1900 bytes
from scrapy import signals

class TmSpiderMiddleware(object):

    @classmethod
    def from_crawler(cls, crawler):
        s = cls()
        crawler.signals.connect((s.spider_opened), signal=(signals.spider_opened))
        return s

    def process_spider_input(self, response, spider):
        pass

    def process_spider_output(self, response, result, spider):
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        pass

    def process_start_requests(self, start_requests, spider):
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)