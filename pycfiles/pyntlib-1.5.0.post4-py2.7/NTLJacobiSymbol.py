# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/ntlib/NTLArchive/NTLJacobiSymbol.py
# Compiled at: 2018-04-23 08:51:10
from .NTLCoprimalityTest import coprimalityTest
from .NTLLegendreSymbol import legendreSymbol
from .NTLPrimeFactorisation import primeFactorisation
from .NTLUtilities import jsrange, jssquare
from .NTLValidations import int_check, pos_check
__all__ = [
 'jacobiSymbol']
nickname = 'jacobi'

def jacobiSymbol(a, m):
    int_check(a, m)
    pos_check(m)
    a %= m
    if a == 1:
        return 1
    if a == m - 1:
        return (-1) ** ((m - 1) // 2)
    if a == 2:
        return (-1) ** ((m ** 2 - 1) // 8)
    if coprimalityTest(a, m) and jssquare(a):
        return 1
    p, q = primeFactorisation(m, wrap=True)
    rst = 1
    for ptr in jsrange(len(p)):
        rst *= legendreSymbol(a, p[ptr]) ** q[ptr]

    return rst