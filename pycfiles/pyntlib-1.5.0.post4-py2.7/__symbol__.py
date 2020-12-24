# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/ntlib/NTLArchive/__abc__/__symbol__.py
# Compiled at: 2018-04-23 08:51:10
import abc, re
from ..NTLExceptions import DefinitionError, ResidueError
from ..NTLValidations import basestring_check, int_check
__all__ = [
 'ABCSymbol']
SYMBOL_FORMAT = re.compile('\n    \\A\\s*                       # optional whitespace at the start, then\n    (?P<sign>[-+]?)             # an optional sign, then\n    (?=\\d)                      # lookahead for digit\n    (?P<num>\\d*)                # numerator\n    (?:[/|]?)                   # followed by a solidus or vertical line, then\n    (?=\\d)                      # lookahead for digit\n    (?P<den>\\d*)                # denominator\n    \\s*\\Z                       # and optional whitespace to finish\n', re.VERBOSE | re.IGNORECASE)
ABCMeta = abc.ABCMeta
abstractmethod = abc.abstractmethod
abstractproperty = abc.abstractproperty

class ABCSymbol(object):
    __all__ = [
     'numerator', 'denominator', 'nickname']
    __metaclass__ = ABCMeta
    __hash__ = None

    @abstractproperty
    def numerator(self):
        pass

    @abstractproperty
    def denominator(self):
        pass

    @abstractproperty
    def nickname(self):
        pass

    @abstractmethod
    def eval(self):
        pass

    @abstractmethod
    def simplify(self):
        pass

    @abstractmethod
    def reciprocate(self):
        pass

    @abstractmethod
    def convert(self, kind):
        pass

    def has_sametype(self, other):
        return isinstance(other, self.__class__)

    def __new__(cls, numerator, denominator=None, **kwargs):
        self = super(ABCSymbol, cls).__new__(cls)
        if denominator is None:
            if isinstance(numerator, ABCSymbol):
                self = numerator
                return self
            basestring_check(numerator)
            m = SYMBOL_FORMAT.match(numerator)
            if m is None:
                raise DefinitionError('Invalid literal for symbols: %r' % numerator)
            _numerator = int(m.group('num'))
            _denominator = int(m.group('den'))
            if m.group('sign') == '-':
                _numerator = -_numerator
        else:
            int_check(numerator, denominator)
            if denominator < 0:
                _numerator = -numerator
                _denominator = -denominator
            else:
                _numerator = numerator
                _denominator = denominator
        if _denominator == 0:
            raise ResidueError('Symbol(%s, 0)' % _numerator)
        self._numerator = _numerator
        self._denominator = _denominator
        return self

    def __repr__(self):
        _ret = '%s(%d, %d)'
        name = self.__class__.__name__
        _num = self._numerator
        _den = self._denominator
        return _ret % (name, _num, _den)

    def __str__(self):
        return '%d | %d' % (self._numerator, self._denominator)

    def __eq__(self, other):
        _ret = self._numerator == other._numerator and self._denominator == other._denominator
        return _ret

    def __ne__(self, other):
        return not self.__eq__(other)

    def __reduce__(self):
        return (
         self.__class__, (str(self),))

    def __copy__(self):
        if type(self) == ABCSymbol:
            return self
        return self.__class__(self._numerator, self._denominator, self._nickname)

    def __deepcopy__(self, memo):
        if type(self) == ABCSymbol:
            return self
        return self.__class__(self._numerator, self._denominator, self._nickname)