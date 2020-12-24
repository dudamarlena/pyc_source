# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/redisobjects/redis_list.py
# Compiled at: 2019-09-28 15:18:33
# Size of source mod 2**32: 1856 bytes
from .redis_object import RedisObject
from .serializers import IdentitySerializer

class RedisList(RedisObject):

    def __init__(self, *, connection=None, key=None, serializer=IdentitySerializer()):
        RedisObject.__init__(self, connection=connection, key=key)
        self.serializer = serializer

    def _serialize_values(self, values):
        return [self.serializer.serialize(value) for value in values]

    async def add(self, *values, tx=None):
        tx = tx or self.connection
        return await (self.push_right)(tx, *values)

    async def push_right(self, *values, tx=None):
        tx = tx or self.connection
        return await (tx.execute)('rpush', self.key, *self._serialize_values(values))

    async def push_left(self, *values, tx=None):
        tx = tx or self.connection
        return await (tx.execute)('lpush', self.key, *self._serialize_values(values))

    async def items(self, limit=-1):
        results = await self.connection.execute('lrange', self.key, 0, limit)
        return (self.serializer.deserialize(value) for value in results)

    async def list(self, limit=-1):
        return list(await self.items(limit))

    async def pop_left(self):
        result = await self.connection.execute('lpop', self.key)
        return self.serializer.deserialize(result)

    async def pop_right(self):
        result = await self.connection.execute('rpop', self.key)
        return self.serializer.deserialize(result)

    async def remove(self, value, limit=1, *, tx=None):
        tx = tx or self.connection
        return await tx.execute('lrem', self.key, limit, self.serializer.serialize(value))

    async def size(self):
        return await self.connection.execute('llen', self.key)