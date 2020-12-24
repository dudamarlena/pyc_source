# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/zhanghang/Desktop/workspace/molbase/molbase_2017_7_3/release/easyspider/easyspider/core/easycrawler.py
# Compiled at: 2017-08-07 09:19:51
"""
    Crawler <- Object
    CrawlerRunner <- Object
    CrawlerProcess <- CrawlerRunner
    关系是 CrawlerRunner 会调用Crawler 从而把三个连起来了
    python 新式类的多继承是：从左到右，宽度优先 (经典类是从左至右，深度优先)
"""
from scrapy.crawler import CrawlerProcess, Crawler, CrawlerRunner
from scrapy.utils.misc import load_object
from twisted.internet import defer
import logging, six, sys
logger = logging.getLogger(__name__)
settings_engine_key = 'ENGINE'
default_engine = 'scrapy.core.engine.ExecutionEngine'

class easyCrawler(Crawler):

    def _create_engine(self):
        engine = self.settings.get(settings_engine_key, default_engine)
        engine_cls = load_object(engine)
        return engine_cls(self, lambda _: self.stop())

    @defer.inlineCallbacks
    def crawl(self, *args, **kwargs):
        """allow spider can return None in start_requests"""
        assert not self.crawling, 'Crawling already taking place'
        self.crawling = True
        try:
            self.spider = self._create_spider(*args, **kwargs)
            self.engine = self._create_engine()
            start_requests = self.spider.start_requests() or ()
            start_requests = iter(start_requests)
            yield self.engine.open_spider(self.spider, start_requests)
            yield defer.maybeDeferred(self.engine.start)
        except Exception:
            if six.PY2:
                exc_info = sys.exc_info()
            self.crawling = False
            if self.engine is not None:
                yield self.engine.close()
            if six.PY2:
                six.reraise(*exc_info)
            raise

        return


class easyCrawlerRunner(CrawlerRunner):

    def _create_crawler(self, spidercls):
        if isinstance(spidercls, six.string_types):
            spidercls = self.spider_loader.load(spidercls)
        return easyCrawler(spidercls, self.settings)


class easyCrawlerProcess(CrawlerProcess, easyCrawlerRunner):
    pass