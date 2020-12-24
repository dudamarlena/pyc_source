# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/quantecon/util/random.py
# Compiled at: 2017-01-17 17:46:10
# Size of source mod 2**32: 884 bytes
"""
Utilities to Support Random State Infrastructure
"""
import numpy as np, numbers

def check_random_state(seed):
    """
    Check the random state of a given seed.

    If seed is None, return the RandomState singleton used by np.random.
    If seed is an int, return a new RandomState instance seeded with seed.
    If seed is already a RandomState instance, return it.

    Otherwise raise ValueError.

    .. Note
       ----
        1. This code was sourced from scikit-learn

    """
    if seed is None or seed is np.random:
        return np.random.mtrand._rand
    if isinstance(seed, (numbers.Integral, np.integer)):
        return np.random.RandomState(seed)
    if isinstance(seed, np.random.RandomState):
        return seed
    raise ValueError('%r cannot be used to seed a numpy.random.RandomState instance' % seed)