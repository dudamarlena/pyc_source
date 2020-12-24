# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/sogubaby/anaconda3/envs/tbb/lib/python3.8/site-packages/scrapy_redis_bloomfilter/dupefilter.py
# Compiled at: 2019-11-27 02:46:39
# Size of source mod 2**32: 4482 bytes
import logging, time
from scrapy.dupefilters import BaseDupeFilter
from scrapy.utils.request import request_fingerprint
from .defaults import BLOOMFILTER_HASH_NUMBER, BLOOMFILTER_BIT, DUPEFILTER_DEBUG
from . import defaults
from .connection import get_redis_from_settings
from iron_man import RedisBloomFilter
logger = logging.getLogger(__name__)

class RFPDupeFilter(BaseDupeFilter):
    __doc__ = "Redis-based request duplicates filter.\n\n    This class can also be used with default Scrapy's scheduler.\n\n    "
    logger = logger

    def __init__(self, server, key, debug, bit, hash_number):
        """Initialize the duplicates filter.

        Parameters
        ----------
        server : redis.StrictRedis
            The redis server instance.
        key : str
            Redis key Where to store fingerprints.
        debug : bool, optional
            Whether to log filtered requests.

        """
        self.server = server
        self.key = key
        self.debug = debug
        self.bit = bit
        self.hash_number = hash_number
        self.logdupes = True
        self.bf = RedisBloomFilter(bit, 0.0001, self.server)

    @classmethod
    def from_settings(cls, settings):
        """Returns an instance from given settings.

        This uses by default the key ``dupefilter:<timestamp>``. When using the
        ``scrapy_redis.scheduler.Scheduler`` class, this method is not used as
        it needs to pass the spider name in the key.

        Parameters
        ----------
        settings : scrapy.settings.Settings

        Returns
        -------
        RFPDupeFilter
            A RFPDupeFilter instance.

        """
        server = get_redis_from_settings(settings)
        key = defaults.DUPEFILTER_KEY % {'timestamp': int(time.time())}
        debug = settings.getbool('DUPEFILTER_DEBUG', DUPEFILTER_DEBUG)
        bit = settings.getint('BLOOMFILTER_BIT', BLOOMFILTER_BIT)
        hash_number = settings.getint('BLOOMFILTER_HASH_NUMBER', BLOOMFILTER_HASH_NUMBER)
        return cls(server, key=key, debug=debug, bit=bit, hash_number=hash_number)

    @classmethod
    def from_crawler(cls, crawler):
        """Returns instance from crawler.

        Parameters
        ----------
        crawler : scrapy.crawler.Crawler

        Returns
        -------
        RFPDupeFilter
            Instance of RFPDupeFilter.

        """
        instance = cls.from_settings(crawler.settings)
        return instance

    def request_seen(self, request):
        if self.bf.is_contain(self.key, request.url):
            return True
        self.bf.add(self.key, request.url)

    def request_fingerprint(self, request):
        """Returns a fingerprint for a given request.

        Parameters
        ----------
        request : scrapy.http.Request

        Returns
        -------
        str

        """
        return request_fingerprint(request)

    def close(self, reason=''):
        """Delete data on close. Called by Scrapy's scheduler.

        Parameters
        ----------
        reason : str, optional

        """
        self.clear()

    def clear(self):
        """Clears fingerprints data."""
        pass

    def log(self, request, spider):
        """Logs given request.

        Parameters
        ----------
        request : scrapy.http.Request
        spider : scrapy.spiders.Spider

        """
        if self.debug:
            msg = 'Filtered duplicate request: %(request)s'
            self.logger.debug(msg, {'request': request}, extra={'spider': spider})
        else:
            if self.logdupes:
                msg = 'Filtered duplicate request %(request)s - no more duplicates will be shown (see DUPEFILTER_DEBUG to show all duplicates)'
                self.logger.debug(msg, {'request': request}, extra={'spider': spider})
                self.logdupes = False
        spider.crawler.stats.inc_value('bloomfilter/filtered', spider=spider)