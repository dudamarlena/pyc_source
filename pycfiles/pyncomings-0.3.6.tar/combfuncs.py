# uncompyle6 version 3.6.7
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.5-i386/egg/pyncomb/combfuncs.py
# Compiled at: 2009-10-12 21:57:21
__doc__ = 'Various combinatorial functions used by the pyncomb library, and\nuseful in and of their own right.'
_Cmax = 0
_C = [[1]]

def binom(n, k, store=True):
    """Calculate the binomial coefficient C(n,k) = n!/k!(n-k)!.

    This is done using dynamic programming. If store is True, the final
    result and all intermediate computations are stored in a lookup table
    so that future function calls can be done in constant time.

    The caching lookup table should be used unless you have very specific reasons
    not to do so, as the binomial table is used in many other functions in pyncomb.
    If store is False, the binomial coefficient is fully calculated, which is very
    inefficient."""
    global _C
    global _Cmax
    if n <= _Cmax:
        if k >= 0 and k <= n:
            return _C[n][k]
        return 0
    else:
        if store:
            for i in xrange(_Cmax + 1, n + 1):
                _C.append([ (_C[(i - 1)][j] if j < i else 0) + (_C[(i - 1)][(j - 1)] if j > 0 else 0) for j in xrange(i + 1) ])

            _Cmax = n
            return _C[n][k]
        return reduce(lambda a, b: a * (n - b) / (b + 1), xrange(k), 1)


def permCount(n, k):
    """Calculate P(n,k) = n!/(n-k)!, the number of permutations over n objects, taking
    k of them at a time."""
    return binom(n, k) * reduce(lambda a, b: a * b, xrange(1, k + 1), 1)


def createLookup(B):
    """Process B to create a reverse lookup scheme that is appropriate for
    any of the libraries in pyncomb that allow for one or more base sets to
    be specified.

    Let rev(K) be the reverse lookup dictionary of a list K, i.e. if
    K[i] = j, then rev(K)[j] = i.

    If B is an integer, then return B.
    If B is a flat list, then return a pair (B,rev(B)).
    If B is a list of lists / integers, then return a list Bn with:
       1. Bn[i] = B[i] if B[i] is an integer.
       2. Bn[i] = (B[i], rev(B[i])) if B[i] is a list.

    For example, createLookup can translate a base set specification of:
        [4,['a','b','c'],[11,22]]
    which represents three base sets [0,1,2,3], ['a','b','c'], [11,22].
    The returned data will consist of base sets with their reverse lookup
    data and can be used as the B parameter in any function."""
    if type(B) == int:
        return B
    if reduce(lambda a, b: a and b, [ type(i) != list for i in B ], True):
        return (B, dict([ (B[i], i) for i in xrange(len(B)) ]))
    Bn = []
    for D in B:
        if type(D) == int:
            Bn.append(D)
        else:
            Bn.append((D, dict([ (D[i], i) for i in xrange(len(D)) ])))

    return Bn