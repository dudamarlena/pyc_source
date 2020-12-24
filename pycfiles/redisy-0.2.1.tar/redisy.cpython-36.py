# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/votec/workspace/git/redisy/redisy/redisy.py
# Compiled at: 2018-07-26 23:34:26
# Size of source mod 2**32: 1616 bytes
try:
    from redis import Redis
except ImportError:
    Redis = object

from .converter import Converter
from .redis_list import RedisList
from .redis_set import RedisSet
from .redis_hash import RedisHash

class Redisy(Redis):

    def __init__(self, **args):
        (super(Redisy, self).__init__)(**args)
        self.converter_ = Converter('json')
        self.args_ = args

    def __getitem__(self, key):
        t = self.type(key)
        if t == b'string':
            return self.converter_.to_value(self.get(key))
        if t == b'list':
            return RedisList(self, key, self.converter_)
        if t == b'set':
            return RedisSet(self, key, self.converter_)
        if t == b'hash':
            return RedisHash(self, key, self.converter_)
        if t == b'none':
            return

    def __setitem__(self, key, value):
        t = type(value)
        if t is list:
            RedisList(self, key, self.converter_, value)
        else:
            if t is set:
                RedisSet(self, key, self.converter_, value)
            else:
                if t is dict:
                    RedisHash(self, key, self.converter_, value)
                else:
                    super(Redisy, self).set(key, self.converter_.from_value(value))

    def __delitem__(self, key):
        self.delete(key)

    def select(self, db):
        self.args_['db'] = db
        (super(Redisy, self).__init__)(**self.args_)

    def list(self, key):
        return RedisList(self, key, self.converter_)

    def set(self, key):
        return RedisSet(self, key, self.converter_)

    def hash(self, key):
        return RedisHash(self, key, self.converter_)