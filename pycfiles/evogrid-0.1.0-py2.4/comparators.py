# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/evogrid/sharing/comparators.py
# Compiled at: 2006-07-30 05:24:47
"""Sharing aware pools
"""
from zope.component import adapts
from zope.interface import implements, implementer
from evogrid.caching.interfaces import ICache
from evogrid.caching.ram import RAMCache
from evogrid.common.comparators import SimpleComparator
from evogrid.interfaces import IPool, IComparator
from evogrid.sharing.interfaces import ISharingAwareComparator, IDistance
_marker = object()

@implementer(IDistance)
def one_dim_distance(a, b):
    """Default dummy distance measure between two numericals

    Can get overridden by the constructor.
    """
    return abs(b - a)


class SharingAwareComparator(object):
    """Base adapter to use a pool as sharing context to build a
    SharingAwareComparator instance

    Can also adapt an existing comparator (instead of the default
    SimpleComparator instance).

    No memoization by default, this comparator can use RAM or
    memcached based memoization for better efficiency for the ``distance``
    method.
    """
    __module__ = __name__
    implements(ISharingAwareComparator)
    adapts(IPool, IComparator)

    def __init__(self, pool, comparator=None, distance=None, cache=None):
        """Build a sharing aware comparator

        Take a pool as sharing context
        """
        self._pool = pool
        if distance is None:
            distance = one_dim_distance
        if cache is not None:
            distance = MemoizedDistance(distance, cache)
        self._distance = distance
        if comparator is None:
            comparator = SimpleComparator()
        self._comparator = comparator
        return

    def distance(self, rep1, rep2):
        """Compute the distance between two replicators
        """
        return self._distance(rep1.candidate_solution, rep2.candidate_solution)

    def share_evaluation(self, rep, context=None):
        """Simple shared evaluation

        Compute the average distance and multiply it by the original
        evaluation.
        """
        if context is None:
            context = self._pool
        if len(context) <= 1:
            return rep.evaluation
        sum = 0.0
        for rep2 in context:
            sum += self.distance(rep, rep2)

        return rep.evaluation * sum / (len(context) - 1)

    def _share(self, replicators):
        """Build copies of replicators with shared evaluations"""
        context = set(self._pool) - set(replicators)
        for rep in replicators:
            shared = rep.replicate()
            shared.evaluation = self.share_evaluation(rep, context=context)
            shared._original_replicator = rep
            yield shared

    def cmp(self, rep1, rep2):
        """Compare copies of rep1 and rep2 whose evaluations got shared"""
        (shared1, shared2) = self._share((rep1, rep2))
        return self._comparator.cmp(shared1, shared2)

    def max(self, replicators):
        """Apply the `max` method to shared copies of replicators"""
        max_shared = self._comparator.max(self._share(replicators))
        return max_shared._original_replicator


class MemoizedDistance(object):
    """Base implementation of a memoize wrapper"""
    __module__ = __name__
    implements(IDistance)
    adapts(IDistance, ICache)

    def __init__(self, distance, cache=None):
        self._distance = distance
        if cache is None:
            cache = RAMCache(max_entries=100)
        self._cache = cache
        self._key_common = {'function': distance.__name__}
        return

    def __call__(self, x1, x2):
        key = self._key_common.copy()
        key['args'] = tuple(sorted((x1, x2)))
        result = self._cache.query(key, _marker)
        if result is _marker:
            result = self._distance(x1, x2)
            self._cache.set(key, result)
        return result