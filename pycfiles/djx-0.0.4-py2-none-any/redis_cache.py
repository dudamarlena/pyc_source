# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-HZd96S/pip/pip/_vendor/cachecontrol/caches/redis_cache.py
# Compiled at: 2019-02-14 00:35:06
from __future__ import division
from datetime import datetime
from pip._vendor.cachecontrol.cache import BaseCache

class RedisCache(BaseCache):

    def __init__(self, conn):
        self.conn = conn

    def get(self, key):
        return self.conn.get(key)

    def set(self, key, value, expires=None):
        if not expires:
            self.conn.set(key, value)
        else:
            expires = expires - datetime.utcnow()
            self.conn.setex(key, int(expires.total_seconds()), value)

    def delete(self, key):
        self.conn.delete(key)

    def clear(self):
        """Helper for clearing all the keys in a database. Use with
        caution!"""
        for key in self.conn.keys():
            self.conn.delete(key)

    def close(self):
        """Redis uses connection pooling, no need to close the connection."""
        pass