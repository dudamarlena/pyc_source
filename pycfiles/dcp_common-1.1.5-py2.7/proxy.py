# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/dcp_common/middlewares/proxy.py
# Compiled at: 2018-09-28 07:51:59
import logging, requests

class ProxyMiddleware:

    def __init__(self, proxy_url, proxy_fail_times):
        self.logger = logging.getLogger(__name__)
        self.proxy_url = proxy_url
        self.proxy_fail_times = proxy_fail_times

    def get_random_proxy(self):
        try:
            response = requests.get(self.proxy_url)
            if response.status_code == 200:
                proxy = response.text
                return proxy
        except requests.ConnectionError:
            return False

    def process_request(self, request, spider):
        if request.meta.get('retry_times') >= self.proxy_fail_times:
            proxy = self.get_random_proxy()
            if proxy:
                uri = ('https://{proxy}').format(proxy=proxy)
                self.logger.debug(('Using Proxy {proxy}').format(proxy=proxy))
                request.meta['proxy'] = uri

    @classmethod
    def from_crawler(cls, crawler):
        settings = crawler.settings
        return cls(proxy_url=settings.get('PROXY_URL'), proxy_fail_times=settings.get('PROXY_FAIL_TIMES', 1))