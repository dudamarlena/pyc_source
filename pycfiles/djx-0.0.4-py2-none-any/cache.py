# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-HZd96S/pip/pip/_vendor/cachecontrol/cache.py
# Compiled at: 2019-02-14 00:35:06
"""
The cache object API for implementing caches. The default is a thread
safe in-memory dictionary.
"""
from threading import Lock

class BaseCache(object):

    def get(self, key):
        raise NotImplementedError()

    def set(self, key, value):
        raise NotImplementedError()

    def delete(self, key):
        raise NotImplementedError()

    def close(self):
        pass


class DictCache(BaseCache):

    def __init__(self, init_dict=None):
        self.lock = Lock()
        self.data = init_dict or {}

    def get(self, key):
        return self.data.get(key, None)

    def set(self, key, value):
        with self.lock:
            self.data.update({key: value})

    def delete(self, key):
        with self.lock:
            if key in self.data:
                self.data.pop(key)