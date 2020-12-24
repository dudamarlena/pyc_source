# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.6/dist-packages/nosyd/cache.py
# Compiled at: 2009-10-08 08:45:51
import time

class MWT(object):
    """Memoize With Timeout"""
    _caches = {}
    _timeouts = {}

    def __init__(self, timeout=2, cache_attr_name=None):
        self.timeout = timeout
        self.cache_attr_name = cache_attr_name
        self.cache = None
        return

    def collect(self):
        """Clear cache of results which have timed out"""
        for func in self._caches:
            cache = {}
            for key in self._caches[func]:
                if time.time() - self._caches[func][key][1] < self._timeouts[func]:
                    cache[key] = self._caches[func][key]

            self._caches[func].clear()
            self._caches[func].update(cache)

    def init_cache(self, f, args, kwargs):
        if self.cache_attr_name == None:
            self.cache = self._caches[f] = {}
        else:
            try:
                the_self = args[0]
                self.cache = getattr(the_self, self.cache_attr_name)
                self._caches[f] = self.cache
            except (IndexError, AttributeError):
                raise TypeError("MWT could not retrieve cache attribute '%s' for function %r" % (
                 self.cache_attr_name, f.func_name))

            return

    def __call__(self, f):
        self._timeouts[f] = self.timeout

        def func(*args, **kwargs):
            if self.cache == None:
                self.init_cache(f, args, kwargs)
            kw = kwargs.items()
            kw.sort()
            key = (args, tuple(kw))
            try:
                v = self.cache[key]
                if time.time() - v[1] > self.timeout:
                    raise KeyError
            except KeyError:
                v = self.cache[key] = (
                 f(*args, **kwargs), time.time())

            return v[0]

        func.func_name = f.func_name
        return func