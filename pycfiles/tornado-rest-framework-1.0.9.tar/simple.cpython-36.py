# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /opt/work/lib/pyenv/versions/3.6.1/envs/maestro/lib/python3.6/site-packages/rest_framework/core/cache/backend/simple.py
# Compiled at: 2018-10-12 04:41:52
# Size of source mod 2**32: 2062 bytes
from time import time
from rest_framework.core.cache.backend.base import BaseCache, DEFAULT_TIMEOUT

class CacheWrapper(BaseCache):
    __doc__ = '\n    简单的内存缓存；\n    适用于单个进程环境，主要用于开发服务器；\n    非线程安全的\n    '

    def __init__(self, server, params):
        super().__init__(server, params)
        self._cache = {}
        self._threshold = self._options.get('THRESHOLD', 0)

    def _prune(self):
        if self._threshold == 0:
            return
        if len(self._cache) > self._threshold:
            now = time()
            for idx, (key, (expires, _)) in enumerate(self._cache.items()):
                if expires is not None and (expires <= now or idx % 3 == 0):
                    self._cache.pop(key, None)

    def get(self, key):
        key = self.make_key(key)
        expires, value = self._cache.get(key, (0, None))
        if expires is None or expires > time():
            return self.decode(value)

    def set(self, key, value, timeout=DEFAULT_TIMEOUT):
        key = self.make_key(key)
        timeout = self.get_backend_timeout(timeout)
        self._prune()
        self._cache[key] = (time() + timeout if timeout else timeout, self.encode(value))

    async def add(self, key, value, timeout=DEFAULT_TIMEOUT):
        key = self.make_key(key)
        timeout = self.get_backend_timeout(timeout)
        if len(self._cache) > self._threshold:
            self._prune()
        item = (
         time() + timeout if timeout else timeout, self.encode(value))
        self._cache.setdefault(key, item)

    async def delete(self, key):
        key = self.make_key(key)
        self._cache.pop(key, None)

    async def clear(self):
        self._cache.clear()

    async def clear_keys(self, key_prefix):
        key = self.make_key(key_prefix)
        del_keys = [k for k in self._cache.keys() if k.startswith(key)]
        for k in del_keys:
            self._cache.pop(k, None)

        return len(del_keys)