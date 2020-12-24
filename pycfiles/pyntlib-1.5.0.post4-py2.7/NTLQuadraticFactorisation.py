# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/ntlib/NTLArchive/NTLQuadraticFactorisation.py
# Compiled at: 2018-04-23 08:51:10
import math
from .NTLExceptions import DefinitionError
from .NTLPrimeFactorisation import primeFactorisation
from .NTLTrivialDivision import trivialDivision
from .NTLUtilities import jsrange
from .NTLValidations import bool_check, composit_check, int_check
__all__ = [
 'quadraticFactorisation', 'solve']
nickname = 'decomposit'

def quadraticFactorisation(N, **kwargs):
    int_check(N)
    if N <= 1:
        raise DefinitionError('The argument must be a composit number greater than 1.')
    trust = False
    for kw in kwargs:
        if kw != 'trust':
            raise KeywordError("Keyword '%s' is not defined." % kw)
        else:
            trust = kwargs[kw]
            bool_check(trust)

    composit_check(trust, N)
    fct = primeFactorisation(N, wrap=True)
    for ptr0 in jsrange(len(fct[1])):
        if fct[1][ptr0] % 2:
            fct[1][ptr0] += 1

    if len(fct[0]):
        if fct[0][0] == 2:
            fct[0].append(3)
            fct[1].append(2)
        else:
            fct[0].append(2)
            fct[1].append(2)
    x = y = 1
    slc = len(fct[0]) // 2
    for ptr1 in jsrange(slc):
        x *= math.pow(fct[0][ptr1], fct[1][ptr1])

    for ptr2 in jsrange(slc, len(fct[0])):
        y *= math.pow(fct[0][ptr2], fct[1][ptr2])

    if x % 2:
        x *= 4
    if y % 2:
        y *= 4
    return solve(x, y)


def solve(x, y):
    if x < y:
        x, y = y, x
    a = (x + y) // 2
    b = (x - y) // 2
    return (
     a, b)