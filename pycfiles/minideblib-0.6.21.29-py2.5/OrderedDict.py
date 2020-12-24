# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-fat/egg/minideblib/OrderedDict.py
# Compiled at: 2007-11-06 15:08:00
from UserDict import UserDict

class OrderedDict(UserDict):
    __order = []

    def __init__(self, dict=None):
        UserDict.__init__(self)
        self.__order = []
        if dict is not None and dict.__class__ is not None:
            self.update(dict)
        return

    def __cmp__(self, dict):
        if isinstance(dict, OrderedDict):
            ret = cmp(self.__order, dict.__order)
            if not ret:
                ret = UserDict.__cmp__(self, dict)
            return ret
        else:
            return UserDict.__cmp__(self, dict)

    def __setitem__(self, key, value):
        if not self.has_key(key):
            self.__order.append(key)
        UserDict.__setitem__(self, key, value)

    def __delitem__(self, key):
        if self.has_key(key):
            del self.__order[self.__order.index(key)]
        UserDict.__delitem__(self, key)

    def clear(self):
        self.__order = []
        UserDict.clear(self)

    def copy(self):
        if self.__class__ is OrderedDict:
            return OrderedDict(self)
        import copy
        return copy.copy(self)

    def keys(self):
        return self.__order

    def items(self):
        return map(lambda x, self=self: (x, self.__getitem__(x)), self.__order)

    def values(self):
        return map(lambda x, self=self: self.__getitem__(x), self.__order)

    def update(self, dict):
        for (k, v) in dict.items():
            self.__setitem__(k, v)