# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\py_mysql\lib\mysql\connector\catch23.py
# Compiled at: 2017-12-07 02:34:36
# Size of source mod 2**32: 3574 bytes
"""Python v2 to v3 migration module"""
from decimal import Decimal
import struct, sys
from .custom_types import HexLiteral
PY2 = sys.version_info[0] == 2
if PY2:
    NUMERIC_TYPES = (
     int, float, Decimal, HexLiteral, long)
    INT_TYPES = (int, long)
    UNICODE_TYPES = (unicode,)
    STRING_TYPES = (str, unicode)
    BYTE_TYPES = (bytearray,)
else:
    NUMERIC_TYPES = (
     int, float, Decimal, HexLiteral)
    INT_TYPES = (int,)
    UNICODE_TYPES = (str,)
    STRING_TYPES = (str,)
    BYTE_TYPES = (bytearray, bytes)

def init_bytearray(payload=b'', encoding='utf-8'):
    """Initializes a bytearray from the payload"""
    if isinstance(payload, bytearray):
        return payload
    else:
        if PY2:
            return bytearray(payload)
        else:
            if isinstance(payload, int):
                return bytearray(payload)
            if not isinstance(payload, bytes):
                try:
                    return bytearray(payload.encode(encoding=encoding))
                except AttributeError:
                    raise ValueError('payload must be a str or bytes')

        return bytearray(payload)


def isstr(obj):
    """Returns whether a variable is a string"""
    if PY2:
        return isinstance(obj, basestring)
    else:
        return isinstance(obj, str)


def isunicode(obj):
    """Returns whether a variable is a of unicode type"""
    if PY2:
        return isinstance(obj, unicode)
    else:
        return isinstance(obj, str)


if PY2:

    def struct_unpack(fmt, buf):
        """Wrapper around struct.unpack handling buffer as bytes and strings"""
        if isinstance(buf, (bytearray, bytes)):
            return struct.unpack_from(fmt, buffer(buf))
        else:
            return struct.unpack_from(fmt, buf)


else:
    struct_unpack = struct.unpack

def make_abc(base_class):
    """Decorator used to create a abstract base class

    We use this decorator to create abstract base classes instead of
    using the abc-module. The decorator makes it possible to do the
    same in both Python v2 and v3 code.
    """

    def wrapper(class_):
        attrs = class_.__dict__.copy()
        for attr in ('__dict__', '__weakref__'):
            attrs.pop(attr, None)

        bases = class_.__bases__
        if PY2:
            attrs['__metaclass__'] = class_
        else:
            bases = (
             class_,) + bases
        return base_class(class_.__name__, bases, attrs)

    return wrapper