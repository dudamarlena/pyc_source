# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/quantecon/util/combinatorics.py
# Compiled at: 2018-01-09 20:12:47
# Size of source mod 2**32: 2723 bytes
"""
Useful routines for combinatorics

"""
from scipy.special import comb
from numba import jit
from .numba import comb_jit

@jit(nopython=True, cache=True)
def next_k_array(a):
    """
    Given an array `a` of k distinct nonnegative integers, sorted in
    ascending order, return the next k-array in the lexicographic
    ordering of the descending sequences of the elements [1]_. `a` is
    modified in place.

    Parameters
    ----------
    a : ndarray(int, ndim=1)
        Array of length k.

    Returns
    -------
    a : ndarray(int, ndim=1)
        View of `a`.

    Examples
    --------
    Enumerate all the subsets with k elements of the set {0, ..., n-1}.

    >>> n, k = 4, 2
    >>> a = np.arange(k)
    >>> while a[-1] < n:
    ...     print(a)
    ...     a = next_k_array(a)
    ...
    [0 1]
    [0 2]
    [1 2]
    [0 3]
    [1 3]
    [2 3]

    References
    ----------
    .. [1] `Combinatorial number system
       <https://en.wikipedia.org/wiki/Combinatorial_number_system>`_,
       Wikipedia.

    """
    k = len(a)
    if k == 1 or a[0] + 1 < a[1]:
        a[0] += 1
        return a
    a[0] = 0
    i = 1
    x = a[i] + 1
    while i < k - 1 and x == a[(i + 1)]:
        i += 1
        a[i - 1] = i - 1
        x = a[i] + 1

    a[i] = x
    return a


def k_array_rank(a):
    """
    Given an array `a` of k distinct nonnegative integers, sorted in
    ascending order, return its ranking in the lexicographic ordering of
    the descending sequences of the elements [1]_.

    Parameters
    ----------
    a : ndarray(int, ndim=1)
        Array of length k.

    Returns
    -------
    idx : scalar(int)
        Ranking of `a`.

    References
    ----------
    .. [1] `Combinatorial number system
       <https://en.wikipedia.org/wiki/Combinatorial_number_system>`_,
       Wikipedia.

    """
    k = len(a)
    idx = int(a[0])
    for i in range(1, k):
        idx += comb((a[i]), (i + 1), exact=True)

    return idx


@jit(nopython=True, cache=True)
def k_array_rank_jit(a):
    """
    Numba jit version of `k_array_rank`.

    Notes
    -----
    An incorrect value will be returned without warning or error if
    overflow occurs during the computation. It is the user's
    responsibility to ensure that the rank of the input array fits
    within the range of possible values of `np.intp`; a sufficient
    condition for it is `scipy.special.comb(a[-1]+1, len(a), exact=True)
    <= np.iinfo(np.intp).max`.

    """
    k = len(a)
    idx = a[0]
    for i in range(1, k):
        idx += comb_jit(a[i], i + 1)

    return idx