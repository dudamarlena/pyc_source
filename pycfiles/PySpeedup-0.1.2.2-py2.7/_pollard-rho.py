# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pyspeedup/algorithms/_pollard-rho.py
# Compiled at: 2017-02-25 12:54:13


def DiscreteLog(p, n, alpha, beta):
    """Solves the discrete log problem using the Pollard Rho algorithm."""

    def f(x, a, b):
        temp = x % 3
        if temp == 1:
            return (beta * x % p, a, (b + 1) % n)
        if temp == 0:
            return (x * x % p, 2 * a % n, 2 * b % n)
        return (
         alpha * x % p, (a + 1) % n, b)

    x, a, b = f(1, 0, 0)
    xp, ap, bp = f(x, a, b)
    while x != xp:
        x, a, b = f(x, a, b)
        xp, ap, bp = f(xp, ap, bp)
        xp, ap, bp = f(xp, ap, bp)

    if gcd((bp - b) % n, n) != 1:
        raise Exception('Failed to determine the discrete log.')
    return (a - ap) * invMod((bp - b) % n, n) % n