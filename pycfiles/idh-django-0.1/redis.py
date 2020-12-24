# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: .\django\core\cache\redis.py
# Compiled at: 2018-02-12 22:08:21
# Size of source mod 2**32: 1097 bytes
import redis
from idh.django.cache.base import Cache

class RedisCache(Cache):

    def __init__(self, **kwargs):
        super(RedisCache, self).__init__(**kwargs)
        self.connection = redis.StrictRedis(host=self.config['host'], port=self.config['port'], db=self.config['db'], password=self.config['password'], decode_responses=True)

    def doGet(self, group, key):
        return self.connection.get(group + key)

    def doSet(self, group, key, value, expiry=None):
        result = self.connection.set(group + key, value)
        if expiry is not None:
            self.connection.expire(group + key, expiry)
        return result

    def doExpire(self, group, key, expiry=None):
        if expiry is not None:
            return self.connection.expire(group + key, expiry)
        return False

    def doDelete(self, group, key):
        return self.connection.delete(group + key)

    def isExists(self, group, key):
        return self.connection.exists(group + key)