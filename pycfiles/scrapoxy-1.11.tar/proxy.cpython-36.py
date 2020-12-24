# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/fabien/.virtualenvs/scrapy3/lib/python3.6/site-packages/scrapoxy/downloadmiddlewares/proxy.py
# Compiled at: 2017-12-15 11:20:18
# Size of source mod 2**32: 1288 bytes
"""
An extension to use Scrapoxy as a proxy for Scrapy.

You must fill PROXY in settings:
PROXY = 'http://127.0.0.1:8888/?noconnect'

Don't forget the ?noconnect to use HTTPS over HTTP.
"""
from __future__ import unicode_literals
import base64, re

class ProxyMiddleware(object):

    def __init__(self, crawler):
        proxy = crawler.settings.get('PROXY')
        if proxy:
            parts = re.match('(\\w+://)(\\w+:\\w+@)?(.+)', proxy)
            if parts.group(2):
                proxy_auth = parts.group(2)[:-1].encode().decode().strip()
                self._proxy_auth = 'Basic {}'.format(base64.b64encode(proxy_auth.encode('ascii')).decode('ascii'))
                print(self._proxy_auth)
            self._proxy = parts.group(1) + parts.group(3)

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler)

    def process_request(self, request, spider):
        if request.meta.get('no-proxy'):
            return
        if hasattr(self, '_proxy'):
            request.meta['proxy'] = self._proxy
            if hasattr(self, '_proxy_auth'):
                request.headers['proxy-authorization'] = self._proxy_auth