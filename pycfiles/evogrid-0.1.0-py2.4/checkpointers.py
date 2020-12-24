# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/evogrid/common/checkpointers.py
# Compiled at: 2006-08-08 16:11:46
"""Standard checkpointing strategy implementations
"""
from time import time
from zope.interface import implements, alsoProvides
from zope.component import adapts
from evogrid.common.comparators import SimpleComparator
from evogrid.common.pools import EliteArchive, ProviderFromEliteArchive
from evogrid.common.replicators import Replicator
from evogrid.common.evaluators import BaseEvaluator
from evogrid.interfaces import ICheckpointer, IComparator, ICounter, IEvaluator, IPool, IProvider, IReplicator
_missing = object()

class TimedCheckpointer(object):
    """Continue while delay is not over

    Start measuring time at init time
    """
    __module__ = __name__
    implements(ICheckpointer)

    def __init__(self, delay):
        """`delay` in seconds before time is over"""
        self._delay = delay
        self._t0 = time()

    def reset(self):
        self._t0 = time()

    def should_stop(self):
        return time() - self._t0 >= self._delay


class Counter(object):
    """Simple counter implementation
    """
    __module__ = __name__
    implements(ICounter)
    count = 0

    def increment(self, step=1):
        self.count += step


class CounterCheckpointer(Counter):
    """Countinue while number of evaluations is not reached

    The number of evaluations is measured by adapting an evaluator interface.
    """
    __module__ = __name__
    implements(ICheckpointer)

    def __init__(self, maxcount, autoincrement=True):
        self._maxcount = maxcount
        self._autoincrement = autoincrement

    def reset(self):
        self.count = 0

    def should_stop(self):
        if self._autoincrement:
            self.increment()
        return self.count >= self._maxcount


class CountingEvaluator(BaseEvaluator):
    """Evaluator increments a counter at each call to `compute_fitness`"""
    __module__ = __name__
    implements(IEvaluator)
    adapts(ICounter, IEvaluator)

    def __init__(self, counter, evaluator):
        self._counter = counter
        self._evaluator = evaluator

    def compute_fitness(self, cs):
        """Increment the counter by one and delegate to the replicator"""
        self._counter.increment()
        return self._evaluator.compute_fitness(cs)


class CountingProvider(object):
    """Adapter to make a provider increment a counter at each `next` call
    """
    __module__ = __name__
    implements(IProvider)
    adapts(ICounter, IProvider)

    def __init__(self, counter, provider):
        self._counter = counter
        self._provider = provider

    def next(self):
        """Increment the counter by one and delegate the provider call"""
        self._counter.increment()
        return self._provider.next()

    def __iter__(self):
        return self


class ReferenceReplicator(Replicator):
    """Fake replicator used as reference"""
    __module__ = __name__

    def __init__(self, evaluation):
        self.evaluation = evaluation


class PoolQualityCheckpointer:
    """Watch the quality of a pool and stops when it reaches some reference

    This is more efficient when the pool is weak elitism archive
    """
    __module__ = __name__
    implements(ICheckpointer)
    adapts(IPool, IComparator, IReplicator)

    def __init__(self, pool, comparator=None, rep=None, evaluation=_missing):
        self._pool = pool
        self._comparator = comparator or SimpleComparator()
        if rep is None and evaluation is not _missing:
            rep = ReferenceReplicator(evaluation)
        elif rep is None and evaluation is _missing:
            raise ValueError('%s instance needs at least a reference replicator or a reference evaluation' % self.__class__)
        self._reference = rep
        return

    def reset(self):
        pass

    def should_stop(self):
        if len(self._pool) == 0:
            return False
        max = self._comparator.max(self._pool)
        return self._comparator.cmp(max, self._reference) >= 0


class PoolEvolutionCheckpointer:
    """Watch the quality of a pool and stops when it stops increasing

    The max_counts is a count down threshold to set the maximum number of
    calls to the `should_stop` method before it returns `True` for a pool that no
    longer increases its quality.

    This component is more efficient when the pool is weak elitism archive
    """
    __module__ = __name__
    implements(ICheckpointer)
    adapts(IPool, IComparator)

    def __init__(self, pool, maxcount=1, comparator=None):
        self._pool = pool
        self._maxcount = maxcount
        self._count = 0
        self._comparator = comparator or SimpleComparator()
        if len(pool) > 0:
            self._current_max = self._comparator.max(pool)
        else:
            self._current_max = Replicator()

    def reset(self):
        self._count = 0

    def should_stop(self):
        if len(self._pool) == 0:
            self._count += 1
            return self._count > self._maxcount
        last_max = self._current_max
        self._current_max = self._comparator.max(self._pool)
        if self._comparator.cmp(self._current_max, last_max) > 0:
            self._count = 1
            return False
        self._count += 1
        return self._count > self._maxcount


class BaseCompoundCheckpointer(object):
    """Abstract base class to factor common compound checkpointers' methods"""
    __module__ = __name__

    def __init__(self, *checkpointers):
        self._checkpointers = checkpointers

    def reset(self):
        for checkpointer in self._checkpointers:
            checkpointer.reset()


class OrCompoundCheckpointer(BaseCompoundCheckpointer):
    """Stops if at least one the checkpointers tells to stop"""
    __module__ = __name__
    implements(ICheckpointer)

    def should_stop(self):
        for checkpointer in self._checkpointers:
            if checkpointer.should_stop():
                return True

        return False


class AndCompoundCheckpointer(BaseCompoundCheckpointer):
    """Stops if all checkpointers tells to stop"""
    __module__ = __name__
    implements(ICheckpointer)

    def should_stop(self):
        for checkpointer in self._checkpointers:
            if not checkpointer.should_stop():
                return False

        return True


class GenericProviderCheckpointer(object):
    """Generic implementation that combines most of Checkpointer strategies

    This component implements both the IProvider and ICheckpointer interfaces.
    It's semantics is mostly defined at init time according to the arguments
    passed to the constructor:

    - provider: orginal replicator source to adapt
    - maxtime: time limit for a TimedCheckpointer
    - maxcount: count bound for a CounterCheckpointer
    - maxsteadyness: count bound for a PoolEvolutionCheckpointer
    - reference: reference evaluation or replicator for a
      PoolQualityCheckpointer
    - comparator: to provide a custom comparision strategy (set to
      SimpleComparator() by default)
    - archive: to provide a custom archive instance (set to EliteArchive() by
      default)
    - combinator: class used to combine internal replicators together (set to
      OrCompoundCheckpointer by default)
    """
    __module__ = __name__
    implements(ICheckpointer)
    adapts(IProvider)

    def __init__(self, provider=None, maxtime=None, maxcount=None, maxsteadyness=None, reference=None, comparator=None, archive=None, combinator=None):
        comparator = comparator or SimpleComparator()
        self.archive = archive or EliteArchive(comparator=comparator)
        if provider is not None:
            self._provider = ProviderFromEliteArchive(self.archive, provider)
            alsoProvides(self, IProvider)
        checkpointers = []
        if maxtime is not None:
            checkpointers.append(TimedCheckpointer(maxtime))
        if maxcount is not None:
            checkpointers.append(CounterCheckpointer(maxcount))
        if maxsteadyness is not None:
            checkpointers.append(PoolEvolutionCheckpointer(self.archive, maxsteadyness, comparator))
        if reference is not None:
            if not IReplicator.implementedBy(reference):
                evaluation, reference = reference, Replicator()
                reference.evaluation = evaluation
            checkpointers.append(PoolQualityCheckpointer(self.archive, comparator, reference))
        combinator = combinator or OrCompoundCheckpointer
        self._checkpointer = combinator(*checkpointers)
        return

    def reset(self):
        return self._checkpointer.reset()

    def should_stop(self):
        return self._checkpointer.should_stop()

    def next(self):
        return self._provider.next()

    def __iter__(self):
        return self