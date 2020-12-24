# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/crwy/utils/filter/RedisSet.py
# Compiled at: 2020-02-03 23:11:43
from crwy.utils.no_sql.redis_m import get_redis_client

class RedisSet(object):
    """Simple Deduplicate with Redis Backend"""

    def __init__(self, name, namespace='deduplicate', server=None, **redis_kwargs):
        """
        The default connection parameters are:
        host='localhost', port=6379, db=0
        """
        if server:
            self.__db = server
        else:
            self.__db = get_redis_client(**redis_kwargs)
        self.key = '%s:%s' % (namespace, name)

    def sadd(self, item):
        """Add item."""
        if self.__db.sadd(self.key, item) == 0:
            return False
        else:
            return True

    def srem(self, item):
        """Del item."""
        if self.__db.srem(self.key, item) == 0:
            return False
        else:
            return True

    def scard(self):
        """Return total count."""
        return self.__db.scard(self.key)

    def smembers(self):
        """Return all item."""
        return self.__db.smembers(self.key)

    def clean(self):
        """Empty key"""
        return self.__db.delete(self.key)

    def db(self):
        return self.__db