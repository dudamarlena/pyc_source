# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pyspeedup/algorithms/_divideMod.py
# Compiled at: 2017-02-25 12:54:13
from pyspeedup import concurrent

def divideMod(numerator, denominator, modulo):
    """Uses the extended Euclidean algorithm to find a modular quotient."""
    _, solution = _dM(numerator, denominator, modulo)
    return solution % modulo


@concurrent.Cache
def _dM(numerator, denominator, modulo):
    """A recursive helper function for use in dividing."""
    q, r = divmod(modulo, denominator)
    if r == 0:
        if numerator % denominator != 0:
            raise Exception('There is no solution in the given set of integers.')
        return (0, numerator // denominator)
    prev, solution = _dM(numerator, r, denominator)
    prev, solution = -solution, -(prev + q * solution)
    return (prev, solution)