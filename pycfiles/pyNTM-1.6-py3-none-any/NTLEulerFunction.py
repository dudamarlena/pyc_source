# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/ntlib/NTLArchive/NTLEulerFunction.py
# Compiled at: 2018-04-23 08:51:10
from .NTLCoprimalityTest import coprimalityTest
from .NTLUtilities import jsrange
from .NTLValidations import int_check, pos_check
__all__ = [
 'eulerFunction']
nickname = 'euler'

def eulerFunction(m):
    int_check(m)
    pos_check(m)
    phi_m = 0
    for num in jsrange(1, m + 1):
        if coprimalityTest(num, m):
            phi_m += 1

    return phi_m