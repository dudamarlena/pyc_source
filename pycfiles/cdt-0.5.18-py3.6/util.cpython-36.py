# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/cdt/causality/pairwise/Jarfo_model/util.py
# Compiled at: 2020-02-05 06:32:12
# Size of source mod 2**32: 550 bytes
"""
Random permutation of a symmetrized database

"""
import numpy as np

def random_permutation(x, y, seed=14777777):
    np.random.seed(seed)
    global_random_permutation = np.array(range(len(x) // 2))
    np.random.shuffle(global_random_permutation)
    index = np.array(range(len(x)))
    index[0::2] = 2 * global_random_permutation
    index[1::2] = 2 * global_random_permutation + 1
    x.index = index
    y.index = index
    return (x.sort_index(), y.sort_index())