# uncompyle6 version 3.6.7
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.5-i386/egg/pyncomb/subsetgc.py
# Compiled at: 2010-10-16 14:06:35
__doc__ = 'An implementation of basic combinatorial subset opertions using a binary\nreflected Gray code ordering. The binary reflected Gray code ordering is\nrecursively defined as an ordering on the 0-1 vectors of length 2^n as follows:\n\n     G^n = [0G^{n-1}_0, ..., 0G^{n-1}_{2^{n-1}-1},\n            1G^{n-1}_{2^{n-1}-1}, ..., 1G^{n-1}_0]\n\nwith G^1 = [0,1].\n\nNote that for our purposes here, sets are represented as lists as\nranking, unranking, and successor functions need a total order on the\nelements of the set.\n\nFor the base set B, if B is an integer, we assume that our base set is\n[0,...,B-1]. Otherwise, assume that B is a pair consisting of:\n   1. a list representing the base set\n   2. a reverse lookup dict, mapping elements of the base set to their\n      position in the total order.\n   Example: [0,3,4,2], {0:0, 3:1, 4:2, 2:3}\nNote that we require B to contain the reverse lookup information to\nspeed up the algorithms here; otherwise, we would need to call index on\nour base set many times, which would increase complexity by a factor of\nthe length of the base set.\n\nBy Sebastian Raaphorst, 2009.'
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