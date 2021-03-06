# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/salamoia/h2o/decorators/memoize.py
# Compiled at: 2007-12-02 16:26:56


class MWT(object):
    """Memoize With Timeout"""
    __module__ = __name__
    _caches = {}
    _timeouts = {}

    def __init__(self, timeout=2):
        self.timeout = timeout

    def collect(self):
        """Clear cache of results which have timed out"""
        for func in self._caches:
            cache = {}
            for key in self._caches[func]:
                if time.time() - self._caches[func][key][1] < self._timeouts[func]:
                    cache[key] = self._caches[func][key]

            self._caches[func] = cache

    def __call__(self, f):
        self.cache = self._caches[f] = {}
        self._timeouts[f] = self.timeout

        def func(*args, **kwargs):
            kw = kwargs.items()
            kw.sort()
            key = (args, tuple(kw))
            try:
                v = self.cache[key]
                print 'cache'
                if time.time() - v[1] > self.timeout:
                    raise KeyError
            except KeyError:
                print 'new'
                v = self.cache[key] = (f(*args, **kwargs), time.time())

            return v[0]

        func.func_name = f.func_name
        return func


from salamoia.tests import *
runDocTests()