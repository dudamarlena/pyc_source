# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/ntlib/NTLArchive/NTLIndex.py
# Compiled at: 2018-04-23 08:51:10
from .NTLEulerFunction import eulerFunction
from .NTLPrimitiveRoot import primitiveRoot
from .NTLRepetiveSquareModulo import repetiveSquareModulo
from .NTLUtilities import jsrange
from .NTLValidations import int_check, pos_check
__all__ = [
 'Index']
nickname = 'Index'

class Index:
    __all__ = [
     '_mul', '_mod', '_pmr', '_phi', '_ind', '_tab']

    @property
    def modulo(a):
        return a._mod

    @property
    def root(a):
        return a._pmr

    @property
    def phi(a):
        return a._phi

    @property
    def index(a):
        return a._ind

    @property
    def table(a):
        return a._tab

    def __init__(self, modulo):
        int_check(modulo)
        pos_check(modulo)
        self._mul = []
        self._mod = modulo
        self._pmr = primitiveRoot(modulo)[0]
        self._phi = eulerFunction(self._mod)
        self._ind = self._make_index()
        self._tab = self._make_table()

    def __call__(self, *args):
        self._mul = []
        for _int in args:
            int_check(_int)
            if _int == 0:
                return 0
            self._mul.append(_int)

        if self._mul == []:
            return None
        else:
            _product = self._calc_multi()
            return _product

    def __repr__(self):
        return 'Index(%d)' % self_.mod

    def __str__(self):
        string = '\t0\t1\t2\t3\t4\t5\t6\t7\t8\t9'
        for i in jsrange(len(self._tab)):
            string += '\n%d\t' % i
            for j in self._tab[i]:
                if j == 0:
                    string += '\t'
                else:
                    string += '%d\t' % j

            string = string[:-1]

        return string

    def _make_index(self):
        _ind = [
         0] * self._mod
        for _num in jsrange(1, self._mod):
            ptr = repetiveSquareModulo(self._pmr, _num, self._mod)
            _ind[ptr] = _num

        return _ind

    def _make_table(self):
        _tab = []
        for ctr in jsrange(0, self._phi + 1, 10):
            _tab.append([0, 0, 0, 0, 0, 0, 0, 0, 0, 0])

        for ptr in jsrange(1, self._mod):
            _tab[(ptr // 10)][ptr % 10] = self._ind[ptr]

        return _tab

    def _calc_multi(self):
        _all_index = 0
        for _mul in self._mul:
            _all_index += self._ind[(_mul % self._mod)]

        _product = self._pmr ** (_all_index % self._phi) % self._mod
        return _product