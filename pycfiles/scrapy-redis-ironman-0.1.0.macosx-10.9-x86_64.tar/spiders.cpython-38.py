# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/sogubaby/anaconda3/envs/tbb/lib/python3.8/site-packages/scrapy_redis_bloomfilter/spiders.py
# Compiled at: 2019-11-26 21:39:54
# Size of source mod 2**32: 6835 bytes
from scrapy import signals
from scrapy.exceptions import DontCloseSpider
from scrapy.spiders import Spider, CrawlSpider
from . import connection, defaults
from .utils import bytes_to_str

class RedisMixin(object):
    __doc__ = 'Mixin class to implement reading urls from a redis queue.'
    redis_key = None
    redis_batch_size = None
    redis_encoding = None
    server = None

    def start_requests(self):
        """Returns a batch of start requests from redis."""
        return self.next_requests()

    def setup_redis(self, crawler=None):
        """Setup redis connection and idle signal.

        This should be called after the spider has set its crawler object.
        """
        if self.server is not None:
            return
        else:
            if crawler is None:
                crawler = getattr(self, 'crawler', None)
            if crawler is None:
                raise ValueError('crawler is required')
            settings = crawler.settings
            if self.redis_key is None:
                self.redis_key = settings.get('REDIS_START_URLS_KEY', defaults.START_URLS_KEY)
            self.redis_key = self.redis_key % {'name': self.name}
            assert self.redis_key.strip(), 'redis_key must not be empty'
        if self.redis_batch_size is None:
            self.redis_batch_size = settings.getint('REDIS_START_URLS_BATCH_SIZE', settings.getint('CONCURRENT_REQUESTS'))
        try:
            self.redis_batch_size = int(self.redis_batch_size)
        except (TypeError, ValueError):
            raise ValueError('redis_batch_size must be an integer')
        else:
            if self.redis_encoding is None:
                self.redis_encoding = settings.get('REDIS_ENCODING', defaults.REDIS_ENCODING)
            self.logger.info("Reading start URLs from redis key '%(redis_key)s' (batch size: %(redis_batch_size)s, encoding: %(redis_encoding)s", self.__dict__)
            self.server = connection.from_settings(crawler.settings)
            crawler.signals.connect((self.spider_idle), signal=(signals.spider_idle))

    def next_requests(self):
        """Returns a request to be scheduled or none."""
        use_set = self.settings.getbool('REDIS_START_URLS_AS_SET', defaults.START_URLS_AS_SET)
        fetch_one = self.server.spop if use_set else self.server.lpop
        found = 0
        while found < self.redis_batch_size:
            data = fetch_one(self.redis_key)
            if not data:
                break
            req = self.make_request_from_data(data)
            if req:
                (yield req)
                found += 1
            else:
                self.logger.debug('Request not made from data: %r', data)

        if found:
            self.logger.debug("Read %s requests from '%s'", found, self.redis_key)

    def make_request_from_data(self, data):
        """Returns a Request instance from data coming from Redis.

        By default, ``data`` is an encoded URL. You can override this method to
        provide your own message decoding.

        Parameters
        ----------
        data : bytes
            Message from redis.

        """
        url = bytes_to_str(data, self.redis_encoding)
        return self.make_requests_from_url(url)

    def schedule_next_requests(self):
        """Schedules a request if available"""
        for req in self.next_requests():
            self.crawler.engine.crawl(req, spider=self)

    def spider_idle(self):
        """Schedules a request if available, otherwise waits."""
        self.schedule_next_requests()
        raise DontCloseSpider


class RedisSpider(RedisMixin, Spider):
    __doc__ = 'Spider that reads urls from redis queue when idle.\n\n    Attributes\n    ----------\n    redis_key : str (default: REDIS_START_URLS_KEY)\n        Redis key where to fetch start URLs from..\n    redis_batch_size : int (default: CONCURRENT_REQUESTS)\n        Number of messages to fetch from redis on each attempt.\n    redis_encoding : str (default: REDIS_ENCODING)\n        Encoding to use when decoding messages from redis queue.\n\n    Settings\n    --------\n    REDIS_START_URLS_KEY : str (default: "<spider.name>:start_urls")\n        Default Redis key where to fetch start URLs from..\n    REDIS_START_URLS_BATCH_SIZE : int (deprecated by CONCURRENT_REQUESTS)\n        Default number of messages to fetch from redis on each attempt.\n    REDIS_START_URLS_AS_SET : bool (default: False)\n        Use SET operations to retrieve messages from the redis queue. If False,\n        the messages are retrieve using the LPOP command.\n    REDIS_ENCODING : str (default: "utf-8")\n        Default encoding to use when decoding messages from redis queue.\n\n    '

    @classmethod
    def from_crawler(self, crawler, *args, **kwargs):
        obj = (super(RedisSpider, self).from_crawler)(crawler, *args, **kwargs)
        obj.setup_redis(crawler)
        return obj


class RedisCrawlSpider(RedisMixin, CrawlSpider):
    __doc__ = 'Spider that reads urls from redis queue when idle.\n\n    Attributes\n    ----------\n    redis_key : str (default: REDIS_START_URLS_KEY)\n        Redis key where to fetch start URLs from..\n    redis_batch_size : int (default: CONCURRENT_REQUESTS)\n        Number of messages to fetch from redis on each attempt.\n    redis_encoding : str (default: REDIS_ENCODING)\n        Encoding to use when decoding messages from redis queue.\n\n    Settings\n    --------\n    REDIS_START_URLS_KEY : str (default: "<spider.name>:start_urls")\n        Default Redis key where to fetch start URLs from..\n    REDIS_START_URLS_BATCH_SIZE : int (deprecated by CONCURRENT_REQUESTS)\n        Default number of messages to fetch from redis on each attempt.\n    REDIS_START_URLS_AS_SET : bool (default: True)\n        Use SET operations to retrieve messages from the redis queue.\n    REDIS_ENCODING : str (default: "utf-8")\n        Default encoding to use when decoding messages from redis queue.\n\n    '

    @classmethod
    def from_crawler(self, crawler, *args, **kwargs):
        obj = (super(RedisCrawlSpider, self).from_crawler)(crawler, *args, **kwargs)
        obj.setup_redis(crawler)
        return obj