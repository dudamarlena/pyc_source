# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/transit/write_handlers.py
# Compiled at: 2017-12-12 16:52:26
import uuid, datetime, struct
from transit import pyversion
from transit.class_hash import ClassDict
from transit.transit_types import Keyword, Symbol, URI, frozendict, TaggedValue, Link, Boolean
from decimal import Decimal
from dateutil import tz
from math import isnan
MAX_INT = 9223372036854775807
MIN_INT = -9223372036854775808

class TaggedMap(object):

    def __init__(self, tag, rep, str):
        self._tag = tag
        self._rep = rep
        self._str = str

    def tag(self):
        return self._tag

    def rep(self):
        return self._rep

    def string_rep(self):
        return self._str


class NoneHandler(object):

    @staticmethod
    def tag(_):
        return '_'

    @staticmethod
    def rep(_):
        return

    @staticmethod
    def string_rep(n):
        return


class IntHandler(object):

    @staticmethod
    def tag(i):
        return 'i'

    @staticmethod
    def rep(i):
        return i

    @staticmethod
    def string_rep(i):
        return str(i)


class BigIntHandler(object):

    @staticmethod
    def tag(_):
        return 'n'

    @staticmethod
    def rep(n):
        return str(n)

    @staticmethod
    def string_rep(n):
        return str(n)


class Python3IntHandler(object):

    @staticmethod
    def tag(n):
        if n < MAX_INT and n > MIN_INT:
            return 'i'
        return 'n'

    @staticmethod
    def rep(n):
        return n

    @staticmethod
    def string_rep(n):
        return str(n)


class BigDecimalHandler(object):

    @staticmethod
    def tag(_):
        return 'f'

    @staticmethod
    def rep(n):
        return str(n)

    @staticmethod
    def string_rep(n):
        return str(n)


class FloatHandler(object):

    @staticmethod
    def tag(f):
        if isnan(f) or f in (float('Inf'), float('-Inf')):
            return 'z'
        return 'd'

    @staticmethod
    def rep(f):
        if isnan(f):
            return 'NaN'
        if f == float('Inf'):
            return 'INF'
        if f == float('-Inf'):
            return '-INF'
        return f

    @staticmethod
    def string_rep(f):
        return str(f)


class StringHandler(object):

    @staticmethod
    def tag(s):
        return 's'

    @staticmethod
    def rep(s):
        return s

    @staticmethod
    def string_rep(s):
        return s


class BooleanHandler(object):

    @staticmethod
    def tag(_):
        return '?'

    @staticmethod
    def rep(b):
        return bool(b)

    @staticmethod
    def string_rep(b):
        if b:
            return 't'
        return 'f'


class ArrayHandler(object):

    @staticmethod
    def tag(a):
        return 'array'

    @staticmethod
    def rep(a):
        return a

    @staticmethod
    def string_rep(a):
        return


class MapHandler(object):

    @staticmethod
    def tag(m):
        return 'map'

    @staticmethod
    def rep(m):
        return m

    @staticmethod
    def string_rep(m):
        return


class KeywordHandler(object):

    @staticmethod
    def tag(k):
        return ':'

    @staticmethod
    def rep(k):
        return str(k)

    @staticmethod
    def string_rep(k):
        return str(k)


class SymbolHandler(object):

    @staticmethod
    def tag(s):
        return '$'

    @staticmethod
    def rep(s):
        return str(s)

    @staticmethod
    def string_rep(s):
        return str(s)


class UuidHandler(object):

    @staticmethod
    def tag(_):
        return 'u'

    @staticmethod
    def rep(u):
        return struct.unpack('>qq', u.bytes)

    @staticmethod
    def string_rep(u):
        return str(u)


class UriHandler(object):

    @staticmethod
    def tag(_):
        return 'r'

    @staticmethod
    def rep(u):
        return u.rep

    @staticmethod
    def string_rep(u):
        return u.rep


class DateTimeHandler(object):
    epoch = datetime.datetime(1970, 1, 1).replace(tzinfo=tz.tzutc())

    @staticmethod
    def tag(_):
        return 'm'

    @staticmethod
    def rep(d):
        td = d - DateTimeHandler.epoch
        return int((td.microseconds + (td.seconds + td.days * 24 * 3600) * 1000000) / 1000.0)

    @staticmethod
    def verbose_handler():
        return VerboseDateTimeHandler

    @staticmethod
    def string_rep(d):
        return str(DateTimeHandler.rep(d))


class VerboseDateTimeHandler(object):

    @staticmethod
    def tag(_):
        return 't'

    @staticmethod
    def rep(d):
        return d.isoformat()

    @staticmethod
    def string_rep(d):
        return d.isoformat()


class SetHandler(object):

    @staticmethod
    def tag(_):
        return 'set'

    @staticmethod
    def rep(s):
        return TaggedMap('array', tuple(s), None)

    @staticmethod
    def string_rep(_):
        return


class TaggedValueHandler(object):

    @staticmethod
    def tag(tv):
        return tv.tag

    @staticmethod
    def rep(tv):
        return tv.rep

    @staticmethod
    def string_rep(_):
        return


class LinkHandler(object):

    @staticmethod
    def tag(_):
        return 'link'

    @staticmethod
    def rep(l):
        return l.as_map

    @staticmethod
    def string_rep(_):
        return


class WriteHandler(ClassDict):
    """This is the master handler for encoding/writing Python data into
    Transit data, based on its type.
    The Handler itself is a dispatch map, that resolves on full type/object
    inheritance.

    These handlers can be overriden during the creation of a Transit Writer.
    """

    def __init__(self):
        super(WriteHandler, self).__init__()
        self[type(None)] = NoneHandler
        self[bool] = BooleanHandler
        self[Boolean] = BooleanHandler
        self[str] = StringHandler
        self[pyversion.unicode_type] = StringHandler
        self[list] = ArrayHandler
        self[tuple] = ArrayHandler
        self[dict] = MapHandler
        if pyversion.PY3:
            self[int] = Python3IntHandler
        else:
            self[int] = IntHandler
            self[long] = BigIntHandler
        self[float] = FloatHandler
        self[Keyword] = KeywordHandler
        self[Symbol] = SymbolHandler
        self[uuid.UUID] = UuidHandler
        self[URI] = UriHandler
        self[datetime.datetime] = DateTimeHandler
        self[set] = SetHandler
        self[frozenset] = SetHandler
        self[TaggedMap] = TaggedMap
        self[dict] = MapHandler
        self[frozendict] = MapHandler
        self[TaggedValue] = TaggedValueHandler
        self[Link] = LinkHandler
        self[Decimal] = BigDecimalHandler
        return