# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/redisobjects/redis_dict.py
# Compiled at: 2019-10-06 14:32:54
# Size of source mod 2**32: 2444 bytes
from .redis_object import RedisObject
from .serializers import IdentitySerializer

class RedisDict(RedisObject):

    def __init__(self, *, connection=None, key=None, value_serializer=IdentitySerializer(), field_serializer=IdentitySerializer()):
        RedisObject.__init__(self, connection=connection, key=key)
        self.value_serializer = value_serializer
        self.field_serializer = field_serializer

    async def set(self, field, value, *, tx=None):
        tx = tx or self.connection
        return await tx.execute('hset', self.key, self.field_serializer.serialize(field), self.value_serializer.serialize(value)) > 0

    async def get(self, field):
        result = await self.connection.execute('hget', self.key, self.field_serializer.serialize(field))
        return self.value_serializer.deserialize(result)

    async def items(self):
        results = await self.connection.execute('hgetall', self.key)
        if type(results) == dict:
            return results.items()
        else:
            size = int(len(results) / 2)
            return ((self.field_serializer.deserialize(results[(2 * i)]), self.value_serializer.deserialize(results[(2 * i + 1)])) for i in range(size))

    async def dict(self):
        return {k:v for k, v in await self.items()}

    async def size(self):
        return await self.connection.execute('hlen', self.key)

    async def remove(self, *fields, tx=None):
        tx = tx or self.connection
        serialized_fields = [self.field_serializer.serialize(field) for field in fields]
        return await (tx.execute)('hdel', self.key, *serialized_fields) == len(fields)