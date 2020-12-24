# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.3-fat/egg/Products/GroupUserFolder/DynaList.py
# Compiled at: 2008-05-20 04:51:58
__doc__ = "\nDynaList.py => a list that has dynamic data (ie. calculated by a 'data' method).\nPlease override this class and define a data(self,) method that will return the actual list.\n"
__version__ = '$Revision:  $'
__docformat__ = 'restructuredtext'

class DynaList:
    __module__ = __name__

    def __init__(self, initlist=None):
        pass

    def __repr__(self):
        return repr(self.data())

    def __lt__(self, other):
        return self.data() < self.__cast(other)

    def __le__(self, other):
        return self.data() <= self.__cast(other)

    def __eq__(self, other):
        return self.data() == self.__cast(other)

    def __ne__(self, other):
        return self.data() != self.__cast(other)

    def __gt__(self, other):
        return self.data() > self.__cast(other)

    def __ge__(self, other):
        return self.data() >= self.__cast(other)

    def __cast(self, other):
        if isinstance(other, UserList):
            return other.data()
        else:
            return other

    def __cmp__(self, other):
        raise RuntimeError, 'UserList.__cmp__() is obsolete'

    def __contains__(self, item):
        return item in self.data()

    def __len__(self):
        return len(self.data())

    def __getitem__(self, i):
        return self.data()[i]

    def __setitem__(self, i, item):
        self.data()[i] = item

    def __delitem__(self, i):
        del self.data()[i]

    def __getslice__(self, i, j):
        i = max(i, 0)
        j = max(j, 0)
        return self.__class__(self.data()[i:j])

    def __setslice__(self, i, j, other):
        i = max(i, 0)
        j = max(j, 0)
        if isinstance(other, UserList):
            self.data()[i:j] = other.data()
        elif isinstance(other, type(self.data())):
            self.data()[i:j] = other
        else:
            self.data()[i:j] = list(other)

    def __delslice__(self, i, j):
        i = max(i, 0)
        j = max(j, 0)
        del self.data()[i:j]

    def __add__(self, other):
        if isinstance(other, UserList):
            return self.__class__(self.data() + other.data())
        elif isinstance(other, type(self.data())):
            return self.__class__(self.data() + other)
        else:
            return self.__class__(self.data() + list(other))

    def __radd__(self, other):
        if isinstance(other, UserList):
            return self.__class__(other.data() + self.data())
        elif isinstance(other, type(self.data())):
            return self.__class__(other + self.data())
        else:
            return self.__class__(list(other) + self.data())

    def __iadd__(self, other):
        raise NotImplementedError, 'Not implemented'

    def __mul__(self, n):
        return self.__class__(self.data() * n)

    __rmul__ = __mul__

    def __imul__(self, n):
        raise NotImplementedError, 'Not implemented'

    def append(self, item):
        self.data().append(item)

    def insert(self, i, item):
        self.data().insert(i, item)

    def pop(self, i=-1):
        return self.data().pop(i)

    def remove(self, item):
        self.data().remove(item)

    def count(self, item):
        return self.data().count(item)

    def index(self, item):
        return self.data().index(item)

    def reverse(self):
        self.data().reverse()

    def sort(self, *args):
        apply(self.data().sort, args)

    def extend(self, other):
        if isinstance(other, UserList):
            self.data().extend(other.data())
        else:
            self.data().extend(other)