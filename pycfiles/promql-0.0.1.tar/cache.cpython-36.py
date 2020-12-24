# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/prompt_tool_kit/cache.py
# Compiled at: 2019-08-15 23:53:39
# Size of source mod 2**32: 3402 bytes
from __future__ import unicode_literals
from collections import deque
from functools import wraps
__all__ = ('SimpleCache', 'FastDictCache', 'memoized')

class SimpleCache(object):
    """SimpleCache"""

    def __init__(self, maxsize=8):
        assert isinstance(maxsize, int) and maxsize > 0
        self._data = {}
        self._keys = deque()
        self.maxsize = maxsize

    def get(self, key, getter_func):
        """
        Get object from the cache.
        If not found, call `getter_func` to resolve it, and put that on the top
        of the cache instead.
        """
        try:
            return self._data[key]
        except KeyError:
            value = getter_func()
            self._data[key] = value
            self._keys.append(key)
            if len(self._data) > self.maxsize:
                key_to_remove = self._keys.popleft()
                if key_to_remove in self._data:
                    del self._data[key_to_remove]
            return value

    def clear(self):
        """ Clear cache. """
        self._data = {}
        self._keys = deque()


class FastDictCache(dict):
    """FastDictCache"""

    def __init__(self, get_value=None, size=1000000):
        if not callable(get_value):
            raise AssertionError
        elif not (isinstance(size, int) and size > 0):
            raise AssertionError
        self._keys = deque()
        self.get_value = get_value
        self.size = size

    def __missing__(self, key):
        if len(self) > self.size:
            key_to_remove = self._keys.popleft()
            if key_to_remove in self:
                del self[key_to_remove]
        result = (self.get_value)(*key)
        self[key] = result
        self._keys.append(key)
        return result


def memoized(maxsize=1024):
    """
    Momoization decorator for immutable classes and pure functions.
    """
    cache = SimpleCache(maxsize=maxsize)

    def decorator(obj):

        @wraps(obj)
        def new_callable(*a, **kw):

            def create_new():
                return obj(*a, **kw)

            key = (
             a, tuple(kw.items()))
            return cache.get(key, create_new)

        return new_callable

    return decorator