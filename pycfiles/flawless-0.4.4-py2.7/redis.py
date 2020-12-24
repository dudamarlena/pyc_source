# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/flawless/lib/storage/redis.py
# Compiled at: 2018-03-20 23:48:02
from __future__ import absolute_import
try:
    import cPickle as pickle
except ImportError:
    import pickle

from future.utils import iteritems
import redis, flawless.lib.config
from flawless.lib.storage import StorageInterface

class RedisStorage(StorageInterface):

    def __init__(self, host, port, partition, socket_timeout=2):
        super(RedisStorage, self).__init__(partition=partition)
        self.redis_partition_name = self.partition if self.partition else 'config'
        self.client = redis.Redis(host=host, port=port, socket_timeout=socket_timeout)
        config = flawless.lib.config.get()
        self.redis_version = config.redis_version

    def _redis_key(self, key):
        """We use repr instead of pickle.dumps(key) because in pickle dumping the object is not always guaranteed
        to be the same exact string"""
        return repr(key)

    def _serialize_data(self, key, value):
        return pickle.dumps((key, value), pickle.HIGHEST_PROTOCOL)

    def _deserialize_data(self, data):
        if data is None:
            return (None, None)
        else:
            parsed_data = pickle.loads(data)
            if not isinstance(parsed_data, tuple) or len(parsed_data) != 2:
                return (None, None)
            key, value = parsed_data
            self.migrate_thrift_obj(key)
            self.migrate_thrift_obj(value)
            return (key, value)

    def _hscan_iter(self, name):
        if hasattr(self.client, 'hscan_iter') and self.redis_version >= '2.8':
            for key, value in self.client.hscan_iter(name):
                yield (
                 key, value)

            return
        for key, value in iteritems(self.client.hgetall(name)):
            yield (
             key, value)

        return

    def iteritems(self):
        for redis_key, data in self._hscan_iter(self.redis_partition_name):
            yield self._deserialize_data(data)

    def __setitem__(self, key, item):
        self.client.hset(self.redis_partition_name, self._redis_key(key), self._serialize_data(key, item))

    def __getitem__(self, key):
        data = self.client.hget(self.redis_partition_name, self._redis_key(key))
        return self._deserialize_data(data)[1]

    def __contains__(self, key):
        return self.client.hexists(self.redis_partition_name, self._redis_key(key))