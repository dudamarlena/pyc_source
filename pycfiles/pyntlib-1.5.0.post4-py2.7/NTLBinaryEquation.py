# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/ntlib/NTLArchive/NTLBinaryEquation.py
# Compiled at: 2018-04-23 08:51:10
from .NTLBezoutEquation import bezoutEquation
from .NTLExceptions import SolutionError
from .NTLGreatestCommonDivisor import greatestCommonDivisor
from .NTLValidations import int_check
__all__ = [
 'binaryEquation']
nickname = 'binary'

def binaryEquation(a, b, c):
    int_check(a, b, c)
    pn_a = pn_b = pn_c = 1
    if a < 0:
        pn_a = -1
        a *= -1
    if b < 0:
        pn_b = -1
        b *= -1
    if c < 0:
        pn_c = -1
        c *= -1
    gcd = greatestCommonDivisor(a, b)
    if c % gcd != 0:
        raise SolutionError('The binary equation has no integral solution.')
    else:
        mtp = c // gcd
    s, t = bezoutEquation(a, b)
    x0 = s * mtp * pn_a * pn_c
    y0 = t * mtp * pn_b * pn_c
    return (
     x0, y0)