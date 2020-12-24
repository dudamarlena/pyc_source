# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/sogubaby/.virtualenvs/scrapy_middlewares/lib/python3.7/site-packages/scrapy_cabinet/extensions/redis_spider_idle_closed_extensions.py
# Compiled at: 2019-11-06 05:29:55
# Size of source mod 2**32: 2361 bytes
from scrapy import signals
from scrapy.exceptions import NotConfigured
from scrapy_cabinet.types import _Crawler, _Spider

class RedisSpiderIdleClosedExtensions(object):
    __doc__ = 'A IdleClosed Extensions to close a idel RedisSpider.\n\n    Attributes:\n        crawler  : _Crawler : A _Crawler from Scrapy.\n        idle_num : int      : A max wait times for idle.\n\n    Methods:\n        spider_idle  | spider: _Spider | A method when spider is idle, every 5 times check redis_key isEmpty.\n    '

    def __init__(self, idle_num: int, crawler: _Crawler) -> None:
        self.crawler = crawler
        self.idle_num = idle_num
        self.idle_list = []
        self.idle_count = 0

    @classmethod
    def from_crawler(cls, crawler: _Crawler) -> object:
        if not crawler.settings.getbool('MYEXT_ENABLED'):
            raise NotConfigured
        if 'redis_key' not in crawler.spidercls.__dict__.keys():
            raise NotConfigured('ONLY SUPPORT REDISSPIDER')
        idle_num = crawler.settings.getint('IDLE_NUMBER', 120)
        ext = cls(idle_num, crawler)
        crawler.signals.connect((ext.spider_opened), signal=(signals.spider_opened))
        crawler.signals.connect((ext.spider_closed), signal=(signals.spider_closed))
        crawler.signals.connect((ext.spider_idle), signal=(signals.spider_idle))
        return ext

    def spider_opened(self, spider: _Spider):
        spider.logger.info('opened spider {}, Allow waiting time:{} second'.format(spider.name, self.idle_num * 5))

    def spider_closed(self, spider: _Spider):
        spider.logger.info('closed spider {}, Waiting time exceeded {} second'.format(spider.name, self.idle_num * 5))

    def spider_idle(self, spider: _Spider):
        if not spider.server.exists(spider.redis_key):
            self.idle_count += 1
        else:
            self.idle_count = 0
        if self.idle_count > self.idle_num:
            self.crawler.engine.close_spider(spider, 'Waiting time exceeded')