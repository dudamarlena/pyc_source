# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/sogubaby/anaconda3/envs/tbb/lib/python3.8/site-packages/scrapy_redis_bloomfilter/pipelines.py
# Compiled at: 2019-11-26 21:39:54
# Size of source mod 2**32: 2083 bytes
from scrapy.utils.misc import load_object
from scrapy.utils.serialize import ScrapyJSONEncoder
from twisted.internet.threads import deferToThread
from . import connection, defaults
default_serialize = ScrapyJSONEncoder().encode

class RedisPipeline(object):
    __doc__ = 'Pushes serialized item into a redis list/queue\n\n    Settings\n    --------\n    REDIS_ITEMS_KEY : str\n        Redis key where to store items.\n    REDIS_ITEMS_SERIALIZER : str\n        Object path to serializer function.\n\n    '

    def __init__(self, server, key=defaults.PIPELINE_KEY, serialize_func=default_serialize):
        """Initialize pipeline.

        Parameters
        ----------
        server : StrictRedis
            Redis client instance.
        key : str
            Redis key where to store items.
        serialize_func : callable
            Items serializer function.

        """
        self.server = server
        self.key = key
        self.serialize = serialize_func

    @classmethod
    def from_settings(cls, settings):
        params = {'server': connection.from_settings(settings)}
        if settings.get('REDIS_ITEMS_KEY'):
            params['key'] = settings['REDIS_ITEMS_KEY']
        if settings.get('REDIS_ITEMS_SERIALIZER'):
            params['serialize_func'] = load_object(settings['REDIS_ITEMS_SERIALIZER'])
        return cls(**params)

    @classmethod
    def from_crawler(cls, crawler):
        return cls.from_settings(crawler.settings)

    def process_item(self, item, spider):
        return deferToThread(self._process_item, item, spider)

    def _process_item(self, item, spider):
        key = self.item_key(item, spider)
        data = self.serialize(item)
        self.server.rpush(key, data)
        return item

    def item_key(self, item, spider):
        """Returns redis key based on given spider.

        Override this function to use a different key depending on the item
        and/or spider.

        """
        return self.key % {'spider': spider.name}