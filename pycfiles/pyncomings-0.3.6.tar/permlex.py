# uncompyle6 version 3.6.7
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.5-i386/egg/pyncomb/permlex.py
# Compiled at: 2010-10-16 14:06:04
__doc__ = 'An implementation of basic combinatorial permutation operations using\nlexicographic ordering.\n\nNote that for our purposes here, permutations are represented as lists,\nwith P[i] = j meaning that P maps i to j.\n\nBy Sebastian Raaphorst, 2009.'
from . import combfuncs

def rank(n, P):
    """Return the rank of a permutation P in Sn."""
    rk = 0
    Pn = P[:]
    fac = reduce(lambda x, y: x * y, range(1, n), 1)
    for j in xrange(n):
        rk += Pn[j] * fac
        if n != j + 1:
            fac /= n - j - 1
        for i in range(j + 1, n):
            if Pn[i] > Pn[j]:
                Pn[i] -= 1

    return rk


def unrank(n, rk):
    """Return the permutation of rank rk in Sn."""
    P = [
     0] * n
    fac = 1
    for j in xrange(n - 1):
        fac *= j + 1
        d = rk % (fac * (j + 2)) / fac
        rk -= d * fac
        P[n - j - 2] = d
        for i in xrange(n - j - 1, n):
            if P[i] > d - 1:
                P[i] += 1

    return P


def succ(n, P):
    """Return the successor of the permutation P in Sn.
    If there is no successor, we return None."""
    Pn = P[:] + [-1]
    i = n - 2
    while Pn[(i + 1)] < Pn[i]:
        i -= 1

    if i == -1:
        return None
    else:
        j = n - 1
        while Pn[j] < Pn[i]:
            j -= 1

        Pn[i], Pn[j] = Pn[j], Pn[i]
        Pn[(i + 1):n] = Pn[n - 1:i:-1]
        return Pn[:-1]


def all(n):
    """A generator to create all permutations in Sn."""
    P = range(n)
    while P != None:
        yield P
        P = succ(n, P)

    return