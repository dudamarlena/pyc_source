# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/gleipnir/stopping_criterion.py
# Compiled at: 2019-03-14 18:41:15
# Size of source mod 2**32: 2131 bytes
"""Classes for defining the stopping criterion for a Nested Sampling run.

This module defines the classes used by gleinir.nested_sampling.NestedSampling
instances to define the stopping criterion for the Nested Sampling run.

"""
import numpy as np

class NumberOfIterations(object):
    __doc__ = 'Stop after a fixed number of iteration.\n    Attributes:\n        n_iterations (int): The number of Nested Sampling iterations after\n            which to terminate the run.\n    '

    def __init__(self, iterations):
        """Initialize the NumberOfIterations stopping criterion.
        Args:
            iterations (int): Sets the n_iterations Attribute.
        """
        self.n_iterations = iterations

    def __call__(self, nested_sampler):
        """Evaluate the criterion.
        Args:
            nested_sampler (:obj:gleipnir.nested_sampler.NestedSampling): The
                instance of the NestedSampling object to be tested.
        Return:
            bool : Should stop the Nested Sampling run if True, should
                continue running if False.
        """
        return nested_sampler._n_iterations >= self.n_iterations


class RemainingPriorMass(object):
    __doc__ = 'Stop after the remaining amount of prior mass reaches a preset threshold.\n    Attributes:\n        cutoff (float): The remaining prior mass threshold that Nested Sampling\n            iterations should reach after which to terminate the run.\n    '

    def __init__(self, cutoff):
        """Initialize the RemainingPriorMass stopping criterion.
        Args:
            cutoff (float): Sets the cutoff Attribute.
        """
        self.cutoff = cutoff

    def __call__(self, nested_sampler):
        """Evaluate the criterion.
        Args:
            nested_sampler (:obj:gleipnir.nested_sampler.NestedSampling): The
                instance of the NestedSampling object to be tested.
        Return:
            bool : Should stop the Nested Sampling run if True, should
                continue running if False.
        """
        return nested_sampler._alpha ** nested_sampler._n_iterations <= self.cutoff