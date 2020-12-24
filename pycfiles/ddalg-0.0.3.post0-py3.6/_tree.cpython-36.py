# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ddalg/itree/_tree.py
# Compiled at: 2020-03-30 11:18:59
# Size of source mod 2**32: 7123 bytes
import logging, numbers, typing
from collections import deque
from deprecation import deprecated
from ddalg import __version__
from ddalg.metrics.interval import get_boundary_margin, jaccard_coefficient
from ddalg.model import Interval
from ._node import IntervalNode

class IntervalTree:

    def __init__(self, intervals: typing.List[Interval]):
        self._head = IntervalNode(intervals)
        self._intervals = intervals
        self._in_sync = True
        self._size = len(intervals)
        self._logger = logging.getLogger(__name__)

    def build(self):
        if not self._in_sync:
            self._head = IntervalNode(self._intervals)
            self._in_sync = True
            self._size = len(self._intervals)

    def insert(self, interval: Interval):
        """
        Insert interval into the tree. The insert results in invalidation of the tree leading to lazy rebuild of
        the tree structure upon the next query.
        :param interval: interval to be inserted
        :return: None
        """
        self._intervals.append(interval)
        self._in_sync = False

    def search(self, position: numbers.Number) -> typing.List[Interval]:
        """
        Return intervals that overlap with given `position`.
        :param position: 1-based numeric position
        :return: list of overlapping intervals
        """
        self.build()
        return self._head.search(position)

    def get_overlaps(self, begin, end) -> typing.List[Interval]:
        """
        Get intervals that overlap with given query coordinates.
        :param begin: 0-based (excluded) begin position of query
        :param end: 0-based (included) end position of query
        :return: list (not necessarily sorted) with intervals overlapping with query coordinates
        """
        self.build()
        return self._head.get_overlaps(begin, end)

    @deprecated(deprecated_in='0.0.3', removed_in='0.0.5', current_version=__version__, details='Get all overlapping intervals using `get_overlaps` and then remove using methods from `ddalg.metrics.interval` module.')
    def fuzzy_query(self, begin, end, coverage=1.0) -> typing.List[Interval]:
        """
        Get intervals that imperfectly overlap with given query coordinates, while covering at least `coverage` of
        the query.
        :param begin: 0-based (excluded) begin position of query
        :param end: 0-based (included) end position of query
        :param coverage: float in [0,1] specifying what fraction of query the interval needs to overlap with
        :return: list of overlapping intervals
        """
        if 0 < coverage > 1:
            raise ValueError('coverage must be within [0,1]')
        self.build()
        margin = get_boundary_margin(begin, end, coverage)
        dist_begin, dist_end = begin - margin, end + margin
        prox_begin, prox_end = begin + margin, end - margin
        self._logger.debug('Returning intervals [{}+-{:.2f}, {}+-{:.2f}]'.format(begin, margin, end, margin))
        return [interval for interval in self.get_overlaps(begin, end) if dist_begin <= interval.begin <= prox_begin if dist_end >= interval.end >= prox_end]

    @deprecated(deprecated_in='0.0.3', removed_in='0.0.5', current_version=__version__, details='Get all overlapping intervals using `get_overlaps` and then remove using methods from `ddalg.metrics.interval` module.')
    def jaccard_query(self, begin, end, min_jaccard=1.0):
        """
        Get intervals that imperfectly overlap with given query coordinates, while covering at least `coverage` of
        the query.
        :param begin: 0-based (excluded) begin position of query
        :param end: 0-based (included) end position of query
        :param min_jaccard: float in [0,1] specifying what fraction of query the interval needs to overlap with
        :return: list of overlapping intervals
        """
        if 0 < min_jaccard > 1:
            raise ValueError('min_jaccard must be within [0,1]')
        self.build()
        return [interval for interval in self.get_overlaps(begin, end) if jaccard_coefficient(interval, SimpleInterval.of(begin, end)) >= min_jaccard]

    def __len__(self):
        self.build()
        return self._size

    def __repr__(self):
        return 'IntervalTree(size={})'.format(len(self))

    def __iter__(self):
        self.build()
        return IntervalTreeIterator(self._head)

    def __bool__(self):
        return len(self) != 0


class IntervalTreeIterator:

    def __init__(self, root):
        self.initialized = False
        self.root = root
        self.node = None
        self.queue = None

    def has_next(self):
        if not self.initialized:
            if self.root:
                self.node = self.root.minimum()
                self.queue = self.node_to_queue(self.node)
                self.initialized = True
            else:
                return False
        if self.queue:
            return True
        else:
            self.node = self.successor(self.node)
            self.queue = self.node_to_queue(self.node)
            return len(self.queue) != 0

    def __next__(self):
        if self.has_next():
            return self.queue.popleft()
        raise StopIteration()

    @staticmethod
    def node_to_queue(node: IntervalNode) -> deque:
        queue = deque()
        if node:
            for interval in node.intervals:
                for item in node.intervals[interval]:
                    queue.append(item)

        return queue

    @staticmethod
    def successor(node: IntervalNode):
        if node.right:
            return node.right.minimum()
        else:
            y = node.parent
            while y and node == y.right:
                node = y
                y = y.parent

            return y


class SimpleInterval(Interval):
    __doc__ = 'Simple interval implementation for internal usage within the module.'

    def __init__(self, begin: int, end: int):
        self._begin = begin
        self._end = end

    @classmethod
    def of(cls, begin, end):
        return cls(begin, end)

    @property
    def begin(self):
        return self._begin

    @property
    def end(self):
        return self._end