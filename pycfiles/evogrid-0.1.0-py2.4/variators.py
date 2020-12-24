# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/evogrid/numeric/variators.py
# Compiled at: 2006-08-26 13:50:17
"""Variators for numpy array encoded replicators

Some of the following variators are deterministic Lamarckian optimizers
whereas other are just blind Darwinian varitors (mutators and crossing over
style combinators).
"""
from zope.interface import implements
from zope.component import adapts
from evogrid.interfaces import IEvaluator, IVariator
from numpy import array
from numpy.random import uniform, normal
from scipy.optimize import fmin, fmin_bfgs, fmin_cg, fmin_powell

class GaussianMutator(object):
    """Apply centered gaussian noise to the replicator"""
    __module__ = __name__
    implements(IVariator)
    number_to_combine = 1

    def __init__(self, scale=1.0, scales=None):
        self.scale = scale
        self.scales = scales

    def combine(self, *reps):
        rep = reps[0]
        scales = self.scales
        if scales is not None:
            delta = array([ scale and normal(scale=scale) or 0.0 for scale in scales ])
        else:
            delta = normal(scale=self.scale, size=len(rep.candidate_solution))
        rep.candidate_solution += delta
        return (rep,)


class DomainAwareGaussianMutator(object):
    """Apply centered gaussian noise to the replicator

    The scale here is not a absolute value but multiplied to the size
    of the domain for each variable.
    """
    __module__ = __name__
    implements(IVariator)
    number_to_combine = 1

    def __init__(self, scale=0.001, scales=None):
        self.scale = scale
        self.scales = scales

    def combine(self, *reps):
        rep = reps[0]
        scales = self.scales
        if scales is None:
            scales = array([self.scale] * len(rep.candidate_solution))
        domain = rep.domain
        sizes = domain.max - domain.min
        scales = scales * sizes
        delta = array([ normal(scale=scale) for scale in scales ])
        rep.candidate_solution += delta
        return (rep,)


class BlendingCrossover(object):
    """Return two new replicators by linearly combining the parents"""
    __module__ = __name__
    implements(IVariator)
    number_to_combine = 2

    def __init__(self, beta_min=0.1, beta_max=1.5):
        self.beta_min = beta_min
        self.beta_max = beta_max

    def combine(self, *replicators):
        (rep1, rep2) = replicators
        cs1, cs2 = rep1.candidate_solution, rep2.candidate_solution
        beta = uniform(self.beta_min, self.beta_max, len(cs1))
        rep1.candidate_solution = beta * cs1 + (1 - beta) * cs2
        rep2.candidate_solution = beta * cs2 + (1 - beta) * cs1
        return replicators


class BaseLocalSearchVariator(object):
    """Wraps one of scipy.optimize search algorithm into a variator"""
    __module__ = __name__
    implements(IVariator)
    adapts(IEvaluator)
    maxiter = 10
    func = None
    optimizer = None
    number_to_combine = 1

    def __init__(self, evaluator, maxiter=10, **kw):
        self.maxiter = maxiter
        self.func = evaluator.compute_fitness
        self._kw = kw

    def combine(self, *replicators):
        rep = replicators[0]
        optimized = self.optimizer(self.func, rep.candidate_solution, maxiter=self.maxiter, disp=0, **self._kw)
        rep.candidate_solution = optimized
        return (rep,)


class SimplexVariator(BaseLocalSearchVariator):
    __module__ = __name__
    optimizer = staticmethod(fmin)


class BfgsVariator(BaseLocalSearchVariator):
    __module__ = __name__
    optimizer = staticmethod(fmin_bfgs)


class CgVariator(BaseLocalSearchVariator):
    __module__ = __name__
    optimizer = staticmethod(fmin_cg)


class PowellVariator(BaseLocalSearchVariator):
    __module__ = __name__
    optimizer = staticmethod(fmin_powell)