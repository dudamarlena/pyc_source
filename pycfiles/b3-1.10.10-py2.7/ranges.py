# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\b3\plugins\netblocker\netblock\ranges.py
# Compiled at: 2016-03-08 18:42:10
"""Sets of (ranges of) integer numbers.

This module exports the Ranges class and the BadRange exception."""
from __future__ import generators
__all__ = [
 'BadRange', 'Ranges']

class BadRange(Exception):
    """Raised if there is some problem with ranges.
        (Yes, this is non-specific.)"""
    pass


class Ranges:
    """Represent a set of integer ranges.

        Ranges represent a set of ranges of numbers. A new range
        or a list of them may be added to or deleted from the set.
        Adjacent ranges are merged in the set to create the minimal
        set of ranges necessary to cover all included numbers.

        Range sets support addition and subtraction operations.
        Eg: Ranges(1,10) + Ranges(2,30) + Ranges(50,60) - Ranges(14,28)"""

    def __init__(self, *args):
        """Optional START,END arguments become the initial range."""
        self._l = []
        if len(args) not in (0, 2):
            raise TypeError('Ranges() takes either 0 or 2 arguments.')
        if args:
            self._good(args[0], args[1])
            self._l.append([args[0], args[1]])

    def _good(self, start, end):
        if start > end:
            raise BadRange('start > end')

    def _rel(self, val):
        return val

    def _rrange(self, r):
        if r[0] == r[1]:
            return str(self._rel(r[0]))
        else:
            return '%s-%s' % (self._rel(r[0]), self._rel(r[1]))

    def __str__(self):
        return '<Ranges: %s>' % ((' ').join(map(self._rrange, self._l)),)

    def _find(self, start):
        lo = 0
        hi = len(self._l)
        while lo < hi:
            mid = (lo + hi) // 2
            if self._l[mid][0] < start:
                lo = mid + 1
            else:
                hi = mid

        return lo

    def _isprev(self, i):
        return not i == 0

    def _prev(self, i):
        return self._l[(i - 1)]

    def addnum(self, val):
        """Add VALUE to the set."""
        self.addrange(val, val)

    def delnum(self, val):
        """Remove VALUE from the set."""
        self.delrange(val, val)

    def addrange(self, start, end):
        """And a range from START to END to the set."""
        self._good(start, end)
        i = self._find(start)
        if i == len(self._l):
            self._l.append([start, end])
        else:
            r = self._l[i]
            if start >= r[0] and end <= r[1]:
                return
            self._l.insert(i, [start, end])
        i = max(i, 1)
        while i < len(self._l):
            ro = self._l[(i - 1)]
            r = self._l[i]
            if r[0] - 1 <= ro[1]:
                ro[1] = max(r[1], ro[1])
                del self._l[i]
            elif r[0] == start and r[1] == end:
                i = i + 1
            else:
                break

    def delrange(self, start, end):
        """Remove the range START to END from the set."""
        self._good(start, end)
        i = self._find(start)
        if self._isprev(i) and start <= self._prev(i)[1]:
            r = self._prev(i)
            oe = r[1]
            r[1] = start - 1
            if end < oe:
                self._l.insert(i, [end + 1, oe])
        while i < len(self._l):
            r = self._l[i]
            if r[0] > end:
                break
            if r[1] <= end:
                del self._l[i]
            else:
                r[0] = end + 1

    def addlist(self, l):
        """Add a list of [start,end] ranges to the set."""
        for s, e in l:
            self.addrange(s, e)

    def dellist(self, l):
        """Remove a list of [start,end] ranges from the set."""
        for s, e in l:
            self.delrange(s, e)

    def addRanges(self, rng):
        for s, e in rng._l:
            self.addrange(s, e)

    def delRanges(self, rng):
        for s, e in rng._l:
            self.delrange(s, e)

    def __contains__(self, val):
        """Is VAL a point in the set of ranges?"""
        if len(self._l) <= 4:
            for r in self._l:
                if r[0] <= val <= r[1]:
                    return 1

            return 0
        p = self._find(val)
        pm = p - 1
        return p < len(self._l) and self._l[p][0] <= val <= self._l[p][1] or pm >= 0 and self._l[pm][0] <= val <= self._l[pm][1]

    def copy(self):
        """Return a new object that is a copy of this set of ranges."""
        n = self.__class__()
        for s, e in self._l:
            n._l.append([s, e])

        return n

    def __add__(self, other):
        n = self.copy()
        for s, e in other._l:
            n.addrange(s, e)

        return n

    def __sub__(self, other):
        n = self.copy()
        for s, e in other._l:
            n.delrange(s, e)

        return n

    def __eq__(self, other):
        if len(other._l) != len(self._l):
            return 0
        for i in xrange(0, len(self._l)):
            if self._l[i] != other._l[i]:
                return 0

        return 1

    def subset(self, other):
        """Return True if other is a subset of this set of ranges."""
        i = 0
        myl = self._l
        j = 0
        otl = other._l
        while i < len(myl) and j < len(otl):
            if otl[j][0] >= myl[i][0] and otl[j][1] <= myl[i][1]:
                j += 1
            elif otl[j][0] > myl[i][1]:
                i += 1
            else:
                return 0

        return j == len(otl)

    def intersect(self, other):
        """Returns True if another set of ranges intersects us."""

        def _overlap(t1, t2):
            low1, hi1 = t1
            low2, hi2 = t2
            return low2 <= low1 <= hi2 or low2 <= hi1 <= hi2 or low1 <= low2 <= hi1 or low1 <= hi2 <= hi1

        i = 0
        myl = self._l
        j = 0
        otl = other._l
        while i < len(myl) and j < len(otl):
            if _overlap(myl[i], otl[j]):
                return 1
            if myl[i][1] < otl[j][0]:
                i += 1
            else:
                j += 1

        return 0

    def adjacent(self, other):
        """Return True if we are adjacent to another range."""
        if len(self._l) == 0 or len(other._l) == 0:
            return 0
        return self._l[(-1)][1] + 1 == other._l[0][0] or self._l[0][0] == other._l[(-1)][1] + 1

    def len(self):
        """The length of a set of ranges is the number of elements
                that it contains."""
        return reduce(lambda x, y: x + y[1] - y[0] + 1, self._l, 0)

    def __len__(self):
        """Due to technical limitations of CPython, you should
                use Ranges.len() instead of len(Ranges)."""
        return int(self.len())

    def __nonzero__(self):
        return len(self._l) > 0

    def __cmp__(self, other):
        """Any comparison between Ranges other than for inequality or
                equality has undefined results."""
        if self.__eq__(other):
            return 0
        return 1

    def __iter__(self):
        """Yields every number in the set of ranges."""
        for rng in self._l:
            i = rng[0]
            while i <= rng[1]:
                yield self._rel(i)
                i += 1