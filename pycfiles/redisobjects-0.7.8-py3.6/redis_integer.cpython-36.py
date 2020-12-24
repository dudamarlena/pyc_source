# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/redisobjects/redis_integer.py
# Compiled at: 2019-10-05 22:02:52
# Size of source mod 2**32: 1118 bytes
from .redis_atom import RedisAtom
from .serializers import GenericSerializer

class RedisInteger(RedisAtom):

    def __init__(self, *, connection=None, key=None):
        RedisAtom.__init__(self, connection=connection, key=key, serializer=(GenericSerializer(int)))

    async def increment(self, *, n=1, tx=None):
        tx = tx or self.connection
        if n == 1:
            return await tx.execute('incr', self.key)
        else:
            return await tx.execute('incrby', self.key, n)

    async def decrement(self, *, n=1, tx=None):
        tx = tx or self.connection
        if n == 1:
            return await tx.execute('decr', self.key)
        else:
            return await tx.execute('decrby', self.key, n)