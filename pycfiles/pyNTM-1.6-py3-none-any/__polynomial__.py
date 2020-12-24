# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/ntlib/NTLArchive/__abc__/__polynomial__.py
# Compiled at: 2018-04-23 08:51:10
import abc, copy, numbers, operator, re, sys
from ..NTLExceptions import DefinitionError, KeywordError
from ..NTLUtilities import jsappend, jsint, jskeys, jsstring, jsupdate
from ..NTLValidations import basestring_check, dict_check, int_check, pos_check, notneg_check, number_check, str_check, tuple_check
__all__ = [
 'ABCPolynomial']
ABCMeta = abc.ABCMeta
abstractmethod = abc.abstractmethod
abstractproperty = abc.abstractproperty
POLYNOMIAL_FORMAT = re.compile('\n    \\A\\s*                       # optional whitespace at the start, then\n    (?P<sgn_>[-+]?)             # an optional sign, and\n    \\s*                         # optional whitespace after sign, then\n    (?=\\d)?                     # lookahead for digit\n    (?P<coe_>\\d+)?              # coefficient\n    (?:\\*)?                     # followed by an optional asterisk/multiplier, then\n    (?=[A-Z_])?                 # lookahead for non-digit/letter\n    (?P<var_>\\w+)?              # variable\n    (?:(?:\\^)?|(?:\\*\\*))?       # followed by an optional caret or double asterisk, then\n    (?=\\d)?                     # lookahead for digit\n    (?P<exp_>\\d+)?              # exponent\n    \\s*\\Z                       # and optional whitespace to finish\n', re.VERBOSE | re.IGNORECASE)

class ABCPolynomial(object):
    __all__ = [
     'var', 'vector', 'dfvar', 'nickname']
    __metaclass__ = ABCMeta
    __hash__ = None

    @abstractproperty
    def var(a):
        pass

    @abstractproperty
    def vector(a):
        pass

    @abstractproperty
    def dfvar(a):
        pass

    @abstractproperty
    def nickname(a):
        pass

    @abstractmethod
    def eval(self, *vars):
        pass

    @abstractmethod
    def mod(self, *vars, **mods):
        pass

    def has_sametype(self, other):
        return isinstance(other, self.__class__)

    def default(self, var=None):
        if var is None:
            self._dfvar = _dfvar
        else:
            str_check(var)
            self._dfvar = var
        return

    @staticmethod
    def _complex_check(_dict):
        for _key in _dict:
            if isinstance(_dict[_key], complex):
                _cflag = True
                break
        else:
            _cflag = False

        return _cflag

    @staticmethod
    def _int_check(_dict):
        for _key in _dict:
            if not isinstance(_dict[_key], jsint):
                _iflag = False
                break
        else:
            _iflag = True

        return _iflag

    @staticmethod
    def _none_check(_dict):
        if _dict == {}:
            return True
        for _key in _dict:
            if _dict[_key] != 0:
                return False

        return True

    @staticmethod
    def _read_item(item):
        m = POLYNOMIAL_FORMAT.match(item)
        if m is None:
            raise DefinitionError('Invalid literal for symbols: %r' % item)
        t_v = m.group('var_')
        t_c = m.group('coe_')
        t_e = m.group('exp_')
        if t_v is None:
            var = None
            coe = int(t_c)
            exp = 0
        else:
            var = t_v
            coe = 1 if t_c is None else int(t_c)
            exp = 1 if t_e is None else int(t_e)
        if m.group('sgn_') == '-':
            coe = -coe
        return (
         var, exp, coe)

    @staticmethod
    def _read_dict(vec):
        _var = []
        _vec = {}
        for var in vec:
            str_check(var)
            dict_check(vec[var])
            for exp in vec[var]:
                int_check(exp)
                number_check(vec[var][exp])

            _var.append(var)

        _vec.update(vec)
        return (
         _var, _vec)

    def _read_poly(self, poly):
        tuple_check(poly)
        var = []
        vec = {}
        ec = {}
        if isinstance(poly[0], str):
            _vec = list(poly)
            _vec.reverse()
            _var = _vec.pop()
            var.append(_var)
        else:
            _var = self._dfvar
            _vec = list(poly)
            var.append(_var)
        for _ec in _vec:
            tuple_check(_ec)
            if len(_ec) != 2:
                raise DefinitionError('Tuple of coeffients and corresponding exponents in need.')
            _exp = _ec[0]
            int_check(_exp)
            notneg_check(_exp)
            _coe = _ec[1]
            number_check(_coe)
            jsupdate(ec, {_exp: _coe})

        if _var in vec:
            vec[_var] = jsupdate(vec[_var], ec)
        else:
            vec[_var] = ec
        return (var, vec)

    def _read_mods(self, **mods):
        _mod = None
        for mod in mods:
            if mod == 'mod':
                int_check(mods[mod])
                pos_check(mods[mod])
                _mod = mods[mod]
                break
            elif mod == 'dfvar':
                self._dfvar = mods[mod]
            else:
                raise KeywordError("Keyword '%s' is not defined." % mod)

        return _mod

    @staticmethod
    def _read_kwargs(**kwargs):
        _dfvar = 'x'
        for kw in kwargs:
            if kw == 'dfvar':
                _dfvar = kwargs[kw]

        return _dfvar

    def _read_vars(self, *vars):
        _var = {}
        for var in vars:
            if isinstance(var, numbers.Number):
                if len(self._var) == 0:
                    _var[self._dfvar] = var
                else:
                    _var[self._var[0]] = var
            else:
                if isinstance(var, dict):
                    _var = var
                    return var
                tuple_check(var)
                if len(var) != 2:
                    raise DefinitionError('Tuple of variable name and corresponding value in need.')
                str_check(var[0])
                number_check(var[1])
                if var[0] in _var:
                    raise DefinitionError('Only one set of variable name and corresponding value taken.')
                elif var[0] not in self._var:
                    raise KeywordError("Variable '%s' is not found." % var[0])
                else:
                    _var[var[0]] = var[1]

        if _var == {}:
            return None
        else:
            if len(_var) != len(self._var):
                for var in _var:
                    self._var.remove(var)

                var = ("', '").join(self._var)
                raise KeywordError("Variable '%s' should be assigned." % var)
            return _var

    def __new__(cls, other=None, *items, **kwargs):
        self = super(ABCPolynomial, cls).__new__(cls)
        self._dfvar = self._read_kwargs(**kwargs)
        if other is None:
            self._var = []
            self._vec = {}
            return self
        else:
            if isinstance(other, ABCPolynomial):
                self = copy.deepcopy(other)
                return self
            if isinstance(other, numbers.Number):
                self._var = [self._dfvar]
                self._vec = {self._dfvar: {0: other}}
                return self
            if isinstance(other, jsstring):
                other = other.replace('-', ' + - ').strip(' ')
                items = other.split('+')
                var = []
                vec = {}
                for item in items:
                    if item == '':
                        continue
                    _var, _exp, _coe = self._read_item(item)
                    if _var is None:
                        if var == []:
                            _var = self._dfvar
                        else:
                            _var = var[0]
                    var = jsappend(var, _var)
                    ec = {_exp: _coe}
                    if _var in vec:
                        vec[_var] = jsupdate(vec[_var], ec)
                    else:
                        vec[_var] = ec

            else:
                if isinstance(other, dict):
                    var, vec = self._read_dict(other)
                else:
                    var, vec = self._read_poly(other)
                    for _vec in items:
                        _var, _vec = self._read_poly(_vec)
                        var = jsappend(var, _var)
                        vec = jsupdate(vec, _vec)

                for key in jskeys(vec):
                    if self._none_check(vec[key]):
                        var.remove(key)
                        del vec[key]

            self._var = sorted(var)
            self._vec = vec
            return self

    def __call__(self, *vars, **mods):
        _mod = self._read_mods(**mods)
        _var = self._read_vars(*vars)
        if _var is None:
            return 0
        else:
            if _mod is None:
                return self.eval(_var)
            else:
                return self.mod(_var, mod=_mod)

            return

    def __repr__(self):
        _ret = '%s(%s)'
        name = self.__class__.__name__
        _var = (', ').join(self._var)
        return _ret % (name, _var)

    def __str__(self):

        def str_ec(_ec, _var):
            if _ec == {} or _ec == {0: 0}:
                return ''
            _str = ''
            _exp = sorted(_ec, reverse=True)
            for exp in _exp:
                _coe = _ec[exp]
                if _coe == 0:
                    continue
                if isinstance(_coe, complex):
                    _str += ' + '
                else:
                    _str += ' - ' if _coe < 0 else ' + '
                    _coe = abs(_coe)
                if exp == 0:
                    _str += str(_coe)
                else:
                    _str += '' if _coe == 1 else str(_coe)
                    _str += _var
                    _str += '' if exp == 1 else '^' + str(exp)

            if _str[1] == '-':
                _str = '-' + _str[3:]
            if _str[1] == '+':
                _str = _str[3:]
            return _str

        if self._var == []:
            _str = ''
        else:
            _str = []
            for _var in self._var:
                _str.append(str_ec(self._vec[_var], _var))

            _str = (' + ').join(_str)
            _str = _str.replace(' + -', ' - ')
        if _str != '':
            return _str
        return '0'

    @abstractmethod
    def _add(a, b):
        pass

    @abstractmethod
    def radd(a, b):
        pass

    @abstractmethod
    def _sub(a, b):
        pass

    @abstractmethod
    def rsub(a, b):
        pass

    @abstractmethod
    def _mul(a, b):
        pass

    @abstractmethod
    def rmul(a, b):
        pass

    @abstractmethod
    def _div(a, b):
        pass

    @abstractmethod
    def rdiv(a, b):
        pass

    @abstractmethod
    def _divmod(a, b):
        pass

    @abstractmethod
    def rdivmod(a, b):
        pass

    @abstractmethod
    def _floordiv(a, b):
        pass

    @abstractmethod
    def rfloordiv(a, b):
        pass

    @abstractmethod
    def _mod(a, b):
        pass

    @abstractmethod
    def rmod(a, b):
        pass

    @abstractmethod
    def _pow(a, exp, mod=None):
        pass

    @abstractmethod
    def _neg(a):
        pass

    @abstractmethod
    def _pos(a):
        pass

    @abstractmethod
    def _abs(a):
        pass

    @abstractmethod
    def _int(self):
        pass

    @abstractmethod
    def _der(self):
        pass