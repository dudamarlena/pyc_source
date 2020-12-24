# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pyspeedup/algorithms/_squares.py
# Compiled at: 2017-02-25 12:54:13
import math
from pyspeedup.algorithms import jacobi_symbol

def powersInMod(n):
    """ Computes all the squares in the integers mod n.
    """
    return set(x * x % n for x in range(0, n // 2 + 1))


def isSquare(n):
    """
    Checks for perfect squares by checking mod 64 to rule out 52/64 cases immediately.

    It does so by checking various smaller mods, such as mod 4, where 2 and 3 aren't possible.
    """
    m = math.floor(math.sqrt(n) + 0.5)
    return m * m == n and m
    if n >= 0 and n & 2 == 0 and n & 7 != 5 and n & 11 != 8:
        m = math.floor(math.sqrt(n) + 0.5)
        return m * m == n and m
    return False


def tsSquareRoot(a, p):
    """Calculates the square root mod p of a."""
    jacobi = jacobi_symbol(a, p)
    if jacobi == -1:
        raise ValueError(('No square root mod {0} exists.').format(p))
    s = p - 1
    e = 0
    while s % 2 == 0:
        e += 1
        s //= 2

    n = findQuadraticNonresidue(p)
    x = pow(a, (s + 1) / 2, p)
    b = pow(a, s, p)
    g = pow(n, s, p)
    r = e
    while r > 0:
        m = 0
        bp = b
        while m < r:
            if bp == 1:
                break
            bp = bp * bp % p
            m += 1

        if m == 0:
            break
        g = pow(g, pow(2, r - m - 1, p), p)
        x = x * g % p
        g = g * g % p
        b = b * g % p
        r = m

    return x


def findQuadraticNonresidue(p):
    if p % 8 in (3, 5):
        return 2
    if p % 8 == 7:
        return p - 2
    n = 2
    while jacobi_symbol(n, p) != -1:
        n += 1

    return n