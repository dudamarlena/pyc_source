# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/aestrivex/anaconda3/lib/python3.7/site-packages/bct/utils/miscellaneous_utilities.py
# Compiled at: 2020-04-27 14:47:22
# Size of source mod 2**32: 3584 bytes
from __future__ import division, print_function
import random, numpy as np

class BCTParamError(RuntimeError):
    pass


def teachers_round(x):
    """
    Do rounding such that .5 always rounds to 1, and not bankers rounding.
    This is for compatibility with matlab functions, and ease of testing.
    """
    if x > 0 and x % 1 >= 0.5 or x < 0:
        if x % 1 > 0.5:
            return int(np.ceil(x))
    return int(np.floor(x))


def pick_four_unique_nodes_quickly(n, seed=None):
    """
    This is equivalent to np.random.choice(n, 4, replace=False)

    Another fellow suggested np.random.random_sample(n).argpartition(4) which is
    clever but still substantially slower.
    """
    rng = get_rng(seed)
    k = rng.randint(n ** 4)
    a = k % n
    b = k // n % n
    c = k // n ** 2 % n
    d = k // n ** 3 % n
    if a != b:
        if a != c:
            if a != d:
                if b != c:
                    if b != d:
                        if c != d:
                            return (
                             a, b, c, d)
    return pick_four_unique_nodes_quickly(n, rng)


def cuberoot(x):
    """
    Correctly handle the cube root for negative weights, instead of uselessly
    crashing as in python or returning the wrong root as in matlab
    """
    return np.sign(x) * np.abs(x) ** 0.3333333333333333


def dummyvar(cis, return_sparse=False):
    """
    This is an efficient implementation of matlab's "dummyvar" command
    using sparse matrices.

    input: partitions, NxM array-like containing M partitions of N nodes
        into <=N distinct communities

    output: dummyvar, an NxR matrix containing R column variables (indicator
        variables) with N entries, where R is the total number of communities
        summed across each of the M partitions.

        i.e.
        r = sum((max(len(unique(partitions[i]))) for i in range(m)))
    """
    n = np.size(cis, axis=0)
    m = np.size(cis, axis=1)
    r = np.sum((np.max(len(np.unique(cis[:, i]))) for i in range(m)))
    nnz = np.prod(cis.shape)
    ix = np.argsort(cis, axis=0)
    s_cis = cis[ix][:, range(m), range(m)]
    mask = np.hstack((((True,), ) * m, (s_cis[:-1, :] != s_cis[1:, :]).T))
    indptr, = np.where(mask.flat)
    indptr = np.append(indptr, nnz)
    import scipy.sparse as sp
    dv = sp.csc_matrix((np.repeat((1, ), nnz), ix.T.flat, indptr), shape=(n, r))
    return dv.toarray()


def get_rng(seed=None):
    """
    By default, or if `seed` is np.random, return the global RandomState
    instance used by np.random.
    If `seed` is a RandomState instance, return it unchanged.
    Otherwise, use the passed (hashable) argument to seed a new instance
    of RandomState and return it.

    Parameters
    ----------
    seed : hashable or np.random.RandomState or np.random, optional

    Returns
    -------
    np.random.RandomState
    """
    if not seed is None:
        if seed == np.random:
            return np.random.mtrand._rand
        if isinstance(seed, np.random.RandomState):
            return seed
    else:
        try:
            rstate = np.random.RandomState(seed)
        except ValueError:
            rstate = np.random.RandomState(random.Random(seed).randint(0, 4294967295))

    return rstate