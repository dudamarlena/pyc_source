# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pdfs/Cache.py
# Compiled at: 2017-08-14 16:20:11
# Size of source mod 2**32: 1239 bytes
import pickle, time
from .Bases import Singleton
from .TermOutput import msg

class RequestCache(metaclass=Singleton):

    def __init__(self, cacheFile=None):
        self.cacheFile = cacheFile
        try:
            self.cache = pickle.load(open(self.cacheFile, 'rb'))
        except FileNotFoundError:
            msg.info('Started new request cache')
            self.cache = {}

    def writeCacheFile(self):
        pickle.dump(self.cache, open(self.cacheFile, 'wb'))


def cachedRequest(name=None):

    def _cachedRequest(fn):

        def wrapper(*args, **kwargs):
            rc = RequestCache()
            if name not in rc.cache:
                rc.cache[name] = dict()
            else:
                cache = rc.cache[name]
                if 'cache_key' in kwargs:
                    if kwargs['cache_key'] is None:
                        raise RuntimeError('cache_key required')
                    x = kwargs['cache_key']
                else:
                    x = args[0]
            if x not in cache:
                msg.debug('%s cache miss', name)
                time.sleep(0.4)
                cache[x] = fn(*args, **kwargs)
                rc.writeCacheFile()
            return cache[x]

        return wrapper

    return _cachedRequest