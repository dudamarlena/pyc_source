# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.9-intel/egg/cpip/util/StrTree.py
# Compiled at: 2017-10-03 13:07:16
__doc__ = 'Treats a string as a tree.'
__author__ = 'Paul Ross'
__date__ = '2011-07-10'
__rights__ = 'Copyright (c) 2008-2017 Paul Ross'

class StrTree(object):
    """Initialise the class with a optional list of strings."""

    def __init__(self, theIterable=None):
        """Initialise the class with a optional list of strings."""
        self._ir = {}
        self._b = False
        if theIterable is not None:
            for aS in theIterable:
                self.add(aS)

        return

    def __str__(self):
        return ('\n').join(self._str(0))

    def _str(self, d):
        p = ' ' * d
        sL = ['%s%s %d' % (p, self._b, d)]
        kS = self._ir.keys()
        for k in kS:
            sL.append('%s"%s"' % (p, k))
            sL.extend(self._ir[k]._str(d + 1))

        return sL

    def add(self, s):
        """Add a string."""
        if s:
            if s[0] not in self._ir:
                self._ir[s[0]] = StrTree()
            self._ir[s[0]].add(s[1:])
        else:
            self._b = True

    def has(self, s, i=0):
        """Returns the index of the end of s that match a complete word
        in the tree. i.e. [i:return_value] is in the dictionary.
        Note IndexError and KeyError are trapped here."""
        assert i >= 0
        try:
            myI = self._ir[s[i]].has(s, i + 1)
            if myI > 0:
                return myI
            if self._b:
                return i
        except (IndexError, KeyError):
            if self._b:
                return i

        return 0

    def values(self):
        """Returns all values."""
        return self._values([])

    def _values(self, l):
        r = []
        if self._b:
            r.append(('').join(l))
        for k in self._ir.keys():
            l.append(k)
            r.extend(self._ir[k]._values(l))
            l.pop()

        return r