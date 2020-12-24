# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/ntlib/NTLArchive/NTLCongruence.py
# Compiled at: 2018-04-23 08:51:10
import copy
from .NTLBezoutEquation import bezoutEquation
from .NTLExceptions import DefinitionError, PCError, PolyError, SolutionError
from .NTLGreatestCommonDivisor import greatestCommonDivisor
from .NTLPolynomial import Polynomial
from .NTLPrimeFactorisation import primeFactorisation
from .NTLRepetiveSquareModulo import repetiveSquareModulo
from .NTLTrivialDivision import trivialDivision
from .NTLUtilities import jsmaxint, jsrange
from .NTLValidations import int_check, number_check
__all__ = [
 'Congruence', 'Solution']
nickname = 'Congruence'

class Congruence(Polynomial):
    __all__ = [
     'modulo', 'isprime', 'solution', 'iscomplex', 'isinteger',
     'ismultivar', 'var', 'vector', 'dfvar', 'nickname']
    __slots__ = ('_modulo', '_pflag', '_solution', '_cflag', '_iflag', '_vflag', '_var',
                 '_vec', '_dfvar', '_nickname')

    @property
    def modulo(a):
        return a._modulo

    @property
    def isprime(a):
        return a._pflag

    @property
    def solution(a):
        if a._solution is None:
            return a._solve()
        else:
            return a._solution
            return

    def __new__(cls, other=None, *items, **mods):
        try:
            trust = mods.pop('trust')
        except KeyError:
            trust = False

        if isinstance(other, Congruence):
            self = copy.deepcopy(other)
        elif isinstance(other, Polynomial):
            self = copy.deepcopy(other)
            self._modulo = None
            self._pflag = True if trust else None
            self._solution = None
        else:
            self = super(Congruence, cls).__new__(cls, other, *items, **mods)
            self._modulo = None
            self._pflag = True if trust else None
            self._solution = None
        return self

    def __init__(self, other=None, *items, **mods):
        self._update_state()
        self._nickname = 'cong'
        if self._modulo is None:
            self._modulo = self._read_mods(**mods)
            if self._modulo is None:
                raise DefinitionError('The modulo of congruence is missing.')
        if self._pflag is None:
            self._pflag = trivialDivision(self._modulo)
        return

    def __call__(self, *vars):
        var = self._read_vars(*vars)
        if var is None:
            return self.solution
        else:
            _mod = self._modulo
            return self._eval(var, mod=_mod)
            return

    def __repr__(self):
        _ret = '%s(%s, mod=%d)'
        name = self.__class__.__name__
        _var = (', ').join(self._var)
        _mod = self._modulo
        return _ret % (name, _var, _mod)

    def __str__(self):
        _str = super(Congruence, self).__str__()
        _str += ' ≡ 0 (mod %d)' % self._modulo
        return _str

    def _eval(self, *vars):
        _mod = self._modulo
        return self.mod(mod=_mod, *vars)

    def _calc(self, *vars):
        _ret = super(Congruence, self).eval(*vars)
        return _ret

    def _simplify(self):
        if self._vflag:
            raise PolyError('Multi-variable congruence dose not support simplification.')
        if not self._iflag:
            raise PolyError('Non-integral congruence does not support simplification.')
        if not self._pflag:
            raise PCError('Composit-modulo congruence does not support simplification.')
        _mod = self._modulo
        _var = self._var[0]
        dvs_cong = Congruence((_var, (_mod, 1), (1, -1)), mod=_mod)
        rst_cong = self % dvs_cong
        return rst_cong

    def _solve(self):
        if self._vflag:
            raise PolyError('Multi-variable congruence dose not support solution.')
        if not self._iflag:
            raise PolyError('Non-integral congruence does not support solution.')
        if self._pflag:
            return self._prime()
        else:
            return self._composit()

    def _prime(self):
        _rem = []
        rem = self._simplify()
        for x in jsrange(rem._modulo):
            if rem._eval(x) == 0:
                _rem.append(x)

        _var = self._var
        _mod = self._modulo
        _ret = Solution(_var, _mod, _rem)
        return _ret

    def _composit(self):
        p, q = primeFactorisation(self._modulo, wrap=True)
        if len(p) == 1:
            tmpMod = p[0]
            tmpExp = q[0]
            _rem = self._primeLite(tmpMod, tmpExp)
        else:
            tmpRem = []
            tmpMod = []
            for ptr in jsrange(len(p)):
                tmpModVar = p[ptr]
                tmpExpVar = q[ptr]
                tmpMod.append(tmpModVar ** tmpExpVar)
                tmpRem.append(self._primeLite(tmpModVar, tmpExpVar))

            _rem = self._CTR(tmpRem, tmpMod)
        _var = self._var
        _mod = self._modulo
        _ret = Solution(_var, _mod, _rem)
        return _ret

    def _primeLite(self, mod, exp):
        tmpCgc = copy.deepcopy(self)
        tmpCgc._modulo = mod
        tmpCgc._pflag = True
        tmpRem = tmpCgc._prime()[:]
        if exp == 1:
            return tmpRem
        _rem = tmpCgc._primePro(tmpRem, exp)
        return _rem

    def _primePro(self, rem, exp):
        mod = self._modulo
        drv = self._der()
        for tmpRem in rem:
            if greatestCommonDivisor(drv.mod(tmpRem), mod) == 1:
                x = tmpRem
                drvMod = drv.mod(x, mod=mod) - mod
                drvRcp = 1 // drvMod
                break

        for ctr in jsrange(0, exp):
            t = -self._calc(x) // mod ** ctr * drvRcp % mod
            x += t * mod ** ctr % mod ** (ctr + 1)

        return [
         x]

    def _CTR(self, rem, mod):
        modulo = self._modulo
        bList = []
        for tmpMod in mod:
            M = modulo // tmpMod
            t = bezoutEquation(M, tmpMod)[0]
            bList.append(t * M)

        _rem = self._iterCalc(rem, bList)
        return _rem

    def _iterCalc(self, ognList, coeList):
        ptrList = []
        lvlList = []
        for tmpList in ognList:
            ptrList.append(len(tmpList) - 1)
            lvlList.append(len(tmpList) - 1)

        flag = True
        rstList = []
        modulo = self._modulo
        while flag:
            ptrNum = 0
            rstNum = 0
            for ptr in ptrList:
                rstNum += ognList[ptrNum][ptr] * coeList[ptrNum]
                ptrNum += 1

            x = rstNum % modulo
            rstList.append(x)
            ptrList, flag = self._updateState(ptrList, lvlList)

        return rstList

    def _updateState(self, ptrList, lvlList):
        ptr = 0
        flag = True
        glbFlag = True
        while flag:
            if ptrList[ptr] > 0:
                ptrList[ptr] -= 1
                flag = False
            elif ptr < len(lvlList) - 1:
                ptrList[ptr] = lvlList[ptr]
                ptr += 1
            else:
                flag = False
                glbFlag = False

        return (ptrList, glbFlag)

    calc = _calc
    eval = _eval
    simplify = _simplify
    solve = _solve

    def __reduce__(self):
        return (
         self.__class__, (str(self),))

    def __copy__(self):
        if type(self) == Congruence:
            return self
        return self.__class__(self._vec, mod=self._modulo, dfvar=self._dfvar)

    def __deepcopy__(self, memo):
        if type(self) == Congruence:
            return self
        return self.__class__(self._vec, mod=self._modulo, dfvar=self._dfvar)


class Solution(object):
    __all__ = [
     'var', 'mod', 'rem', 'qflag']
    __slots__ = ('_var', '_mod', '_rem', '_qflag')

    @property
    def variables(a):
        return a._var

    @property
    def modulo(a):
        return a._mod

    @property
    def solutions(a):
        return a._rem

    def __new__(cls, var, mod, rem, qflag=None):
        self = super(Solution, cls).__new__(cls)
        self._var = var
        self._mod = mod
        self._rem = sorted(rem)
        if qflag is None:
            self._qflag = False
        else:
            self._qflag = qflag
        return self

    def __call__(self):
        return self._rem

    def __repr__(self):
        _ret = 'Solution(%s, %d)' % (self._var, self._mod)
        return _ret

    def __str__(self):

        def _make_str(_list):
            _ret = []
            for item in _list:
                _ret.append(str(item))

            return _ret

        if self._qflag:
            x = self._var[0]
            y = self._var[1]
            a = self._rem[0]
            b = self._rem[1]
            _str = '%s = ±%d\t%s = ±%d' % (x, a, y, b)
        else:
            if len(self._rem) == 0:
                return 'No solution for %s modulo %d' % (self._var, self._mod)
            _rem = _make_str(self._rem)
            _str = '%s ≡ ' % self._var[0]
            _str += (', ').join(_rem)
            _str += ' (mod %d)' % self._mod
        return _str

    def __len__(self):
        return len(self._rem)

    def __getitem__(self, _key):
        if isinstance(_key, str):
            if self._qflag:
                try:
                    return self._rem[self._var.find(_key)]
                except IndexError:
                    return

            else:
                if _key in self._var:
                    return self._rem
                else:
                    return []

        else:
            if isinstance(_key, slice):
                return self.__getslice__(_key.start, _key.stop, _key.step)
            int_check(_key)
            try:
                return self._rem[_key]
            except IndexError:
                raise SolutionError('Only %d solutions found.' % len(self._rem))

        return

    def __getslice__(self, i, j, k=None):
        if i is None:
            i = 0
        if j is None:
            j = len(self)
        if k is None:
            k = 1
        int_check(i, j, k)
        if j == jsmaxint:
            j = len(self)
        _list = []
        for ptr in jsrange(i, j, k):
            try:
                _list.append(self._rem[ptr])
            except IndexError:
                pass

        return _list

    def __reduce__(self):
        return (
         self.__class__, (str(self),))

    def __copy__(self):
        if type(self) == Congruence:
            return self
        return self.__class__(self._vec, self._mod, self._rem)

    def __deepcopy__(self, memo):
        if type(self) == Congruence:
            return self
        return self.__class__(self._vec, self._mod, self._rem)