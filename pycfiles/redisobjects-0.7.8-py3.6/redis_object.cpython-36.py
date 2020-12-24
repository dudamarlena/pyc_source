# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/redisobjects/redis_object.py
# Compiled at: 2019-09-29 16:53:10
# Size of source mod 2**32: 1300 bytes
"""
A RedisObject can be seen as a single key in a Redis database with a certain
structure (atomic, hash, list, etc.) and convenient methods that correspond
to Redis operations.
"""

class RedisObject:

    def __init__(self, *, connection=None, key=None):
        self.connection = connection
        self.key = key

    async def watch(self, *, tx=None):
        tx = tx or self.connection
        return await tx.execute('watch', self.key)

    async def unwatch(self, *, tx=None):
        tx = tx or self.connection
        return await tx.execute('unwatch', self.key)

    async def delete(self, *, tx=None):
        tx = tx or self.connection
        return await tx.execute('del', self.key)

    async def expire(self, duration, *, tx=None):
        tx = tx or self.connection
        return await tx.execute('expire', self.key, duration)