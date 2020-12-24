# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/sogubaby/.virtualenvs/scrapy_middlewares/lib/python3.7/site-packages/scrapy_cabinet/downloadermiddlewares/proxy_downloader_middleware.py
# Compiled at: 2019-11-06 05:29:55
# Size of source mod 2**32: 2640 bytes
import random
from typing import Optional
from scrapy import signals
from scrapy_cabinet.exceptions import NotSetProxyError
from scrapy_cabinet.utils import LOGGER
from scrapy_cabinet.types import _Proxies, _Crawler, _Spider, _Request

class ProxyDownloaderMiddleware(object):
    __doc__ = 'A base DownloaderMiddleware to set proxy to Scrapy request.\n\n    To use this Middleware, Project should set proxy_url or proxy_pool in settings.py.\n    When use PROXY_URL, PROXY_TYPE should be set at the same time.\n        PROXY_TYPE == 1 or PROXY_TYPE == 0.\n\n    Attributes:\n        proxies : _Proxies : A _Proxies type to store proxy_url.\n        is_init : bool     : A bool value to check the proxies is set successfully\n\n    Methods:\n        get_proxies  | Args: NaN | A method to get proxy_url, when use proxy_url and proxy_type == 1\n                                   this method can not be implemented.\n\n    '

    def __init__(self, proxies: _Proxies) -> None:
        self.proxies = proxies
        self.is_init = True

    @classmethod
    def from_crawler(cls, crawler: _Crawler) -> object:
        o = None
        proxies = crawler.settings.get('PROXY_URL')
        if proxies:
            proxies_type = crawler.settings.get('PROXY_TYPE')
            if proxies_type == 0:
                o = cls(proxies)
                o.proxies = o.get_proxies()
            else:
                o = cls(proxies)
        proxies = crawler.settings.get('PROXY_POOL')
        if proxies:
            LOGGER.warning('THIS PROXY_POOL WILL BE DROPED IN A FUTURE VERSION, PLEASE USE PROXY_URL and IMPLEMENT get_proxies method')
            o = cls(proxies)
        if o:
            crawler.signals.connect((o.spider_opened), signal=(signals.spider_opened))
            return o
        LOGGER.error('TO USE THIS MIDDLEWARE ,PLEASE SET PROXY_URL OR PROXY_POOL')
        raise NotSetProxyError()

    def spider_opened(self, spider: _Spider) -> None:
        spider.logger.info(f"Proxy Has Been Set. Type: {type(self.proxies)}")

    def process_request(self, request: _Request, spider: _Spider) -> None:
        if isinstance(self.proxies, list):
            proxies = random.choice(self.proxies)
        else:
            proxies = self.proxies
        request.meta['proxy'] = proxies
        spider.logger.debug(f"{proxies}")

    def get_proxies(self) -> Optional[_Proxies]:
        raise NotImplementedError()