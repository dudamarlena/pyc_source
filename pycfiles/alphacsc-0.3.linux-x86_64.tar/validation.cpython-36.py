# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/tom/.local/miniconda/lib/python3.6/site-packages/alphacsc/utils/validation.py
# Compiled at: 2019-06-04 04:10:26
# Size of source mod 2**32: 964 bytes
import numpy as np

def check_consistent_shape(*args):
    for array in args[1:]:
        if array is not None and array.shape != args[0].shape:
            raise ValueError('Incompatible shapes. Got (%s != %s)' % (
             array.shape, args[0].shape))


def check_random_state(seed):
    """Turn seed into a np.random.RandomState instance.

    If seed is None, return the RandomState singleton used by np.random.
    If seed is an int, return a new RandomState instance seeded with seed.
    If seed is already a RandomState instance, return it.
    Otherwise raise ValueError.
    """
    if seed is None or seed is np.random:
        return np.random.mtrand._rand
    else:
        if isinstance(seed, (int, np.integer)):
            return np.random.RandomState(seed)
        if isinstance(seed, np.random.RandomState):
            return seed
    raise ValueError('%r cannot be used to seed a numpy.random.RandomState instance' % seed)