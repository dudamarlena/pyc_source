# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/votec/workspace/git/redisy/redisy/redis_set.py
# Compiled at: 2018-07-24 23:26:57
# Size of source mod 2**32: 1194 bytes


class RedisSet:

    def __init__(self, redis, key, converter, content=None):
        self.key_ = key
        self.redis_ = redis
        self.converter_ = converter
        if content:
            self.reset(content)

    def __len__(self):
        return self.redis_.scard(self.key_)

    def __call__(self):
        return {self.converter_.to_value(v) for v in self.redis_.smembers(self.key_)}

    def __repr__(self):
        return str(self())

    def __str__(self):
        return str(self())

    def __contains__(self, key):
        return self.redis_.sismember(self.key_, self.converter_.from_value(key))

    def __delitem__(self, key):
        self.redis_.srem(self.key_, self.converter_.from_value(key))

    def reset(self, value_list=None):
        self.redis_.delete(self.key_)
        if value_list:
            (self.redis_.sadd)(self.key_, *[self.converter_.from_value(v) for v in value_list])

    def add(self, value):
        self.redis_.sadd(self.key_, self.converter_.from_value(value))

    def pop(self):
        return self.converter_.to_value(self.redis_.spop(self.key_))