# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-intel/egg/redis_wrap/redis_hash.py
# Compiled at: 2015-02-03 04:24:44
from .redis_systems import *

class HashFu(redis_obj):

    def get(self, key, default=None):
        r = self.conn.hget(self.name, key)
        if r == None:
            r = default
        return r

    def keys(self):
        return self.conn.hkeys(self.name) or []

    def values(self):
        return self.conn.hvals(self.name) or []

    def items(self):
        return self.conn.hgetall(self.name).items()

    def pop(self, key, *args):
        n = self.name

        def f(pipe):
            pipe.multi()
            pipe.hget(n, key)
            pipe.hdel(n, key)

        r = self.conn.transaction(f, key)
        if r and r[1]:
            return r[0]
        if args:
            return args[0]
        raise KeyError

    def update(self, *args, **kwargs):
        for o in args:
            self._update(o)

        self._update(kwargs)

    def _update(self, other):
        if hasattr(other, 'items'):
            for k, v in other.items():
                self[k] = v

        else:
            for k, v in other:
                self[k] = v

    def iter(self):
        for k in self.keys():
            yield k

    def __len__(self):
        return self.conn.hlen(self.name) or 0

    def __iter__(self):
        return self.iter()

    def __getitem__(self, key):
        val = self.get(key)
        if val == None:
            raise KeyError
        return val

    def __setitem__(self, key, value):
        self.conn.hset(self.name, key, value)

    def __delitem__(self, key):
        self.conn.hdel(self.name, key)

    def __contains__(self, key):
        return self.conn.hexists(self.name, key)