# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\User\AppData\Local\Temp\pip-install-oj_abz_z\hypothesis\hypothesis\internal\intervalsets.py
# Compiled at: 2020-01-12 08:06:33
# Size of source mod 2**32: 2473 bytes


class IntervalSet:

    def __init__(self, intervals):
        self.intervals = tuple(intervals)
        self.offsets = [0]
        for u, v in self.intervals:
            self.offsets.append(self.offsets[(-1)] + v - u + 1)
        else:
            self.size = self.offsets.pop()

    def __len__(self):
        return self.size

    def __iter__(self):
        for u, v in self.intervals:
            (yield from range(u, v + 1))

        if False:
            yield None

    def __getitem__(self, i):
        if i < 0:
            i = self.size + i
        if i < 0 or i >= self.size:
            raise IndexError('Invalid index %d for [0, %d)' % (i, self.size))
        j = len(self.intervals) - 1
        if self.offsets[j] > i:
            hi = j
            lo = 0
            if lo + 1 < hi:
                mid = (lo + hi) // 2
                if self.offsets[mid] <= i:
                    lo = mid
                else:
                    hi = mid
            else:
                j = lo
        t = i - self.offsets[j]
        u, v = self.intervals[j]
        r = u + t
        assert r <= v
        return r

    def __repr__(self):
        return 'IntervalSet(%r)' % (self.intervals,)

    def index(self, value):
        for offset, (u, v) in zip(self.offsets, self.intervals):
            if u == value:
                return offset
            if u > value:
                raise ValueError('%d is not in list' % (value,))
            if value <= v:
                return offset + (value - u)
        else:
            raise ValueError('%d is not in list' % (value,))

    def index_above(self, value):
        for offset, (u, v) in zip(self.offsets, self.intervals):
            if u >= value:
                return offset
            if value <= v:
                return offset + (value - u)
            return self.size