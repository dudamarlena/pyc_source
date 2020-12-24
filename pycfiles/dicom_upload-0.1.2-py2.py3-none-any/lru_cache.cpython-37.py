# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.12-x86_64/egg/dicom_tools/pyqtgraph/util/lru_cache.py
# Compiled at: 2018-05-21 04:28:19
# Size of source mod 2**32: 4264 bytes
import operator, sys, itertools
_IS_PY3 = sys.version_info[0] == 3

class LRUCache(object):
    """LRUCache"""

    def __init__(self, maxSize=100, resizeTo=70):
        """
        ============== =========================================================
        **Arguments:**
        maxSize        (int) This is the maximum size of the cache. When some 
                       item is added and the cache would become bigger than 
                       this, it's resized to the value passed on resizeTo.
        resizeTo       (int) When a resize operation happens, this is the size 
                       of the final cache.
        ============== =========================================================
        """
        if not resizeTo < maxSize:
            raise AssertionError
        else:
            self.maxSize = maxSize
            self.resizeTo = resizeTo
            self._counter = 0
            self._dict = {}
            if _IS_PY3:
                self._nextTime = itertools.count(0).__next__
            else:
                self._nextTime = itertools.count(0).next

    def __getitem__(self, key):
        item = self._dict[key]
        item[2] = self._nextTime()
        return item[1]

    def __len__(self):
        return len(self._dict)

    def __setitem__(self, key, value):
        item = self._dict.get(key)
        if item is None:
            if len(self._dict) + 1 > self.maxSize:
                self._resizeTo()
            item = [key, value, self._nextTime()]
            self._dict[key] = item
        else:
            item[1] = value
            item[2] = self._nextTime()

    def __delitem__(self, key):
        del self._dict[key]

    def get(self, key, default=None):
        try:
            return self[key]
        except KeyError:
            return default

    def clear(self):
        self._dict.clear()

    if _IS_PY3:

        def values(self):
            return [i[1] for i in self._dict.values()]

        def keys(self):
            return [x[0] for x in self._dict.values()]

        def _resizeTo(self):
            ordered = sorted((self._dict.values()), key=(operator.itemgetter(2)))[:self.resizeTo]
            for i in ordered:
                del self._dict[i[0]]

        def iteritems(self, accessTime=False):
            """
            :param bool accessTime:
                If True sorts the returned items by the internal access time.
            """
            if accessTime:
                for x in sorted((self._dict.values()), key=(operator.itemgetter(2))):
                    yield (
                     x[0], x[1])

            else:
                for x in self._dict.items():
                    yield (
                     x[0], x[1])

    else:

        def values(self):
            return [i[1] for i in self._dict.itervalues()]

        def keys(self):
            return [x[0] for x in self._dict.itervalues()]

        def _resizeTo(self):
            ordered = sorted((self._dict.itervalues()), key=(operator.itemgetter(2)))[:self.resizeTo]
            for i in ordered:
                del self._dict[i[0]]

        def iteritems(self, accessTime=False):
            """
            ============= ======================================================
            **Arguments**
            accessTime    (bool) If True sorts the returned items by the 
                          internal access time.
            ============= ======================================================
            """
            if accessTime:
                for x in sorted((self._dict.itervalues()), key=(operator.itemgetter(2))):
                    yield (
                     x[0], x[1])

            else:
                for x in self._dict.iteritems():
                    yield (
                     x[0], x[1])