# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
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