# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/ntlib/NTLArchive/NTLLeastCommonMultiple.py
# Compiled at: 2018-04-23 08:51:10
from .NTLGreatestCommonDivisor import greatestCommonDivisor
from .NTLValidations import int_check
__all__ = [
 'leastCommonMultiple']
nickname = 'lcm'

def leastCommonMultiple(a, b):
    int_check(a, b)
    if a < 0:
        a = -1 * a
    if b < 0:
        b = -1 * b
    return a * b // greatestCommonDivisor(a, b)