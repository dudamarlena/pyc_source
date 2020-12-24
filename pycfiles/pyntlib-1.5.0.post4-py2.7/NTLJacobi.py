# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/ntlib/NTLArchive/NTLJacobi.py
# Compiled at: 2018-04-23 08:51:10
from .__abc__ import __symbol__
from .NTLExceptions import DefinitionError, KeywordError
from .NTLPrimeFactorisation import primeFactorisation
from .NTLTrivialDivision import trivialDivision
from .NTLUtilities import jssign
from .NTLValidations import str_check
__all__ = [
 'Jacobi',
 'default_numerator', 'default_denominator',
 'jacobi_eval', 'jacobi_simplify', 'jacobi_reciprocate']
nickname = 'Jacobi'
Symbol = __symbol__.ABCSymbol
_default_numerator = 1
_default_denominator = 2

def _jacobi_eval(jacobi):
    _ret = _jacobi_simplify(jacobi)
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
        r *= Jacobi(_a, p).eval()

    if r != p - 1:
        return r
    return -1


def _jacobi_simplify(jacobi):
    _ret = jacobi
    _ret._numerator %= _ret._denominator
    while abs(_ret._numerator) not in (0, 1, 2) and trivialDivision(abs(_ret._numerator)):
        _num = _ret._numerator
        _den = _ret._denominator
        if _den > abs(_num):
            _ret = _jacobi_reciprocate(_ret)

    return _ret


def _jacobi_reciprocate(jacobi):
    _den = jacobi._numerator
    _num = jacobi._denominator * (-1) ** ((_den - 1) // 2) % _den
    if _num == _den - 1:
        _num = -1
    _ret = Jacobi(_num, _den)
    return _ret


class Jacobi(Symbol):

    @property
    def nickname(a):
        return a._nickname

    @property
    def numerator(a):
        return a._numerator

    @property
    def denominator(a):
        return a._denominator

    def __call__(self):
        from .NTLLegendre import Legendre
        a = self._numerator
        m = self._denominator
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
            rst *= Legendre(a, p[ptr])() ** q[ptr]

        return rst

    def convert(self, kind=None):
        if kind is None:
            return self
        else:
            str_check(kind)
            if kind == 'Jacobi':
                return self
            if kind == 'Legendre':
                from .NTLLegendre import Legendre
                _ret = Legendre(self._numerator, self._denominator)
                return _ret
            raise KeywordError('%s is an unknown type of symbol.' % kind)
            return

    _nickname = 'Jacobi'
    _numerator = _default_numerator
    _denominator = _default_denominator
    eval = _jacobi_eval
    simplify = _jacobi_simplify
    reciprocate = _jacobi_reciprocate