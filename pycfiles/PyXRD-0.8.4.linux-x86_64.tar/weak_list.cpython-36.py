# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.6/dist-packages/mvc/support/collections/weak_list.py
# Compiled at: 2020-03-07 03:51:49
# Size of source mod 2**32: 2651 bytes
import weakref

class WeakList(list):
    __doc__ = '\n        A list subclass referring to its items using weak references if possible \n    '

    def __init__(self, items=list()):
        list.__init__(self)
        tuple(map(self.append, items))

    def get_value(self, item):
        try:
            item = item()
        finally:
            return

        return item

    def make_ref(self, item):
        try:
            item = weakref.ref(item, self.remove)
        finally:
            return

        return item

    def __contains__(self, item):
        return list.__contains__(self, self.make_ref(item))

    def __getitem__(self, key):
        if isinstance(key, slice):
            return type(self)(self.get_value(item) for item in list.__getitem__(self, key))
        else:
            return self.get_value(list.__getitem__(self, key))

    def __getslice__(self, i, j):
        return self.__getitem__(slice(i, j))

    def __setitem__(self, key, item):
        return list.__setitem__(self, key, self.make_ref(item))

    def __iter__(self):
        return iter([self[key] for key in range(len(self))])

    def append(self, item):
        list.append(self, self.make_ref(item))

    def remove(self, item):
        item = self.make_ref(item)
        while list.__contains__(self, item):
            list.remove(self, item)

    def index(self, item):
        return list.index(self, self.make_ref(item))

    def pop(self, item):
        return list.pop(self, self.make_ref(item))