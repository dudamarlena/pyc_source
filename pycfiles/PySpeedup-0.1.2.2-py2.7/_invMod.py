# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pyspeedup/algorithms/_invMod.py
# Compiled at: 2017-02-25 12:54:13
from pyspeedup import concurrent

def invMod(number, modulo):
    """Uses the extended Euclidean algorithm to deduce the inverse of 'number' mod 'modulo'."""
    _, solution = _iM(modulo, number)
    return solution % modulo


@concurrent.Cache
def _iM(dividend, divisor):
    """A recursive helper function for use in inverting."""
    q, r = divmod(dividend, divisor)
    if r == 0:
        if divisor != 1:
            raise Exception('Number not invertible in given set of integers.')
        return (0, 1)
    prev, solution = _iM(divisor, r)
    prev, solution = -solution, -(prev + q * solution)
    return (prev, solution)