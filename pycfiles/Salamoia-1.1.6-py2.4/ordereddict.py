# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/salamoia/h2o/ordereddict.py
# Compiled at: 2007-12-02 16:26:58
"""

Taken from http://sqlalchemy.org
"""

class OrderedDict(dict):
    """
    A Dictionary that keeps its own internal ordering

    example:

    >>> d = OrderedDict()
    >>> d['4'] = 4
    >>> d['5'] = 5
    >>> d['0'] = 0
    >>> d.keys()
    ['4', '5', '0']
    >>> d.values()
    [4, 5, 0]

    """
    __module__ = __name__

    def __init__(self, values=None):
        self._list = []
        if values is not None:
            for val in values:
                self.update(val)

        return

    def keys(self):
        return list(self._list)

    def clear(self):
        self._list = []
        dict.clear(self)

    def update(self, dict):
        for key in dict.keys():
            self.__setitem__(key, dict[key])

    def setdefault(self, key, value):
        if not self.has_key(key):
            self.__setitem__(key, value)
            return value
        else:
            return self.__getitem__(key)

    def values(self):
        return map(lambda key: self[key], self._list)

    def __iter__(self):
        return iter(self._list)

    def itervalues(self):
        return iter([ self[key] for key in self._list ])

    def iterkeys(self):
        return self.__iter__()

    def iteritems(self):
        return iter([ (key, self[key]) for key in self.keys() ])

    def __delitem__(self, key):
        try:
            del self._list[self._list.index(key)]
        except ValueError:
            raise KeyError(key)

        dict.__delitem__(self, key)

    def __setitem__(self, key, object):
        if not self.has_key(key):
            self._list.append(key)
        dict.__setitem__(self, key, object)

    def __getitem__(self, key):
        return dict.__getitem__(self, key)


from salamoia.tests import *
runDocTests()