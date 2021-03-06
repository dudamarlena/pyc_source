# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-intel/egg/redis_wrap/redis_list.py
# Compiled at: 2015-06-09 08:04:33
from .redis_systems import *
N = 30

class ListFu(redis_obj):

    def append(self, item):
        self.conn.rpush(self.name, item)

    def extend(self, iterable):
        for item in iterable:
            self.append(item)

    def remove(self, value):
        self.conn.lrem(self.name, value)

    def pop(self, index=None):
        if index:
            raise ValueError('Not supported')
        return self.conn.rpop(self.name)

    def list_trim(self, start, stop):
        self.conn.ltrim(self.name, start, stop)

    def __len__(self):
        return self.conn.llen(self.name)

    def __getitem__(self, key):
        if isinstance(key, slice):
            return self.conn.lrange(self.name, key.start, key.stop - 1)
        val = self.conn.lindex(self.name, key)
        if not val:
            raise IndexError
        return val

    def __setitem__(self, key, value):
        try:
            self.conn.lset(self.name, key, value)
        except redis.exceptions.ResponseError:
            raise IndexError

    def __iter__(self):
        i = 0
        while True:
            items = self.conn.lrange(self.name, i, i + N - 1)
            if len(items) == 0:
                raise StopIteration
            for item in items:
                yield item

            i += N