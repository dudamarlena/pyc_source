# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/ntlib/NTLArchive/NTLCarmichealTest.py
# Compiled at: 2018-04-23 08:51:10
from .NTLPrimeFactorisation import primeFactorisation
from .NTLValidations import int_check, pos_check, odd_check
__all__ = [
 'carmichealTest']
nickname = 'carmicheal'

def carmichealTest(n):
    int_check(n)
    pos_check(n)
    odd_check(n)
    p, q = primeFactorisation(n, wrap=True)
    if len(p) < 3:
        return False
    for qitem in q:
        if qitem > 1:
            return False

    for pitem in p:
        if (n - 1) % (pitem - 1) != 0:
            return False

    return True