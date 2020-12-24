# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/pocoo/utils/cache.py
# Compiled at: 2006-12-26 17:18:07
__doc__ = '\n    pocoo.utils.cache\n    ~~~~~~~~~~~~~~~~~\n\n    Provides a very simple caching system for persistent processes.\n\n    **This is currently unused and untested.**\n\n    :copyright: 2006 by Armin Ronacher, Georg Brandl.\n    :license: GNU GPL, see LICENSE for more details.\n'
import copy, time
from pocoo.exceptions import PocooRuntimeError

class Cache(object):
    """
    A simple memory caching system.

    Usage example::

        >>> from pocoo.utils.cache import Cache
        >>> memcache = Cache()
        >>> memcache.dump('test', 'Hello World', 5)
        >>> memcache.fetch('test')
        'Hello World'
        >>> memcache.fetch('test')
        'Hello World'
        >>> memcache.fetch('test')
        'Hello World'
        >>> memcache.fetch('test')
        >>> memcache.expired('test')
        True
        >>> memcache['blub'] = 'Test'
        >>> memcache['blub']
        'Test'
        >>> memcache['blub', 2] = 'Spam'
        >>> memcache['blub']
        'Spam'
        >>> memcache.expired('blub')
        True
    """
    __module__ = __name__

    def __init__(self, autoprune):
        self._cache = {}
        self.autoprune = autoprune

    def __repr__(self):
        d = {}
        for key in self._cache:
            if not self.expired(key):
                d[key] = self.fetch(key)

        return '<Cache %r - caching %d items, %d expired>' % (d, len(d), len(self._cache) - len(d))

    def dump(self, key, obj, expires=360):
        if expires > -1:
            expires = time.time() + expires
        self._cache[key] = (
         copy.copy(obj), expires)

    def fetch(self, key, default=None):
        if self.autoprune:
            self.prune()
        if not self.expired(key):
            return self._cache[key][0]
        return default

    def remove(self, key):
        if key in self._cache:
            del self._cache[key]

    def prune(self):
        ncache = {}
        for key in self._cache:
            if not self.expired(key):
                ncache[key] = self._cache[key]

        self._cache = ncache

    def expired(self, key):
        if key not in self._cache:
            return True
        if self._cache[key][1] < 0:
            return False
        return self._cache[key][1] < time.time()

    def new(self, key):
        return key not in self._cache

    def __contains__(self, key):
        return not self.expired(key)

    def __getitem__(self, item):
        return self.fetch(item)

    def __setitem__(self, item, value):
        if isinstance(item, tuple):
            (key, expires) = item
        elif isinstance(item, str):
            key = item
            expires = -1
        else:
            raise PocooRuntimeError('string expected')
        self.dump(key, value, expires)