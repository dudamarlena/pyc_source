# uncompyle6 version 3.6.7
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.5-i386/egg/pyncomb/ksubsetrevdoor.py
# Compiled at: 2010-10-16 14:05:29
__doc__ = 'An implementation of basic combinatorial k-subset operations using\na revolving door (minimal change) ordering.\n\nNote that for our purposes here, sets are represented as lists as\nranking, unranking, and successor functions need a total order on the\nelements of the set.\n\nFor the base set B, if B is an integer, we assume that our base set is\n[0,...,B-1]. Otherwise, assume that B is a pair consisting of:\n   1. a list representing the base set\n   2. a reverse lookup dict, mapping elements of the base set to their\n      position in the total order.\n   Example: [0,3,4,2], {0:0, 3:1, 4:2, 2:3}\nNote that we require B to contain the reverse lookup information to\nspeed up the algorithms here; otherwise, we would need to call index on\nour base set many times, which would increase complexity by a factor of\nthe length of the base set.\n\nBy Sebastian Raaphorst, 2009.'
from . import combfuncs

def rank(B, K):
    """Return the rank of k-subset K in base set B."""
    block = K if type(B) == int else [ B[1][i] for i in K ]
    k = len(block)
    return sum([ (1 if i % 2 == k % 2 else -1) * combfuncs.binom(block[(i - 1)] + 1, i) for i in xrange(k, 0, -1) ]) + (0 if k % 2 == 0 else -1)


def unrank(B, k, rk):
    """Return the k-subset of rank rk in base set B."""
    v = B if type(B) == int else len(B[0])
    K = [
     0] * k
    for i in xrange(k, 0, -1):
        while combfuncs.binom(v, i) > rk:
            v -= 1

        K[i - 1] = v
        rk = combfuncs.binom(v + 1, i) - rk - 1

    if type(B) == int:
        return K
    return [ B[0][i] for i in K ]


def succ(B, K):
    """Return the successor of the k-subset K in base set B.
    If there is no successor, we return None."""
    v = B if type(B) == int else len(B[0])
    Kn = (K if type(B) == int else [ B[1][i] for i in K ]) + [v]
    k = len(K)
    j = 0
    while j < k and Kn[j] == j:
        j += 1

    if k % 2 == j % 2:
        if j == 0:
            Kn[0] -= 1
        else:
            Kn[j - 1] = j
            Kn[j - 2] = j - 1
    elif Kn[(j + 1)] != Kn[j] + 1:
        Kn[j - 1] = Kn[j]
        Kn[j] += 1
    else:
        Kn[j + 1] = Kn[j]
        Kn[j] = j
    if Kn[:k] == range(k):
        return None
    else:
        if type(B) == int:
            return Kn[:k]
        return [ B[0][i] for i in Kn[:k] ]


def all(B, k):
    """A generator to create all subsets over the specified base set B."""
    Bn = B if type(B) == int else (B[0][:], dict(B[1]))
    K = range(k) if type(B) == int else Bn[0][:k]
    while K != None:
        yield K
        K = succ(Bn, K)

    return