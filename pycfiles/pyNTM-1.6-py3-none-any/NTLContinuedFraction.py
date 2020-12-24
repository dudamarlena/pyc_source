# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/ntlib/NTLArchive/NTLContinuedFraction.py
# Compiled at: 2018-04-23 08:51:10
import fractions, math
from .NTLUtilities import jsfloor
from .NTLValidations import notneg_check, real_check
__all__ = [
 'continuedFraction']
nickname = 'fraction'

def continuedFraction(numerator, denominator=None):
    if denominator is None:
        denominator = 1
    real_check(numerator, denominator)
    notneg_check(numerator, denominator)
    x = fractions.Fraction(numerator, denominator)
    a = jsfloor(x)
    x -= a
    cf_ = [a]
    while x != 0:
        x = 1 / x
        a = jsfloor(x)
        x -= a
        cf_.append(a)

    if cf_[(-1)] == 2:
        cf_[(-1):] = [1, 1]
    return cf_