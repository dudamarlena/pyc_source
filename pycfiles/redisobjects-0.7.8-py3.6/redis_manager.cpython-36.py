# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/redisobjects/redis_manager.py
# Compiled at: 2019-09-28 15:18:33
# Size of source mod 2**32: 1103 bytes
from .redis_keyspace import RedisKeyspace
from .redis_entity_space import RedisEntitySpace
from .redis_object_factory import RedisObjectFactory
from .redis_transaction import RedisTransaction
from .serializers import IdentitySerializer
from aioredis import create_connection

class RedisManager(RedisObjectFactory):

    def __init__(self, connection):
        RedisObjectFactory.__init__(self, connection)

    def keyspace(self, keyspace, key_serializer=IdentitySerializer()):
        return RedisKeyspace(self.connection, keyspace, key_serializer)

    def object_space(self, keyspace, cls, *, key_serializer=IdentitySerializer()):
        return self.entity_space(keyspace, cls, key_serializer=key_serializer)

    def entity_space(self, keyspace, cls, *, key_serializer=IdentitySerializer()):
        return RedisEntitySpace((self.connection), keyspace, cls, key_serializer=key_serializer)

    def create_transaction(self):
        return RedisTransaction(self.connection)

    def close(self):
        self.connection.close()