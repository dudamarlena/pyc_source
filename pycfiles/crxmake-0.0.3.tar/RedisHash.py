# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/crwy/utils/data/RedisHash.py
# Compiled at: 2020-02-03 23:11:43
from crwy.utils.no_sql.redis_m import get_redis_client

class RedisHash(object):
    """Simple Hash with Redis Backend"""

    def __init__(self, name, server=None, **redis_kwargs):
        """
        The default connection parameters are:
        host='localhost', port=6379, db=0
        """
        if server:
            self.__db = server
        else:
            self.__db = get_redis_client(**redis_kwargs)
        self.key = name

    def hget(self, item):
        """Get item value."""
        return self.__db.hget(self.key, item)

    def hset(self, item, value):
        """Set item value."""
        return self.__db.hset(self.key, item, value)

    def hexists(self, item):
        """Is item exist."""
        return self.__db.hexists(self.key, item)

    def hlen(self):
        """Return total count."""
        return self.__db.hlen(self.key)

    def hkeys(self):
        return self.__db.hkeys(self.key)

    def clean(self):
        """Empty key"""
        return self.__db.delete(self.key)

    def db(self):
        return self.__db