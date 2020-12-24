# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ddalg/itree/_node.py
# Compiled at: 2020-03-30 11:18:59
# Size of source mod 2**32: 6316 bytes
import numbers, statistics, typing
from collections import OrderedDict, defaultdict
from ddalg.model import Interval

class IntervalNode:

    def __init__(self, intervals: typing.List[Interval], parent=None):
        """
        Create a node from given intervals.
        :param intervals: list with intervals
        """
        self.intervals = OrderedDict()
        self.parent = parent
        self.left = None
        self.right = None
        if len(intervals) == 0:
            return
        self._center = statistics.median(get_coordinates(intervals))
        inner = defaultdict(list)
        left, right = [], []
        for interval in intervals:
            if interval.end < self._center:
                left.append(interval)
            else:
                if interval.begin >= self._center:
                    right.append(interval)
                else:
                    inner[interval].append(interval)

        for interval in sorted(inner.keys()):
            self.intervals[interval] = []
            for item in inner[interval]:
                self.intervals[interval].append(item)

        if left:
            self.left = IntervalNode(left, parent=self)
        if right:
            self.right = IntervalNode(right, parent=self)

    def search(self, position: numbers.Number) -> typing.List[Interval]:
        """
        Return intervals that overlap with given `position`.
        :param position: 1-based numeric position
        :return: list of overlapping intervals
        """
        if not isinstance(position, numbers.Number):
            raise ValueError('Expected a number but `{}` is `{}`'.format(position, type(position)))
        results = []
        if not self.intervals:
            return results
        else:
            for entry in self.intervals:
                if entry.contains(position):
                    for item in self.intervals[entry]:
                        results.append(item)

                elif entry.begin > position:
                    break

            if position < self._center:
                if self.left:
                    for item in self.left.search(position):
                        results.append(item)

            if position >= self._center:
                if self.right:
                    for item in self.right.search(position):
                        results.append(item)

            return results

    def get_overlaps(self, begin: numbers.Number, end: numbers.Number) -> typing.List[Interval]:
        """
        Return intervals that overlap with given `begin` and `end` coordinates.
        :param begin: 0-based (excluded) begin coordinate
        :param end: 0-based (included) end coordinate
        :return: list of overlapping intervals
        """
        results = []
        if not self.intervals:
            return results
        else:
            for entry in self.intervals:
                if entry.intersects(begin, end):
                    for item in self.intervals[entry]:
                        results.append(item)

                elif entry.begin >= end:
                    break

            if begin <= self._center:
                if self.left:
                    for item in self.left.get_overlaps(begin, end):
                        results.append(item)

            if end > self._center:
                if self.right:
                    for item in self.right.get_overlaps(begin, end):
                        results.append(item)

            return results

    def min_value(self):
        return next(iter(self.intervals))

    def max_value(self):
        return next(reversed(self.intervals))

    def minimum(self):
        node = self
        while node.left:
            node = node.left

        return node

    def maximum(self):
        node = self
        while node.right:
            node = node.right

        return node

    def __eq__(self, other):
        return self.intervals == other.intervals and self.left == other.left and self.right == other.right

    def __len__(self):
        if self.intervals:
            return len(self.intervals)
        else:
            return 0

    def __repr__(self):
        intstr = ','.join([str(key) for key in self.intervals.keys()])
        return 'ITNode(intervals=[{}])'.format(intstr)


def get_coordinates(items: typing.Iterable[Interval]):
    results = set()
    for item in items:
        results.add(item.begin)
        results.add(item.end)

    return results