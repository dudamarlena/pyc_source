# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/cbayes/solve.py
# Compiled at: 2018-07-06 19:51:41
# Size of source mod 2**32: 2313 bytes
"""
This module contains the methods for solving the stochastic inverse problem:
    :method:`cbayes.solve.perform_accept_reject`

"""
import numpy as np
from nose import with_setup

def perform_accept_reject(samples, ratios, seed=21982):
    """
    TODO: CHECK SIZES!!! samples and ratios should match up.
    Perform a standard accept/reject procedure by comparing 
    normalized density values to draws from Uniform[0,1]
    
    :param samples: Your samples.
    :type samples: :class:`~/cbayes.sample.sample_set` of shape (num, dim)
    
    :param ratios:
    :type ratios: :class:`numpy.ndarray` of shape (num,)
    :param int seed: Your seed for the accept/reject.
    
    It is encouraged that you run this multiple times when num_samples is small
    Then, average the results to get an average acceptance rate.
    """
    num_samples = len(ratios)
    M = np.max(ratios)
    eta_r = ratios / M
    np.random.seed(seed)
    nr = np.random.rand(num_samples)
    accept_inds = [i for i in range(num_samples) if eta_r[i] > nr[i]]
    return accept_inds


def problem(problem_set, method='AR', seed=25234):
    """
    This solves the inverse problem. It's a wrapper for other functions.
    
    :param problem_set: Your problem_set.
    :type problem_set: :class:`~/cbayes.sample.problem_set` 

    :param str method: One of the supported methods ('AR' for accept/reject)
    """
    samples = problem_set.input.samples
    if problem_set.ratio is None:
        if not ValueError('ratios not set'):
            raise AssertionError
    else:
        ratios = problem_set.ratio
        if method == 'AR':
            accept_inds = perform_accept_reject(samples, ratios, seed)
        else:
            raise TypeError('method given not supported. Please see documentation.')
    problem_set.accept_inds = accept_inds