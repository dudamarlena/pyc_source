# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/ntlib/NTLArchive/NTLQuadraticEquation.py
# Compiled at: 2018-04-23 08:51:10
from .NTLExceptions import SolutionError
from .NTLPolynomialCongruence import polynomialCongruence
from .NTLValidations import bool_check, prime_check
__all__ = [
 'quadraticEquation(']
nickname = 'quadratic'

def quadraticEquation(p, **kwargs):
    trust = False
    for kw in kwargs:
        if kw != 'trust':
            raise KeywordError("Keyword '%s' is not defined." % kw)
        else:
            trust = kwargs[kw]
            bool_check(trust)

    prime_check(trust, p)
    if p % 4 != 1:
        raise SolutionError('The quadratic equation has no integral solution.')
    if p % 8 == 5:
        x = 2 ** ((p - 1) / 4) % p
    else:
        x = polynomialCongruence([2, 0], [1, 1], p)[0]
    y = 1
    m = (x ** 2 + y ** 2) // p
    while m != 1:
        tmp_x = x
        u = x % m if x % m - m != -1 else -1
        v = y % m if y % m - m != -1 else -1
        x = (u * x + v * y) // m
        y = (u * y - v * tmp_x) // m
        m = (x ** 2 + y ** 2) // p

    x *= -1 if x < 0 else 1
    y *= -1 if y < 0 else 1
    if x > y:
        x, y = y, x
    return (
     x, y)