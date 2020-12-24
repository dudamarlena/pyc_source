# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
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