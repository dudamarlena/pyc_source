# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/fabien/.virtualenvs/scrapy3/lib/python3.6/site-packages/scrapoxy/downloadmiddlewares/wait.py
# Compiled at: 2017-12-14 13:10:42
# Size of source mod 2**32: 862 bytes
"""
An extension to wait at least 1 instance on Scrapoxy.

You can change the delay with WAIT_FOR_START parameters (120 seconds by default).
"""
from __future__ import unicode_literals
import logging, time

class WaitMiddleware(object):

    def __init__(self, crawler):
        self._WAIT_FOR_START = crawler.settings.get('WAIT_FOR_START') or 120

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler)

    def process_response(self, request, response, spider):
        if response.status != 407:
            return response
        else:
            spider.log(('[WaitMiddleware] Sleeping {0} seconds because no proxy is found: {1}'.format(self._WAIT_FOR_START, response.text)), level=(logging.WARNING))
            time.sleep(self._WAIT_FOR_START)
            return request.replace(dont_filter=True)