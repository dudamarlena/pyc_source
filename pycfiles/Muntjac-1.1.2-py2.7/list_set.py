# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/muntjac/data/util/list_set.py
# Compiled at: 2013-04-04 15:36:37
"""ListSet is an internal Muntjac class which implements a combination of
a list and a set."""

class ListSet(list):
    """ListSet is an internal Muntjac class which implements a combination of
    a List and a Set. The main purpose of this class is to provide a list with
    a fast L{contains} method. Each inserted object must by unique (as
    specified by L{equals}). The L{set} method allows duplicates because of
    the way L{sort} works.

    This class is subject to change and should not be used outside Muntjac
    core.
    """

    def __init__(self, *args):
        self._itemSet = None
        self._duplicates = dict()
        nargs = len(args)
        if nargs == 0:
            super(ListSet, self).__init__()
            self._itemSet = set()
        elif nargs == 1:
            if isinstance(args[0], int):
                initialCapacity, = args
                super(ListSet, self).__init__()
                self._itemSet = set()
            else:
                c, = args
                super(ListSet, self).__init__(c)
                self._itemSet = set()
                self._itemSet = self._itemSet.union(c)
        else:
            raise ValueError, 'too many arguments'
        return

    def contains(self, o):
        return o in self._itemSet

    def __contains__(self, item):
        return self.contains(item)

    def containsAll(self, c):
        for cc in c:
            if cc not in self._itemSet:
                return False
        else:
            return True

    def append(self, val):
        return self.add(val)

    def insert(self, idx, val):
        return self.add(idx, val)

    def add(self, *args):
        """Works as list.append or list.insert but returns
        immediately if the element is already in the ListSet.
        """
        nargs = len(args)
        if nargs == 1:
            e, = args
            if self.contains(e):
                return False
            if not super(ListSet, self).__contains__(e):
                super(ListSet, self).append(e)
                self._itemSet.add(e)
                return True
            return False
        elif nargs == 2:
            index, element = args
            if self.contains(element):
                return
            super(ListSet, self).insert(index, element)
            self._itemSet.add(element)
        else:
            raise ValueError, 'invalid number of arguments'

    def extend(self, iterable):
        return self.addAll(iterable)

    def addAll(self, *args):
        nargs = len(args)
        if nargs == 1:
            c, = args
            modified = False
            for e in c:
                if self.contains(e):
                    continue
                if self.add(e):
                    self._itemSet.add(e)
                    modified = True

            return modified
        if nargs == 2:
            index, c = args
            modified = False
            for e in c:
                if self.contains(e):
                    continue
                self.add(index, e)
                index += 1
                self._itemSet.add(e)
                modified = True

            return modified
        raise ValueError, 'invalid number of arguments'

    def clear(self):
        del self[:]
        self._itemSet.clear()

    def index(self, val):
        return self.indexOf(val)

    def indexOf(self, o):
        if not self.contains(o):
            return -1
        return super(ListSet, self).index(o)

    def lastIndexOf(self, o):
        if not self.contains(o):
            return -1
        return self[::-1].index(o)

    def remove(self, o):
        if isinstance(o, int):
            index = o
            e = super(ListSet, self).pop(index)
            if e is not None:
                self._itemSet.remove(e)
            return e
        if super(ListSet, self).remove(o):
            self._itemSet.remove(o)
            return True
        else:
            return False
            return

    def removeRange(self, fromIndex, toIndex):
        toRemove = set()
        for idx in range(fromIndex, toIndex):
            toRemove.add(self[idx])

        del self[fromIndex:toIndex]
        for r in toRemove:
            self._itemSet.remove(r)

    def set(self, index, element):
        if element in self:
            if self[index] == element:
                return element
            self.addDuplicate(element)
        old = self[index] = element
        self.removeFromSet(old)
        self._itemSet.add(element)
        return old

    def removeFromSet(self, e):
        """Removes "e" from the set if it no longer exists in the list.
        """
        dupl = self._duplicates.get(e)
        if dupl is not None:
            if dupl == 1:
                del self._duplicates[e]
            else:
                self._duplicates[e] = dupl - 1
        else:
            self._itemSet.remove(e)
        return

    def addDuplicate(self, element):
        """Marks the "element" can be found more than once from the list.
        Allowed in L{set} to make sorting work.
        """
        nr = self._duplicates.get(element)
        if nr is None:
            nr = 1
        else:
            nr += 1
        self._duplicates[element] = nr
        return

    def clone(self):
        v = ListSet(self[:])
        v._itemSet = set(self._itemSet)
        return v