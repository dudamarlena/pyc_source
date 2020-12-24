# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/navigation_mdp/utils.py
# Compiled at: 2019-09-17 19:39:02
# Size of source mod 2**32: 342 bytes
import numpy as np

def one_hot(i, n):
    v = np.zeros(n)
    v[i] = 1.0
    return v


def one_hot_nd(nd_int_array, N=None):
    if N is None:
        N = len(np.unique(nd_int_array))
    oh_mat = []
    for x in np.nditer(nd_int_array):
        oh_mat.append(one_hot(x, N))

    return np.asarray(oh_mat).reshape(nd_int_array.shape + (N,))