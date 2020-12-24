# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/transit/read_handlers.py
# Compiled at: 2017-12-12 16:52:26
from transit import pyversion, transit_types
import uuid, ctypes, dateutil.parser, datetime, dateutil.tz
from transit.helpers import pairs
from decimal import Decimal

class DefaultHandler(object):

    @staticmethod
    def from_rep(t, v):
        return transit_types.TaggedValue(t, v)


class NoneHandler(object):

    @staticmethod
    def from_rep(_):
        return


class KeywordHandler(object):

    @staticmethod
    def from_rep(v):
        return transit_types.Keyword(v)


class SymbolHandler(object):

    @staticmethod
    def from_rep(v):
        return transit_types.Symbol(v)


class BigDecimalHandler(object):

    @staticmethod
    def from_rep(v):
        return Decimal(v)


class BooleanHandler(object):

    @staticmethod
    def from_rep(x):
        if x == 't':
            return transit_types.true
        return transit_types.false


class IntHandler(object):

    @staticmethod
    def from_rep(v):
        return int(v)


class FloatHandler(object):

    @staticmethod
    def from_rep(v):
        return float(v)


class UuidHandler(object):

    @staticmethod
    def from_rep(u):
        """Given a string, return a UUID object."""
        if isinstance(u, pyversion.string_types):
            return uuid.UUID(u)
        a = ctypes.c_ulong(u[0])
        b = ctypes.c_ulong(u[1])
        combined = a.value << 64 | b.value
        return uuid.UUID(int=combined)


class UriHandler(object):

    @staticmethod
    def from_rep(u):
        return transit_types.URI(u)


class DateHandler(object):

    @staticmethod
    def from_rep(d):
        if isinstance(d, pyversion.int_types):
            return DateHandler._convert_timestamp(d)
        if 'T' in d:
            return dateutil.parser.parse(d)
        return DateHandler._convert_timestamp(pyversion.long_type(d))

    @staticmethod
    def _convert_timestamp(ms):
        """Given a timestamp in ms, return a DateTime object."""
        return datetime.datetime.fromtimestamp(ms / 1000.0, dateutil.tz.tzutc())


if pyversion.PY3:

    class BigIntegerHandler(object):

        @staticmethod
        def from_rep(d):
            return int(d)


else:

    class BigIntegerHandler(object):

        @staticmethod
        def from_rep(d):
            return long(d)


class LinkHandler(object):

    @staticmethod
    def from_rep(l):
        return transit_types.Link(**l)


class ListHandler(object):

    @staticmethod
    def from_rep(l):
        return l


class SetHandler(object):

    @staticmethod
    def from_rep(s):
        return frozenset(s)


class CmapHandler(object):

    @staticmethod
    def from_rep(cmap):
        return transit_types.frozendict(pairs(cmap))


class IdentityHandler(object):

    @staticmethod
    def from_rep(i):
        return i


class SpecialNumbersHandler(object):

    @staticmethod
    def from_rep(z):
        if z == 'NaN':
            return float('Nan')
        if z == 'INF':
            return float('Inf')
        if z == '-INF':
            return float('-Inf')
        raise ValueError("Don't know how to handle: " + str(z) + ' as "z"')