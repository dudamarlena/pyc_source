# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/ntlib/NTLArchive/NTLPolynomial.py
# Compiled at: 2018-04-23 08:51:10
from .__abc__ import __polynomial__
import copy
from .NTLExceptions import ComplexError, DefinitionError, ResidueError, PolyError
from .NTLRepetiveSquareModulo import repetiveSquareModulo
from .NTLUtilities import jsappend, jsint, jsitems, jskeys, jsmaxint, jsrange, jsupdate, ispy3
from .NTLValidations import int_check, number_check, tuple_check
__all__ = [
 'Polynomial']
nickname = 'Polynomial'
PolyBase = __polynomial__.ABCPolynomial

class Polynomial(PolyBase):
    __all__ = [
     'iscomplex', 'isinteger', 'ismultivar', 'var', 'vector', 'dfvar', 'nickname']
    __slots__ = ('_cflag', '_iflag', '_vflag', '_var', '_vec', '_dfvar', '_nickname')

    @property
    def iscomplex(a):
        return a._cflag

    @property
    def isinteger(a):
        return a._iflag

    @property
    def ismultivar(a):
        return a._vflag

    @property
    def var(a):
        return a._var

    @property
    def vector(a):
        return a._vec

    @property
    def dfvar(a):
        return a._dfvar

    @property
    def nickname(a):
        return a._nickname

    def eval(self, *vars):

        def make_eval(_dict):
            poly = []
            for exp in _dict:
                item = str(_dict[exp]) + '*x**' + str(exp)
                poly.append(item)

            _eval = (' + ').join(poly)
            return _eval

        _rst = 0
        _var = self._read_vars(*vars)
        if _var is None:
            return 0
        else:
            if self._var == []:
                return 0
            for var in _var:
                poly = make_eval(self._vec[var])
                _rst += (lambda x: eval(poly))(_var[var])

            return _rst

    def mod(self, *vars, **mods):
        _rst = 0
        _mod = self._read_mods(**mods)
        if _mod is None:
            return self.eval(*vars)
        else:
            _var = self._read_vars(*vars)
            if _var is None:
                return 0
            if self._var == []:
                return 0
            for var in _var:
                for exp in self._vec[var]:
                    _coe = self._vec[var][exp] % _mod
                    base = _var[var]
                    _tmp = repetiveSquareModulo(base, exp, _mod)
                    _rst += _coe * _tmp % _mod

            _rst %= _mod
            return _rst

    def _update_state(self):
        for var in self._var:
            for exp in jskeys(self._vec[var]):
                if self._vec[var][exp] == 0:
                    del self._vec[var][exp]

            if self._none_check(self._vec[var]):
                self._var.remove(var)
                del self._vec[var]

        self._var.sort()
        self._vflag = True if len(self._var) > 1 else False
        for var in self._var:
            if self._complex_check(self._vec[var]):
                self._cflag = True
                break
        else:
            self._cflag = False

        if self._cflag:
            self._iflag = False
        else:
            for var in self._var:
                if not self._int_check(self._vec[var]):
                    self._iflag = False
                    break
            else:
                self._iflag = True

        self._var = self._var or [self._dfvar]
        self._vec = self._vec or {self._dfvar: {0: 0}}

    def __init__(self, other=None, *items, **kwargs):
        self._nickname = 'poly'
        self._update_state()

    def __len__(self):
        if self._vflag:
            raise PolyError('Multi-variable polynomial has no len().')
        else:
            return max(self._vec[self._var[0]]) + 1

    def __getitem__(self, key):
        if isinstance(key, str):
            if key in self._var:
                vec = {key: self._vec[key]}
                item = Polynomial(vec)
                item._dfvar = self._dfvar
            else:
                item = Polynomial()
            return item
        if isinstance(key, slice):
            return self.__getslice__(key.start, key.stop, key.step)
        int_check(key)
        if ispy3:
            if key < 0:
                key += len(self)
        if self._vflag:
            raise PolyError("Multi-variable polynomial has no attribute '__getitem__'.")
        else:
            try:
                return self._vec[self._var[0]][key]
            except KeyError:
                return 0

    def __setitem__(self, key, value):
        if isinstance(key, str):
            tuple_check(value)
            _ec = {}
            for item in value:
                tuple_check()
                if len(item) != 2:
                    raise DefinitionError('Tuple of coeffients and corresponding exponents in need.')
                _ec[item[0]] = item[1]

            jsappend(self._var, key)
            self._vec[key] = _ec
        elif isinstance(key, slice):
            self.__setslice__(key.start, key.stop, key.step, value)
        else:
            int_check(key)
            number_check(value)
            if ispy3:
                if key < 0:
                    key += len(self)
            if self._vflag:
                raise PolyError('Multi-variable polynomial does not support item assignment.')
            if key in self._vec[self._var[0]] and value == 0:
                del self._vec[self._var[0]][key]
            else:
                self._vec[self._var[0]][key] = value
        self._update_state()

    def __delitem__(self, key):
        if isinstance(key, str):
            if key in self._var:
                self._var.remove(key)
                del self._vec[key]
        elif isinstance(key, slice):
            self.__delslice__(key.start, key.stop, key.step)
        else:
            int_check(key)
            if self._vflag:
                raise PolyError('Multi-variable polynomial does not support item deletion.')
            try:
                del self._vec[self._var[0]][key]
            except KeyError:
                pass

        self._update_state()

    def __contains__(self, poly):
        if isinstance(poly, Polynomial):
            if poly._var in self._var:
                for var in poly._var:
                    for key in poly._vec[var]:
                        try:
                            if poly._vec[var][key] == self._vec[var][key]:
                                continue
                            else:
                                return False
                        except KeyError:
                            return False

            else:
                return False
        else:
            return Polynomial(poly) in self

    def __getslice__(self, i, j, k=None):
        if i is None:
            i = 0
        if j is None:
            j = len(self)
        if k is None:
            k = 1
        int_check(i, j, k)
        if self._vflag:
            raise PolyError("Multi-variable polynomial has no attribute '__getitem__'.")
        if j == jsmaxint:
            j = len(self)
        _list = [
         self._var[0]]
        for ptr in jsrange(i, j, k):
            try:
                _list.append((ptr, self._vec[self._var[0]][ptr]))
            except KeyError:
                pass

        poly = Polynomial(tuple(_list))
        return poly

    def __setslice__(self, i, j, k, coe=None):
        if coe is None:
            if i is None:
                i = 0
            if j is None:
                j = len(self)
            int_check(i, j)
            tuple_check(k)
            if self._vflag:
                raise PolyError('Multi-variable polynomial does not support item assignment.')
            coe = k
            j = i + len(coe)
            for ptr in jsrange(i, j):
                if ptr in self._vec[self._var[0]] and coe[(ptr - i)] == 0:
                    del self._vec[self._var[0]][ptr]
                else:
                    self._vec[self._var[0]][ptr] = coe[(ptr - i)]

            self._update_state()
        else:
            if i is None:
                i = 0
            if j is None:
                j = len(self)
            if k is None:
                k = 1
            int_check(i, j, k)
            tuple_check(coe)
            if self._vflag:
                raise PolyError('Multi-variable polynomial does not support item assignment.')
            j = i + len(coe) * k
            ctr = -1
            for ptr in jsrange(i, j, k):
                ctr += 1
                if ptr in self._vec[self._var[0]] and coe[ctr] == 0:
                    del self._vec[self._var[0]][ptr]
                else:
                    self._vec[self._var[0]][ptr] = coe[ctr]

            self._update_state()
        return

    def __delslice__(self, i, j, k=None):
        if i is None:
            i = 0
        if j is None:
            j = len(self)
        if k is None:
            k = 1
        int_check(i, j, k)
        if self._vflag:
            raise PolyError('Multi-variable polynomial does not support item deletion.')
        if j == jsmaxint:
            j = len(self)
        for ptr in range(i, j, k):
            try:
                del self._vec[self._var[0]][ptr]
            except KeyError:
                pass

        self._update_state()
        return

    def _add(self, poly):
        if isinstance(poly, Polynomial):
            _sum = copy.deepcopy(self)
            _sum._var = jsappend(_sum._var, poly._var)
            _sum._vec = jsupdate(self._vec, poly._vec)
            _sum._update_state()
        else:
            _sum = self + Polynomial(poly)
        return _sum

    def radd(self, poly):
        rsum = poly + self
        return rsum

    __add__ = _add
    __radd__ = radd

    def _sub(self, poly):
        if isinstance(poly, Polynomial):
            _dif = copy.deepcopy(self)
            _poly = -poly
            _dif._var = jsappend(_dif._var, poly._var)
            _dif._vec = jsupdate(self._vec, _poly._vec)
            _dif._update_state()
        else:
            _dif = self - Polynomial(poly)
        return _dif

    def rsub(self, poly):
        rdif = poly - self
        return rdif

    __sub__ = _sub
    __rsub__ = rsub

    def _mul(self, poly):
        if isinstance(poly, Polynomial):
            if self._vflag:
                raise PolyError('Multi-variable polynomial does not support multiplication.')
            elif self._var == poly._var:
                _pro = copy.deepcopy(self)
                vec = {}
                _ec = {}
                for exp_a in self._vec[self._var[0]]:
                    for exp_b in poly._vec[poly._var[0]]:
                        exp = exp_a + exp_b
                        coe = self._vec[self._var[0]][exp_a] * poly._vec[poly._var[0]][exp_b]
                        _ec[exp] = coe

                vec[self._var[0]] = _ec
                _pro = Polynomial(vec)
            else:
                raise PolyError('No support for multi-variable multiplication.')
        else:
            _pro = self * Polynomial(poly)
        return _pro

    def rmul(self, poly):
        rpro = poly * self
        return rpro

    __mul__ = _mul
    __rmul__ = rmul

    def _div(self, poly):
        if poly == 1:
            return self
        if poly == 0:
            raise ResidueError('integer division or modulo by zero')
        if ispy3 and self._iflag and poly._iflag:
            _quo = self // poly
            return _quo
        if isinstance(poly, Polynomial):
            if self._vflag:
                raise PolyError('Multi-variable polynomial does not support division.')
            else:
                if self._var == poly._var:
                    _var = self._var[0]
                    _vec = {_var: {}}
                    _did = copy.deepcopy(poly)
                    _rem = copy.deepcopy(self)
                    a_expmax = max(self._vec[_var])
                    b_exp = sorted(jskeys(_did._vec[_var]), reverse=True)
                    while a_expmax >= b_exp[0]:
                        quo_coe = _rem._vec[_var][a_expmax] / _did._vec[_var][b_exp[0]]
                        quo_exp = a_expmax - b_exp[0]
                        _vec[_var][quo_exp] = quo_coe
                        for exp in b_exp:
                            rem_exp = exp + quo_exp
                            rem_coe = _did._vec[_var][exp] * quo_coe
                            try:
                                _rem._vec[_var][rem_exp] -= rem_coe
                            except KeyError:
                                _rem._vec[_var][rem_exp] = -rem_coe

                        _rem._update_state()
                        try:
                            a_expmax = max(_rem._vec[_var])
                        except ValueError:
                            break

                    _quo = Polynomial(_vec)
                    return _quo
                raise PolyError('No support for multi-variable division.')
        else:
            _quo = self / Polynomial(poly)
            return _quo

    def rdiv(self, poly):
        rquo = poly / self
        return rquo

    __truediv__ = _div
    __rtruediv__ = rdiv
    if not ispy3:
        __div__ = _div
        __rdiv__ = rdiv

    def _divmod(self, poly):
        if isinstance(poly, Polynomial):
            if self._vflag:
                raise PolyError('Multi-variable polynomial does not support division & modulo.')
            else:
                if poly == 1:
                    return (self, 0)
                if poly == 0:
                    raise ResidueError('integer division or modulo by zero')
                if self._var == poly._var:
                    _var = self._var[0]
                    _vec = {_var: {}}
                    _did = copy.deepcopy(poly)
                    _rem = copy.deepcopy(self)
                    a_expmax = max(self._vec[_var])
                    b_exp = sorted(jskeys(_did._vec[_var]), reverse=True)
                    if _did._vec[_var][b_exp[0]] != 1:
                        _coe = _did._vec[_var][b_exp[0]]
                        if self._vec[_var][a_expmax] % _coe == 0:
                            _mul = self._vec[_var][a_expmax] // _coe
                            if self == _did * _mul:
                                _quo = Polynomial(_mul)
                                _rem = Polynomial()
                                return (
                                 _quo, _rem)
                        for exp in b_exp:
                            if _did._vec[_var][exp] % _coe != 0:
                                _quo = Polynomial()
                                _rem = copy.deepcopy(self)
                                return (
                                 _quo, _rem)
                            _did._vec[_var][exp] //= _coe

                        for key in self._vec[_var]:
                            if self._vec[_var][key] % _coe != 0:
                                _quo = Polynomial()
                                _rem = copy.deepcopy(self)
                                return (
                                 _quo, _rem)
                            _rem._vec[_var][key] //= _coe

                    while a_expmax >= b_exp[0]:
                        quo_coe = _rem._vec[_var][a_expmax]
                        quo_exp = a_expmax - b_exp[0]
                        _vec[_var][quo_exp] = quo_coe
                        for exp in b_exp:
                            rem_exp = exp + quo_exp
                            rem_coe = _did._vec[_var][exp] * quo_coe
                            try:
                                _rem._vec[_var][rem_exp] -= rem_coe
                            except KeyError:
                                _rem._vec[_var][rem_exp] = -rem_coe

                        _rem._update_state()
                        try:
                            a_expmax = max(_rem._vec[_var])
                        except (ValueError, KeyError):
                            break

                    _quo = Polynomial(_vec)
                    return (
                     _quo, _rem)
                raise PolyError('No support for multi-variable division & modulo.')
        else:
            _quo, _rem = self._divmod(Polynomial(poly))
            return (_quo, _rem)

    def rdivmod(self, poly):
        _quo, _rem = divmod(poly, self)
        return (_quo, _rem)

    __divmod__ = _divmod
    __rdivmod__ = rdivmod

    def _floordiv(self, poly):
        _quo = self._divmod(poly)[0]
        return _quo

    def rfloordiv(self, poly):
        rquo = poly // self
        return rquo

    __floordiv__ = _floordiv
    __rfloordiv__ = rfloordiv

    def _mod(self, poly):
        _rem = self._divmod(poly)[1]
        return _rem

    def rmod(self, poly):
        rrem = poly % self
        return rrem

    __mod__ = _mod
    __rmod__ = rmod

    def _pow(self, exp, mod=None):
        int_check(exp)
        _pow = copy.deepcopy(self)
        for ctr in jsrange(1, exp):
            _pow *= _pow

        if mod is not None:
            int_check(mod)
            _pow %= _mod
        return _pow

    __pow__ = _pow

    def _neg(self):
        _neg = copy.deepcopy(self)
        for var in _neg._vec:
            for exp in _neg._vec[var]:
                _neg._vec[var][exp] = -_neg._vec[var][exp]

        return _neg

    def _pos(self):
        _pos = copy.deepcopy(self)
        return _pos

    def _abs(self):
        _abs = copy.deepcopy(self)
        for var in _abs._vec:
            for exp in _abs._vec[var]:
                _neg._vec[var][exp] = abs(_neg._vec[var][exp])

        return _abs

    __neg__ = _neg
    __pos__ = _pos
    __abs__ = _abs

    def _der(self):
        vec = {}
        _ec = {}
        for var in self._vec:
            for exp in self._vec[var]:
                if exp:
                    _exp = exp - 1
                    _coe = self._vec[var][exp] * exp
                else:
                    _exp = 0
                    _coe = 0
                _ec[_exp] = _coe

            vec[var] = _ec

        _der = Polynomial(vec)
        return _der

    def _int(self):
        vec = {}
        _ec = {}
        for var in self._vec:
            for exp in self._vec[var]:
                _exp = exp + 1
                if exp:
                    if ispy3:
                        _coe = self._vec[var][exp] / key
                    else:
                        _coe = 1.0 * self._vec[var][exp] / key
                else:
                    _coe = self._vec[var][exp]
                _ec[_exp] = [
                 _coe]

            vec[var] = _ec

        _int = Polynomial(vec)
        return _int

    polyder = _der
    polyint = _int

    def __eq__(self, other):
        if isinstance(other, Polynomial):
            return self._var == other._var and self._vec == other._vec
        else:
            return self == Polynomial(other)

    def __ne__(self, poly):
        return not self == poly

    def __lt__(self, poly):
        if self.has_sametype(poly):
            if self._cflag or poly._cflag:
                raise ComplexError('No ordering relation is defined for complex polynomial.')
            if self._vflag or poly._vflag:
                raise PolyError('No ordering relation is defined for multi-variable polynomial.')
            if len(self) > len(poly):
                return False
            if len(self) < len(poly):
                return True
            a_ec = self._vec[self._var[0]]
            b_ec = poly._vec[poly._var[0]]
            for ptr in jsrange(len(self), -1, -1):
                try:
                    if ptr in a_ec and ptr not in b_ec:
                        return False
                    if a_ec[ptr] > b_ec[ptr]:
                        return False
                except KeyError:
                    continue

            return True
        return self < Polynomial(poly)

    def __le__(self, poly):
        return self == poly or self < poly

    def __gt__(self, poly):
        return not self <= poly

    def __ge__(self, poly):
        return not self < poly

    def __reduce__(self):
        return (
         self.__class__, (str(self),))

    def __copy__(self):
        if type(self) == Polynomial:
            return self
        return self.__class__(self._vec, dfvar=self._dfvar)

    def __deepcopy__(self, memo):
        if type(self) == Polynomial:
            return self
        return self.__class__(self._vec, dfvar=self._dfvar)