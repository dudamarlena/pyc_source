# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/ntlib/NTLArchive/NTLQuadratic.py
# Compiled at: 2018-04-23 08:51:10
import copy, numbers
from .NTLCongruence import Congruence, Solution
from .NTLExceptions import DefinitionError, PCError, PolyError
from .NTLPolynomial import Polynomial
from .NTLPrimeFactorisation import primeFactorisation
from .NTLTrivialDivision import trivialDivision
from .NTLUtilities import jskeys, jssquare
from .NTLValidations import str_check, tuple_check
__all__ = [
 'Quadratic']
nickname = 'Quadratic'

class Quadratic(Polynomial):
    __all__ = [
     'constant', 'isprime', 'solution', 'iscomplex', 'isinteger', 'ismultivar',
     'var', 'vector', 'dfvar', 'nickname']
    __slots__ = ('_constant', '_pflag', '_solution', '_cflag', '_iflag', '_vflag',
                 '_var', '_vec', '_dfvar', '_nickname')

    @property
    def constant(a):
        return a._constant

    @property
    def isprime(a):
        return a._pflag

    @property
    def solution(a):
        if a._solution is None:
            return a.solve()
        else:
            return a._solution
            return

    def __new__(cls, other=None, *items, **mods):
        try:
            trust = mods.pop('trust')
        except KeyError:
            trust = False

        if isinstance(other, Quadratic):
            self = copy.deepcopy(other)
            return self
        else:
            if isinstance(other, numbers.Number):

                def _read_name(**mods):
                    for name in mods:
                        if name == 'vars':
                            tuple_check(mods[name])
                            if len(mods[name]) != 2:
                                raise DefinitionError('Only takes two variable names.')
                            v_1 = mods[name][0]
                            v_2 = mods[name][1]
                            str_check(v_1, v_2)
                            _var = (v_1, v_2)
                            break
                        else:
                            raise KeywordError("Keyword '%s' is not defined." % kw)
                    else:
                        _var = ('x', 'y')

                    return _var

                v_1, v_2 = _read_name(**mods)
                vec = {v_1: {2: 1}, v_2: {2: 1}}
                self = super(Quadratic, cls).__new__(cls, vec, **mods)
                self._pflag = True if trust else trivialDivision(other)
                self._constant = other
                self._solution = None
                return self
            else:
                self = super(Quadratic, cls).__new__(cls, other, *items, **mods)
                self._pflag = True if trust else None
                self._constant = None
                return self

            return

    def __init__(self, other=None, *items, **mods):
        self._update_state()
        self._nickname = 'quad'
        if len(self._var) != 2:
            raise PolyError('Quadratic must take two variables.')

        def _extract(_dict):
            ctr = 0
            for var in _dict:
                for exp in jskeys(_dict[var]):
                    if exp == 0:
                        self._constant = -_dict[var][exp]
                        ctr += 1
                        del _dict[exp]
                    if ctr > 1:
                        raise DefinitionError('Invalid literal for Quadratic.')

        _extract(self._vec)
        v_1 = self._var[0]
        v_2 = self._var[1]
        vec = {v_1: {2: 1}, v_2: {2: 1}}
        if self._vec != vec:
            raise DefinitionError('Invalid literal for Quadratic.')
        if self._constant is None:
            raise DefinitionError('Invalid literal for Quadratic.')
        if self._pflag is None:
            self._pflag = trivialDivision(self._constant)
        return

    def __str__(self):
        return '%s^2 + %s^2 = %d' % (self._var[0], self._var[1], self._constant)

    def solve(self):
        _mul = 1
        if not self._pflag:
            _p, _q = primeFactorisation(self._constant, wrap=True)
            for item in zip(_p, _q):
                if item[1] % 2 == 1:
                    p = item[0]
                    q = self._constant // p
                    if jssquare(q):
                        break
            else:
                _var = self._var
                _mod = self._modulo
                _rem = []
                _ret = Solution(_var, _mod, _rem, True)
                return _ret

        else:
            p = self._constant
        if p % 4 != 1:
            _var = self._var
            _mod = None
            _rem = []
            _ret = Solution(_var, _mod, _rem)
            return _ret
        else:
            if p % 8 == 5:
                x = 2 ** ((p - 1) // 4) % p
            else:
                x = Congruence(((2, 1), (0, 1)), mod=p).solution[0]
            y = 1
            m = (x ** 2 + y ** 2) // p
            while m != 1:
                tmp_x = x
                u = x % m
                if u - m == -1:
                    u = -1
                v = y % m
                if v - m == -1:
                    v = -1
                x = (u * x + v * y) // m
                y = (u * y - v * tmp_x) // m
                m = (x ** 2 + y ** 2) // p

            x *= _mul
            y *= _mul
            _var = self._var
            _mod = None
            _rem = [abs(x), abs(y)]
            _ret = Solution(_var, _mod, _rem, True)
            return _ret