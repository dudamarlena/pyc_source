# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pyspeedup/algorithms/_legendre.py
# Compiled at: 2017-02-25 12:54:13
from pyspeedup import concurrent

@concurrent.Cache
def jacobi_symbol(a, n):
    """Calculate the Jacobi symbol (a/n), which is equivalent to the Legendre for prime n."""
    if n % 2 == 0:
        raise ValueError('The Jacobi symbol is undefined for even n.')
    if a < 0 or a >= n:
        a %= n
    if a == 0:
        return 0
    else:
        if a == 1:
            return 1
        if a == 2:
            if n % 8 in (3, 5):
                return -1
            if n % 8 in (1, 7):
                return 1
        elif a < 0:
            return (-1) ** ((n - 1) / 2) * jacobi_symbol(-1 * a, n)
        if a % 2 == 0:
            jacobi_symbol.apply_async(2, n)
            jacobi_symbol.apply_async(a / 2, n)
            return jacobi_symbol(2, n) * jacobi_symbol(a / 2, n)
        if a % 4 == n % 4 == 3:
            return -1 * jacobi_symbol(n, a)
        return jacobi_symbol(n, a)