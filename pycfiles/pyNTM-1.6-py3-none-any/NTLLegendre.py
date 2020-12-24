# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/ntlib/NTLArchive/NTLLegendre.py
# Compiled at: 2018-04-23 08:51:10
from .__abc__ import __symbol__
from .NTLExceptions import DefinitionError, KeywordError
from .NTLPrimeFactorisation import primeFactorisation
from .NTLRepetiveSquareModulo import repetiveSquareModulo
from .NTLTrivialDivision import trivialDivision
from .NTLUtilities import jssign
from .NTLValidations import bool_check, prime_check, str_check
__all__ = [
 'Legendre',
 '_default_numerator', '_default_denominator',
 '_legendre_eval', '_legendre_simplify', '_legendre_reciprocate']
nickname = 'Legendre'
Symbol = __symbol__.ABCSymbol
_default_numerator = 1
_default_denominator = 2

def _legendre_eval(legendre):
    _ret = _legendre_simplify(legendre)
    a = _ret._numerator
    p = _ret._denominator
    if a == 1:
        return 1
    if a == -1:
        return (-1) ** ((p - 1) // 2)
    if a == 2:
        return (-1) ** ((p ** 2 - 1) // 8)
    r = jssign(a)
    for _a in primeFactorisation(abs(a)):
        r *= Legendre(_a, p).eval()

    if r != p - 1:
        return r
    return -1


def _legendre_simplify(legendre):
    _ret = legendre
    _ret._numerator %= _ret._denominator
    while abs(_ret._numerator) not in (0, 1, 2) and trivialDivision(abs(_ret._numerator)):
        _num = _ret._numerator
        _den = _ret._denominator
        if _den > abs(_num):
            _ret = _legendre_reciprocate(_ret)

    return _ret


def _legendre_reciprocate(legendre):
    _den = legendre._numerator
    _num = legendre._denominator * (-1) ** ((_den - 1) // 2) % _den
    if _num == _den - 1:
        _num = -1
    _ret = Legendre(_num, _den)
    return _ret


class Legendre(Symbol):

    @property
    def nickname(a):
        return a._nickname

    @property
    def numerator(a):
        return a._numerator

    @property
    def denominator(a):
        return a._denominator

    def __init__(self, numerator, denominator=None, **kwargs):
        trust = False
        for kw in kwargs:
            if kw != 'trust':
                raise KeywordError("Keyword '%s' is not defined." % kw)
            else:
                trust = kwargs[kw]
                bool_check(trust)

        prime_check(trust, self._denominator)

    def __call__(self):
        a = self._numerator
        p = self._denominator
        a %= p
        if a == 1:
            return 1
        if a == p - 1:
            return (-1) ** ((p - 1) // 2)
        if a == 2:
            return (-1) ** ((p ** 2 - 1) // 8)
        mod = repetiveSquareModulo(a, (p - 1) // 2, p)
        if mod != p - 1:
            return mod
        return -1

    def convert(self, kind=None):
        if kind is None:
            return self
        else:
            str_check(kind)
            if kind == 'Legendre':
                return self
            if kind == 'Jacobi':
                from .NTLJacobi import Jacobi
                _ret = Jacobi(self._numerator, self._denominator)
                return _ret
            raise KeywordError('%s is an unknown type of symbol.' % kind)
            return

    _nickname = 'Legendre'
    _numerator = _default_numerator
    _denominator = _default_denominator
    eval = _legendre_eval
    simplify = _legendre_simplify
    reciprocate = _legendre_reciprocate