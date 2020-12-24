# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/ntlib/NTLArchive/NTLOrder.py
# Compiled at: 2018-04-23 08:51:10
from .NTLCoprimalityTest import coprimalityTest
from .NTLExceptions import DefinitionError
from .NTLPolynomial import Polynomial
from .NTLUtilities import jsrange
from .NTLValidations import int_check, prime_check
__all__ = [
 'order']
nickname = 'ord'

def order(m, a):
    if isinstance(m, Polynomial) or isinstance(a, Polynomial):
        m = Polynomial(m)
        prime_check(a)
        deg = a ** len(m)
        a = Polynomial('x')
    else:
        int_check(m, a)
        if not coprimalityTest(a, m):
            raise DefinitionError('The arguments must be coprime.')
        deg = m
    for e in jsrange(deg, 1, -1):
        if a ** e % m == 1:
            return e