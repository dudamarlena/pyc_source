# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/evogrid/common/evaluators.py
# Compiled at: 2006-08-10 15:54:24
"""Adapters for evaluator components

As Evaluator components are highly representation dependent, no default
implementation is provided.

However, you will find here a default multi-adapter for the following scheme:
(IEvaluator, IProvider) -> IProvider
"""
from zope.interface import implements
from zope.component import provideAdapter, adapts
from evogrid.caching.interfaces import ICache
from evogrid.caching.ram import RAMCache
from evogrid.interfaces import IEvaluator
from evogrid.interfaces import IProvider

class BaseEvaluator(object):
    """Abstract class to provide default implementation for ``evaluate``"""
    __module__ = __name__

    def compute_fitness(self, cs):
        raise NotImplementedError

    def evaluate(self, rep):
        rep.evaluation = self.compute_fitness(rep.candidate_solution)


class ProviderFromEvaluator(object):
    """Default adapter to use evaluator with providers chains

    This uses a class that wraps a generator since generators are builtin python
    objects that do not support interface implementation.
    """
    __module__ = __name__
    implements(IProvider)
    adapts(IEvaluator, IProvider)

    def _buildGenerator(self, evaluator, provider):
        while True:
            replicator = provider.next()
            evaluator.evaluate(replicator)
            yield replicator

    def __init__(self, evaluator, provider):
        generator = self._buildGenerator(evaluator, provider)
        self._generator = generator

    def next(self):
        return self._generator.next()

    def __iter__(self):
        return self._generator


provideAdapter(ProviderFromEvaluator)
_marker = object()

class MemoizedEvaluator(BaseEvaluator):
    """Base implementation of a memoize wrapper

    The key used is built on the ``candidate_solution`` attribute of the
    replicator being evaluated.
    """
    __module__ = __name__
    implements(IEvaluator)
    adapts(IEvaluator, ICache)

    def __init__(self, evaluator, cache=None):
        self._evaluator = evaluator
        if cache is None:
            cache = RAMCache(max_entries=100)
        self._cache = cache
        self._key_common = {'class': evaluator.__class__.__name__, 'method': 'evaluate'}
        return

    def compute_fitness(self, cs):
        key = self._key_common.copy()
        key['cs'] = cs
        result = self._cache.query(key, _marker)
        if result is _marker:
            result = self._evaluator.compute_fitness(cs)
            self._cache.set(key, result)
            return result
        else:
            return result