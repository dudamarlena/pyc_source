# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/fabien/.virtualenvs/scrapy3/lib/python3.6/site-packages/scrapoxy/downloadmiddlewares/blacklist.py
# Compiled at: 2017-12-15 11:04:43
# Size of source mod 2**32: 2842 bytes
"""
An extension to detect blacklisted status and restart Scrapoxy instances.

You must fill :
API_SCRAPOXY with the commander URL
API_SCRAPOXY_PASSWORD with credential
BLACKLIST_HTTP_STATUS_CODES with the list of blacklisted HTTP codes
"""
from __future__ import unicode_literals
from scrapy.exceptions import IgnoreRequest
from scrapoxy.commander import Commander
import logging, random, time

class BlacklistError(Exception):

    def __init__(self, response, message, *args, **kwargs):
        (super(BlacklistError, self).__init__)(*args, **kwargs)
        self.response = response
        self.message = message

    def __str__(self):
        return self.message


class BlacklistDownloaderMiddleware(object):

    def __init__(self, crawler):
        """Access the settings of the crawler to connect to Scrapoxy.
        """
        self._http_status_codes = crawler.settings.get('BLACKLIST_HTTP_STATUS_CODES', [503])
        self._sleep_min = crawler.settings.get('SCRAPOXY_SLEEP_MIN', 60)
        self._sleep_max = crawler.settings.get('SCRAPOXY_SLEEP_MAX', 180)
        self._commander = Commander(crawler.settings.get('API_SCRAPOXY'), crawler.settings.get('API_SCRAPOXY_PASSWORD'))

    @classmethod
    def from_crawler(cls, crawler):
        """Call constructor with crawler parameters
        """
        return cls(crawler)

    def process_response(self, request, response, spider):
        """Detect blacklisted response and stop the instance if necessary.
        """
        try:
            if response.status in self._http_status_codes:
                raise BlacklistError(response, 'HTTP status {}'.format(response.status))
            return response
        except BlacklistError as ex:
            spider.log(('Ignoring Blacklisted response {0}: {1}'.format(response.url, ex.message)), level=(logging.DEBUG))
            name = response.headers['x-cache-proxyname'].decode('utf-8')
            self._stop_and_sleep(spider, name)
            raise IgnoreRequest()

    def _stop_and_sleep(self, spider, name):
        if name:
            alive = self._commander.stop_instance(name)
            if alive < 0:
                spider.log(('Remove: cannot find instance {}'.format(name)), level=(logging.ERROR))
            else:
                if alive == 0:
                    spider.log('Remove: instance removed (no instance remaining)', level=(logging.WARNING))
                else:
                    spider.log(('Remove: instance removed ({} instances remaining)'.format(alive)), level=(logging.DEBUG))
        else:
            spider.log('Cannot find instance name in headers', level=(logging.ERROR))
        delay = random.randrange(self._sleep_min, self._sleep_max)
        spider.log(('Sleeping {} seconds'.format(delay)), level=(logging.INFO))
        time.sleep(delay)