# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/evogrid/common/pools.py
# Compiled at: 2006-08-16 19:12:25
"""Default pools implementations
"""
from itertools import chain
from zope.interface import implements
from zope.component import adapts
from pprint import PrettyPrinter
from evogrid.common.comparators import SimpleComparator
from evogrid.interfaces import IPool, IComparator, IProvider
pformat = PrettyPrinter(width=74).pformat

class Pool(set):
    """Simple set based pool implementation"""
    __module__ = __name__
    implements(IPool)

    def remove(self, replicator):
        try:
            return set.remove(self, replicator)
        except KeyError, e:
            raise ValueError(e)

    def pop(self):
        try:
            return set.pop(self)
        except KeyError, e:
            raise ValueError(e)

    def __repr__(self):
        return 'Pool(%s)' % pformat(list(self))


class OrderedPool(list):
    """Simple list based pool implementation"""
    __module__ = __name__
    implements(IPool)
    add = list.append

    def clear(self):
        del self[:]

    def pop(self):
        try:
            return list.pop(self)
        except IndexError, e:
            raise ValueError(e)

    def remove(self, replicator):
        """Default list.remove uses '==' instead of physical equality"""
        to_remove = None
        for (i, contained) in enumerate(self):
            if contained is replicator:
                to_remove = i
                break

        if to_remove is not None:
            del self[to_remove]
        else:
            raise ValueError('%r not in pool' % replicator)
        return

    def __repr__(self):
        return 'OrderedPool(%s)' % pformat(list(self))

    def __contains__(self, replicator):
        """Default list.__contains__ tests '==' instead of physical equality"""
        for contained in self:
            if contained is replicator:
                return True

        return False


class UnionPool(object):
    """Virtual pool that behaves as the union of several back end pools

    A creation pool that is used to add new replicators if any can be provided
    as optional argument. If none is provided, the last backend pool is used
    for creations.
    """
    __module__ = __name__
    implements(IPool)

    def __init__(self, pools, creation_pool=None):
        self._pools = pools
        self._reversed_pools = reversed(pools)
        self._creation_pool = pools[(-1)]

    def add(self, replicator):
        self._creation_pool.add(replicator)

    def pop(self):
        for pool in self._reversed_pools:
            if len(pool):
                return pool.pop()

        return pool.pop()

    def remove(self, replicator):
        for pool in self._pools:
            if replicator in pool:
                return pool.remove(replicator)

        return pool.remove(replicator)

    def clear(self):
        for pool in self._pools:
            pool.clear()

    def __len__(self):
        return reduce(int.__add__, (len(pool) for pool in self._pools))

    def __iter__(self):
        return chain(*self._pools)

    def __contains__(self, replicator):
        for pool in self._pools:
            if replicator in pool:
                return True

        return False

    def __repr__(self):
        return 'UnionPool(%s)' % pformat(list(self._pools))


class EliteArchive(object):
    """Weak elitism adapter that keeps only the best replicators in the pool

    Only replicators that are better or equivalent to existing are admitted in
    the elite archive. By adding a better individual into the archive, all
    other lower quality replicators are autmatically removed.
    """
    __module__ = __name__
    implements(IPool)
    adapts(IPool, IComparator)

    def __init__(self, pool=None, comparator=None):
        self._last_added = None
        self._comparator = comparator or SimpleComparator()
        if pool is None:
            pool = Pool()
        elif not IPool.providedBy(pool):
            pool = Pool(pool)
        replicators = list(pool)
        self._storage = pool
        self._storage.clear()
        for rep in replicators:
            self.add(rep)

        return

    def add(self, rep):
        if self._last_added is not None:
            cmp_res = self._comparator.cmp(rep, self._last_added)
            if cmp_res < 0:
                return
            if cmp_res > 0:
                self._storage.clear()
            for already_in in self._storage:
                if already_in == rep:
                    return

        self._last_added = rep
        self._storage.add(rep)
        return

    def pop(self):
        return self._storage.pop()

    def remove(self, rep):
        return self._storage.remove(rep)

    def clear(self):
        self._last_added = None
        return self._storage.clear()

    def __len__(self):
        return self._storage.__len__()

    def __iter__(self):
        return self._storage.__iter__()

    def __contains__(self, rep):
        return self._storage.__contains__(rep)

    def __repr__(self):
        return 'EliteArchive(%s)' % pformat(list(self))


class ProviderFromEliteArchive(object):
    """Adapts an elite archive to plug it in a chain of adapters"""
    __module__ = __name__
    implements(IProvider)
    adapts(IProvider, IPool)

    def __init__(self, archive, provider):
        self._provider = provider
        self._archive = archive

    def next(self):
        rep = self._provider.next()
        self._archive.add(rep)
        return rep

    def __iter__(self):
        return self