# uncompyle6 version 3.6.7
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.5-i386/egg/pyncomb/permtj.py
# Compiled at: 2010-10-16 14:06:20
__doc__ = 'An implementation of basic combinatorial permutation operations using\nTrotter-Johnson (a minimal change) ordering.\n\nNote that for our purposes here, permutations are represented as lists,\nwith P[i] = j meaning that P maps i to j.\n\nBy Sebastian Raaphorst, 2009.'
from . import combfuncs

def rank(n, P):
    """Return the rank of a permutation P in Sn."""
    rk = 0
    for j in xrange(2, n + 1):
        k = 1
        i = 0
        while P[i] != j - 1:
            if P[i] < j - 1:
                k += 1
            i += 1

        if rk % 2 == 0:
            rk = j * rk + j - k
        else:
            rk = j * rk + k - 1

    return rk


def unrank(n, rk):
    """Return the permutation of rank rk in Sn."""
    P = [
     0] * n
    r2 = 0
    fac = 1
    nfac = reduce(lambda x, y: x * y, range(1, n + 1), 1)
    for j in xrange(2, n + 1):
        fac *= j
        r1 = rk * fac / nfac
        k = r1 - j * r2
        if r2 % 2 == 0:
            for i in range(j - 2, j - k - 2, -1):
                P[i + 1] = P[i]

            P[j - k - 1] = j - 1
        else:
            for i in range(j - 2, k - 1, -1):
                P[i + 1] = P[i]

            P[k] = j - 1
        r2 = r1

    return P


def succ(n, P):
    """Return the successor of the permutation P in Sn.
    If there is no successor, we return None."""

    def _permParity(n, P):
        """Determine the number of cycles in P."""
        alpha = [
         0] * n
        c = 0
        for j in xrange(n):
            if alpha[j] == 0:
                c += 1
                alpha[j] = 1
                i = j
                while P[i] != j:
                    i = P[i]
                    alpha[i] = 1

        return (n - c) % 2

    st = 0
    rho = P[:]
    Pn = P[:]
    m = n
    while m > 1:
        d = rho.index(m - 1)
        rho[d:(m - 1)] = rho[d + 1:m]
        par = _permParity(m - 1, rho)
        if par == 1:
            if d == m - 1:
                m -= 1
            else:
                Pn[st + d], Pn[st + d + 1] = Pn[(st + d + 1)], Pn[(st + d)]
                break
        elif d == 0:
            m -= 1
            st += 1
        else:
            Pn[st + d], Pn[st + d - 1] = Pn[(st + d - 1)], Pn[(st + d)]
            break

    if m == 1:
        return None
    else:
        return Pn


def all(n):
    """A generator to create all permutations in Sn."""
    P = range(n)
    while P != None:
        yield P
        P = succ(n, P)

    return