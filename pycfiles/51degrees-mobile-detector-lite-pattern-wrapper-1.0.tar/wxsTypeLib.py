# uncompyle6 version 3.6.7
# Python bytecode 2.3 (62011)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: \Ft\Xml\ThirdParty\Xvif\wxsTypeLib.py
# Compiled at: 2006-01-20 18:15:53
import re, time, rng, rngCoreTypeLib
from Ft.Lib.Regex import W3cRegexToPyRegex
from Ft.Lib.Uri import MatchesUriRefSyntax, PercentEncode
BASE_URI = 'http://www.w3.org/2001/XMLSchema-datatypes'

class _Lexical(object):
    __module__ = __name__

    def __init__(self):
        self.lexical = self

    if len('𐠀') == 1:

        def lengthFacet(self, value):
            return len(self.lexical) == int(value)

    else:

        def lengthFacet(self, value):
            import Smart_len
            return Smart_len.smart_len(self) == int(value)


class stringType(rngCoreTypeLib.stringType, _Lexical):
    """ """
    __module__ = __name__

    def __init__(self, value):
        rngCoreTypeLib.stringType.__init__(self, value)
        _Lexical.__init__(self)

    def maxLengthFacet(self, value):
        return len(self) <= int(value)

    def minLengthFacet(self, value):
        return len(self) >= int(value)

    def patternFacet(self, value):
        m = re.match(W3cRegexToPyRegex(value), self)
        return m and m.end() == len(self) or False


class normalizedStringType(str):
    __module__ = __name__

    def __new__(cls, value=''):
        return unicode.__new__(cls, re.sub('[\n\t]', ' ', value))


class tokenType(rngCoreTypeLib.tokenType, _Lexical):
    """
    Strictly identical to the token builtin class
    """
    __module__ = __name__

    def __init__(self, value):
        rngCoreTypeLib.tokenType.__init__(self, value)
        _Lexical.__init__(self)


class IDType(rngCoreTypeLib.tokenType, _Lexical):
    """
    Similar to the token builtin class
    """
    __module__ = __name__
    stateful = True

    def __init__(self, value, state=None):
        rngCoreTypeLib.tokenType.__init__(self, value)
        _Lexical.__init__(self)
        if state is not None:
            ids = state.setdefault((BASE_URI, 'ID', {}))
            if value in ids:
                raise ValueError("Validity Error: duplicate ID '%s'" % value)
            ids[value] = None
        return
        return


class IDREFType(rngCoreTypeLib.tokenType, _Lexical):
    """
    Similar to the token builtin class
    """
    __module__ = __name__
    stateful = True

    def __init__(self, value, state=None):
        rngCoreTypeLib.tokenType.__init__(self, value)
        _Lexical.__init__(self)
        if state is not None:
            idrefs = state.setdefault((BASE_URI, 'IDREF', {}))
            idrefs[value] = None
        return
        return

    def finalize(state):
        ids = state.setdefault((BASE_URI, 'ID', {}))
        idrefs = state.setdefault((BASE_URI, 'IDREF', {}))
        for idref in idrefs.keys():
            if idref in ids:
                raise ValueError("Validity Error: IDREF '%s' doesn't match any ID" % value)

        return

    finalize = staticmethod(finalize)


class _Bounded:
    __module__ = __name__

    def __init__(self, value):
        if self.__class__.max != None and self > self.__class__.max:
            raise ValueError
        if self.__class__.min != None and self < self.__class__.min:
            raise ValueError
        return


class _Ordered:
    __module__ = __name__

    def maxExclusiveFacet(self, value):
        return self < self.__class__(value)

    def maxInclusiveFacet(self, value):
        return self <= self.__class__(value)

    def minExclusiveFacet(self, value):
        return self > self.__class__(value)

    def minInclusiveFacet(self, value):
        return self >= self.__class__(value)


class _Numeric(_Ordered):
    __module__ = __name__

    def totalDigitsFacet(self, value):
        if self < 0:
            return len(str(self)) - 1 <= value
        else:
            return len(str(self)) <= value


class integerType(long, _Numeric):
    """
    """
    __module__ = __name__


class nonPositiveIntegerType(_Bounded, integerType):
    __module__ = __name__
    min = None
    max = 0


class nonNegativeIntegerType(_Bounded, integerType):
    __module__ = __name__
    min = 0
    max = None


class positiveIntegerType(_Bounded, integerType):
    __module__ = __name__
    min = 1
    max = None


class negativeIntegerType(_Bounded, integerType):
    __module__ = __name__
    min = None
    max = -1


class unsignedLongType(_Bounded, integerType):
    __module__ = __name__
    min = 0
    max = 18446744073709551615


class unsignedIntType(_Bounded, integerType):
    __module__ = __name__
    min = 0
    max = 4294967295


class longType(_Bounded, integerType):
    __module__ = __name__
    min = -9223372036854775808
    max = 9223372036854775807


class intType(int, _Numeric):
    """
    """
    __module__ = __name__


class shortType(_Bounded, intType):
    __module__ = __name__
    min = -32768
    max = 32767


class unsignedShortType(_Bounded, intType):
    __module__ = __name__
    min = 0
    max = 65535


class byteType(_Bounded, intType):
    __module__ = __name__
    min = -128
    max = 127


class unsignedByteType(_Bounded, intType):
    __module__ = __name__
    min = 0
    max = 255


class decimalType(_Numeric):
    __module__ = __name__

    def __init__(self, value):
        value = tokenType(unicode(value))
        if re.match('^[+-]?([0-9]*\\.[0-9]+|[0-9]+\\.?[0-9]*)$', value):
            try:
                (i, d) = value.split('.')
            except ValueError:
                i = value
                d = ''
            else:
                d = re.sub('0*$', '', d)
                self.val = long('%s%s' % (i, d))
                self.power = len(d)
                self.value = value
        else:
            raise ValueError

    def __cmp__(self, other):
        if other.__class__ != decimalType:
            other = decimalType(other)
        if self.power < other.power:
            o = other.val
            s = self.val * 10 ** (other.power - self.power)
        else:
            s = self.val
            o = other.val * 10 ** (self.power - other.power)
        return s.__cmp__(o)

    def fractionDigitsFacet(self, value):
        return self.power <= value

    def totalDigitsFacet(self, value):
        if self.val < 0:
            return len(str(self.val)) - 1 <= value
        else:
            return len(str(self.val)) <= value


floatType = decimalType

class dateType(_Ordered):
    __module__ = __name__
    formatWoTZ = '%Y-%m-%d'
    formatZ = '%Y-%m-%dZ'

    def __init__(self, value):
        self.lexical = tokenType(value)
        if not re.match('[ \t\n]*[0-9]+-[0-9]{2}-[0-9]{2}Z?', value):
            raise ValueError
        try:
            self.value = time.strptime(value, dateType.formatWoTZ)
            self.tz = 0
        except ValueError:
            self.value = time.strptime(value, dateType.formatZ)
            self.tz = 1

        if self.value[2] == 31 and not self.value[1] in (1, 3, 5, 7, 8, 10, 12):
            raise ValueError
        if self.value[2] == 30 and self.value[1] == 2:
            raise ValueError
        if self.value[2] == 29 and self.value[1] == 2 and (self.value[0] % 4 != 0 or self.value[0] % 100 == 0):
            raise ValueError

    def __cmp__(self, other):
        if other.__class__ != dateType:
            other = dateType(other)
        for i in range(0, 5):
            res = self.value[i].__cmp__(other.value[i])
            if res != 0:
                return res

        return 0


class booleanType(rngCoreTypeLib.stringType, _Lexical):
    """ """
    __module__ = __name__

    def __init__(self, value):
        rngCoreTypeLib.stringType.__init__(self, value)
        _Lexical.__init__(self)
        if value not in ['1', '0', 'true', 'false']:
            raise ValueError


class timeType(_Ordered):
    __module__ = __name__

    def __init__(self, value):
        try:
            import datetime
            from TimeLib import parse_isotime
            self.value = parse_isotime(value)
            if not self.value:
                raise ValueError
        except:
            from Ft.Lib.Time import FromISO8601
            try:
                self.value = FromISO8601(value)
            except:
                raise ValueError


class dateTimeType(_Ordered):
    __module__ = __name__

    def __init__(self, value):
        try:
            import datetime
            from TimeLib import parse_isodate
            self.value = parse_isodate(value)
            if not self.value:
                raise ValueError
        except:
            from Ft.Lib.Time import FromISO8601
            try:
                self.value = FromISO8601(value)
            except:
                raise ValueError


class anyURIType(_Lexical):
    """
    anyURI is somewhat of a misnomer;
    it is really a URI reference *or* IRI reference.
    """
    __module__ = __name__

    def __init__(self, value):
        escaped = PercentEncode(value, encodeReserved=False)
        if not MatchesUriRefSyntax(escaped):
            raise ValueError