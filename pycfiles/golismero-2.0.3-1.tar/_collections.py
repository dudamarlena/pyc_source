# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/Dani/Documents/Projects/Golismero_2.0/src_github/thirdparty_libs/requests/packages/urllib3/_collections.py
# Compiled at: 2013-08-26 10:52:44
from collections import MutableMapping
from threading import RLock
try:
    from collections import OrderedDict
except ImportError:
    from .packages.ordered_dict import OrderedDict

__all__ = [
 'RecentlyUsedContainer']
_Null = object()

class RecentlyUsedContainer(MutableMapping):
    """
    Provides a thread-safe dict-like container which maintains up to
    ``maxsize`` keys while throwing away the least-recently-used keys beyond
    ``maxsize``.

    :param maxsize:
        Maximum number of recent elements to retain.

    :param dispose_func:
        Every time an item is evicted from the container,
        ``dispose_func(value)`` is called.  Callback which will get called
    """
    ContainerCls = OrderedDict

    def __init__(self, maxsize=10, dispose_func=None):
        self._maxsize = maxsize
        self.dispose_func = dispose_func
        self._container = self.ContainerCls()
        self.lock = RLock()

    def __getitem__(self, key):
        with self.lock:
            item = self._container.pop(key)
            self._container[key] = item
            return item

    def __setitem__(self, key, value):
        evicted_value = _Null
        with self.lock:
            evicted_value = self._container.get(key, _Null)
            self._container[key] = value
            if len(self._container) > self._maxsize:
                _key, evicted_value = self._container.popitem(last=False)
        if self.dispose_func and evicted_value is not _Null:
            self.dispose_func(evicted_value)

    def __delitem__(self, key):
        with self.lock:
            value = self._container.pop(key)
        if self.dispose_func:
            self.dispose_func(value)

    def __len__(self):
        with self.lock:
            return len(self._container)

    def __iter__(self):
        raise NotImplementedError('Iteration over this class is unlikely to be threadsafe.')

    def clear(self):
        with self.lock:
            values = list(self._container.values())
            self._container.clear()
        if self.dispose_func:
            for value in values:
                self.dispose_func(value)

    def keys(self):
        with self.lock:
            return self._container.keys()