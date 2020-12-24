# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-intel/egg/torngas/cache/backends/dummy.py
# Compiled at: 2016-02-16 00:41:00
"""Dummy cache backend"""
from torngas.cache.backends.base import BaseCache, DEFAULT_TIMEOUT

class DummyCache(BaseCache):

    def __init__(self, host, *args, **kwargs):
        BaseCache.__init__(self, *args, **kwargs)

    def add(self, key, value, timeout=DEFAULT_TIMEOUT, version=None):
        key = self.make_key(key, version=version)
        self.validate_key(key)
        return True

    def get(self, key, default=None, version=None):
        key = self.make_key(key, version=version)
        self.validate_key(key)
        return default

    def set(self, key, value, timeout=DEFAULT_TIMEOUT, version=None):
        key = self.make_key(key, version=version)
        self.validate_key(key)

    def delete(self, key, version=None):
        key = self.make_key(key, version=version)
        self.validate_key(key)

    def get_many(self, keys, version=None):
        return {}

    def has_key(self, key, version=None):
        key = self.make_key(key, version=version)
        self.validate_key(key)
        return False

    def set_many(self, data, timeout=DEFAULT_TIMEOUT, version=None):
        pass

    def delete_many(self, keys, version=None):
        pass

    def clear(self):
        pass