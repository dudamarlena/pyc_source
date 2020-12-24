# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ddalg/model/_interval.py
# Compiled at: 2020-03-30 11:18:59
# Size of source mod 2**32: 1114 bytes
import abc

class Interval(metaclass=abc.ABCMeta):
    __doc__ = 'Class to be subclassed in order to play with IntervalTree.'

    @property
    @abc.abstractmethod
    def begin(self):
        pass

    @property
    @abc.abstractmethod
    def end(self):
        pass

    def contains(self, value) -> bool:
        return self.end >= value > self.begin

    def intersects(self, begin, end):
        return end > self.begin and begin < self.end

    def intersection(self, other):
        if self.end <= other.begin or other.end <= self.begin:
            return 0
        else:
            return max(min(self.end, other.end) - max(self.begin, other.begin), 1)

    def __lt__(self, other):
        if self.begin != other.begin:
            return self.begin < other.begin
        else:
            return self.end < other.end

    def __len__(self):
        return self.end - self.begin

    def __eq__(self, other):
        return self.begin == other.begin and self.end == other.end

    def __repr__(self):
        return '({},{})'.format(self.begin, self.end)

    def __hash__(self):
        return hash((self.begin, self.end))