# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/redisobjects/redis_keyspace.py
# Compiled at: 2019-09-28 15:18:33
# Size of source mod 2**32: 1697 bytes
from .serializers import IdentitySerializer
from .redis_object_factory import RedisObjectFactory
from shortuuid import uuid

class RedisKeyspace(RedisObjectFactory):

    def __init__(self, connection, keyspace='?', key_serializer=IdentitySerializer(), key_factory=lambda : str(uuid())):
        RedisObjectFactory.__init__(self, connection)
        self.key_serializer = key_serializer
        self.placeholder = '?'
        self.keyspace = keyspace
        self.key_factory = key_factory

    def _make_key(self, key=None):
        if key is None:
            key = self.key_factory()
        serialized_key = self.key_serializer.serialize(key)
        complete_key = self.keyspace.replace(self.placeholder, serialized_key)
        if self.placeholder in complete_key:
            raise RuntimeError('Not all placeholders have been replaced for `%s`' % (complete_key,))
        return complete_key