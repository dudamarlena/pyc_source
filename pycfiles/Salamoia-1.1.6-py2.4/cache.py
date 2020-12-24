# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/salamoia/utility/cache.py
# Compiled at: 2007-12-02 16:26:55


class ObjectCache(object):
    __module__ = __name__

    def __init__(self):
        super(ObjectCache, self).__init__()
        self.ocache = Cache(size=700)
        self.searchCache = Cache(size=1000)

    def invalidateCaches(self):
        self.invalidateCache()
        self.invalidateSearchCache()

    def invalidateCache(self):
        self.ocache.clear()

    def invalidateSearchCache(self):
        self.searchCache.clear()


import UserDict, time

class Cache(UserDict.UserDict):
    """simple cache that uses least recently accessed time to trim size"""
    __module__ = __name__

    def __init__(self, data=None, size=100):
        UserDict.UserDict.__init__(self, data)
        self.size = size

    def resize(self):
        """trim cache to no more than 95% of desired size"""
        trim = max(0, int(len(self.data) - 0.95 * self.size))
        if trim:
            values = map(None, self.data.values(), self.data.keys())
            values.sort()
            for (val, k) in values[0:trim]:
                del self.data[k]

        return

    def __setitem__(self, key, val):
        if not self.data.has_key(key) and len(self.data) >= self.size:
            self.resize()
        self.data[key] = (
         time.time(), val)

    def __getitem__(self, key):
        """like normal __getitem__ but updates time of fetched entry"""
        val = self.data[key][1]
        self.data[key] = (time.time(), val)
        return val

    def get(self, key, default=None):
        """like normal __getitem__ but updates time of fetched entry"""
        try:
            return self[key]
        except KeyError:
            return default

    def values(self):
        """return values, but eliminate access times first"""
        vals = list(self.data.values())
        for i in range(len(vals)):
            vals[i] = vals[i][1]

        return tuple(vals)

    def items(self):
        return map(None, self.keys(), self.values())

    def copy(self):
        return self.__class__(self.data, self.size)

    def update(self, dict):
        for k in dict.keys():
            self[k] = dict[k]


def _test(size=100):
    c = Cache(size=size)
    for i in range(120):
        c[i] = i
        if i > 5:
            x = c[5]
        time.sleep(0.01)

    x = c.keys()
    x.sort()
    assert x == [5] + range(21, 120), x
    c.update({1: 1})
    x = c.keys()
    x.sort()
    assert x == [1, 5] + range(26, 120), x
    print 'all cache tests passed'


if __name__ == '__main__':
    _test()
from salamoia.tests import *
runDocTests()