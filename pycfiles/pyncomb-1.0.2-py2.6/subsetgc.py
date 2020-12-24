# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.5-i386/egg/pyncomb/subsetgc.py
# Compiled at: 2010-10-16 14:06:35
"""An implementation of basic combinatorial subset opertions using a binary
reflected Gray code ordering. The binary reflected Gray code ordering is
recursively defined as an ordering on the 0-1 vectors of length 2^n as follows:

     G^n = [0G^{n-1}_0, ..., 0G^{n-1}_{2^{n-1}-1},
            1G^{n-1}_{2^{n-1}-1}, ..., 1G^{n-1}_0]

with G^1 = [0,1].

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

def rank(B, S):
    """Return the rank of the subset S in the base set B."""
    rk = 0
    b = 0
    n = B if type(B) == int else len(B[0])
    for i in xrange(n - 1, -1, -1):
        elem = n - i - 1 if type(B) == int else B[0][(n - i - 1)]
        if elem in S:
            b = 1 - b
        if b == 1:
            rk += 1 << i

    return rk


def unrank(B, rk):
    """Return the subset of rank rk in base set B."""
    S = []
    bp = 0
    n = B if type(B) == int else len(B[0])
    for i in xrange(n - 1, -1, -1):
        b = rk / (1 << i)
        if b != bp:
            S.append(n - i - 1 if type(B) == int else B[0][(n - i - 1)])
            bp = b
        rk -= b * (1 << i)

    return S


def succ(B, S):
    """Return the successor of the subset S in base set B."""

    def swap(S, elem):
        """Assume S is a sorted list. If elem is in S, return a new list
        S' not containing elem. If elem is not in S, return a new list S'
        containing elem."""
        flg = False
        Sn = []
        for i in S:
            if i == elem:
                flg = True
                continue
            if i > elem and not flg:
                Sn.append(elem)
                flg = True
            Sn.append(i)

        if not flg:
            Sn.append(elem)
        return Sn

    n = B - 1 if type(B) == int else B[0][(-1)]
    if len(S) % 2 == 0:
        return swap(S, n)
    else:
        if S[(-1)] == (0 if type(B) == int else B[0][0]):
            return
        else:
            elem = S[(-1)] - 1 if type(B) == int else B[0][(B[1][S[(-1)]] - 1)]
            return swap(S, elem)
        return


def all(B):
    """A generator to create all subsets over the specified base set."""
    Bn = B if type(B) == int else (B[0][:], dict(B[1]))
    K = []
    while K != None:
        yield K
        K = succ(Bn, K)

    return