# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-x86_64/egg/ycyc/libs/rediskit/hash_dict.py
# Compiled at: 2016-02-25 04:17:16
from collections import MutableMapping
import cPickle
from .base import RedisKit

class RedisHashDict(MutableMapping, RedisKit):
    Convertor = cPickle

    def __init__(self, connection, name, *args, **kwargs):
        self.connection = connection
        self.name = name
        super(RedisHashDict, self).__init__(*args, **kwargs)

    def __setitem__(self, key, value):
        self.connection.hset(self.name, key, self.Convertor.dumps(value))

    def __getitem__(self, key):
        value = self.connection.hget(self.name, key)
        if value is None:
            raise KeyError('%s not found' % key)
        return self.Convertor.loads(value)

    def __delitem__(self, key):
        if self.connection.hdel(self.name, key) == 0:
            raise KeyError('%s not found' % key)

    def __iter__(self):
        return iter(self.connection.hkeys(self.name))

    def __len__(self):
        return self.connection.hlen(self.name)

    def __contains__(self, key):
        return self.connection.hexists(self.name, key)