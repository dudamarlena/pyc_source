# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/redisobjects/redis_atom.py
# Compiled at: 2019-09-28 15:18:33
# Size of source mod 2**32: 1093 bytes
from .redis_object import RedisObject
from .serializers import IdentitySerializer
import aioredis

class RedisAtom(RedisObject):

    def __init__(self, *, connection=None, key=None, serializer=IdentitySerializer()):
        RedisObject.__init__(self, connection=connection, key=key)
        self.serializer = serializer

    async def get(self):
        value = await self.connection.execute('get', self.key)
        return self.serializer.deserialize(value)

    async def exists(self):
        return await self.connection.execute('exists', self.key) > 0

    async def set(self, value, *, tx=None):
        serialized_value = self.serializer.serialize(value)
        tx = tx or self.connection
        return await tx.execute('set', self.key, serialized_value)

    async def remove(self, *, tx=None):
        tx = tx or self.connection
        return await tx.execute('del', self.key) > 0