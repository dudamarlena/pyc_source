# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/evogrid/common/replacers.py
# Compiled at: 2006-07-11 12:43:54
"""Classical replacers implementations

Replacers put replicators back to some pool according to some quality criterion.
"""
from itertools import islice
from zope.interface import implements
from zope.component import adapts
from evogrid.common.selectors import RandomSelector
from evogrid.common.comparators import SimpleComparator
from evogrid.interfaces import IReplacer, ISelector, IComparator

class GenerationalReplacer(object):
    """Build an offsprings pool of size `number` (same size as the parent pool
    by default) and replace the parents pool with the offsprings pool.
    """
    __module__ = __name__
    implements(IReplacer)
    number = 0

    def __init__(self, number=0):
        self.number = number

    def replace(self, provider, pool):
        number = self.number or len(pool)
        offspring = tuple(islice(provider, number))
        pool.clear()
        for rep in offspring:
            pool.add(rep)


class TournamentReplacer(object):
    """Organise a tournament between the next replicator from the provider and a
    selected representant of the pool. The winner gets back into the pool

    To build a `TournamentReplacer`, you can optionally provide a selector and
    a comparator to fine tune it's behavior:

      - the `selector` is used to get an player among the replicators of the
        pool
      - the `comparator` is used as a judge to determine which opponent is the
        winner
    """
    __module__ = __name__
    implements(IReplacer)
    adapts(ISelector, IComparator)
    number = 0

    def __init__(self, selector=None, comparator=None, number=0):
        if selector is None:
            selector = RandomSelector()
        if comparator is None:
            comparator = SimpleComparator()
        self._selector = selector
        self._comparator = comparator
        self.number = number
        return

    def replace(self, provider, pool):
        number = self.number or len(pool)
        for _ in xrange(number):
            rep1 = provider.next()
            rep2 = self._selector.select_from(pool)
            if self._comparator.cmp(rep1, rep2) > 0:
                pool.add(rep1)
                pool.remove(rep2)