# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.5-i386/egg/pyncomb/ksubsetcolex.py
# Compiled at: 2010-10-16 14:04:50
"""An implementation of basic combinatorial k-subset operations using
co-lex ordering.

Note that for our purposes here, sets are represented as lists as
ranking, unranking, and successor functions need a total order on the
elements of the set.

For the base set B, if B is an integer, we assume that our base set is
[0,...,B-1]. Otherwise, assume that B is a pair consisting of:
   1. a list representing the base set
   2. a reverse lookup dict, mapping elements of the base set to their
      position in the total order.
   Example: [0,3,4,2], {0:0, 3:1, 4:2, 2:3}
Note that we require B to contain the reverse lookup information to
speed up the algorithms here; otherwise, we would need to call index on
our base set many times, which would increase complexity by a factor of
the length of the base set.

By Sebastian Raaphorst, 2009."""
from . import combfuncs

def rank(B, K):
    """Return the rank of k-subset K in base set B."""
    k = len(K)
    rk = 0
    for i in xrange(k):
        n = K[(k - i - 1)] if type(B) == int else B[1][K[(k - i - 1)]]
        rk += 0 if k - i > n else combfuncs.binom(n, k - i)

    return rk


def unrank(B, k, rk):
    """Return the k-subset of rank rk in base set B."""
    x = B - 1 if type(B) == int else len(B[0]) - 1
    K = [
     0] * k
    for i in xrange(k):
        while combfuncs.binom(x, k - i) > rk:
            x -= 1

        K[k - i - 1] = x if type(B) == int else B[0][x]
        rk -= combfuncs.binom(x, k - i)

    return K


def succ(B, K):
    """Return the successor of the k-subset K in base set B.
    If there is no successor, we return None."""
    k = len(K)
    maxelem = B - 1 if type(B) == int else B[0][(-1)]
    for i in xrange(k):
        if i < k - 1:
            nextelem = K[i] + 1 if type(B) == int else B[0][(B[1][K[i]] + 1)]
            if K[(i + 1)] != nextelem:
                return (range(i) if type(B) == int else B[0][:i]) + [nextelem] + K[i + 1:]
        elif K[i] < maxelem:
            nextelem = K[i] + 1 if type(B) == int else B[0][(B[1][K[i]] + 1)]
            return (range(i) if type(B) == int else B[0][:i]) + [nextelem]

    return


def all(B, k):
    """A generator to create all k-subsets over the specified base set B."""
    Bn = B if type(B) == int else (B[0][:], dict(B[1]))
    K = range(k) if type(B) == int else Bn[0][:k]
    while K != None:
        yield K
        K = succ(Bn, K)

    return