# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\stuc400\PycharmProjects\smart_preprocess\dmreader\utils_readfile.py
# Compiled at: 2018-07-26 09:42:28
# Size of source mod 2**32: 6217 bytes
import struct, logging
from dmreader.exceptions import ByteOrderError
_logger = logging.getLogger(__name__)
B_short = struct.Struct('>h')
L_short = struct.Struct('<h')
B_ushort = struct.Struct('>H')
L_ushort = struct.Struct('<H')
B_long = struct.Struct('>l')
L_long = struct.Struct('<l')
B_ulong = struct.Struct('>L')
L_ulong = struct.Struct('<L')
B_float = struct.Struct('>f')
L_float = struct.Struct('<f')
B_double = struct.Struct('>d')
L_double = struct.Struct('<d')
B_bool = struct.Struct('>B')
L_bool = struct.Struct('<B')
B_byte = struct.Struct('>b')
L_byte = struct.Struct('<b')
B_char = struct.Struct('>c')
L_char = struct.Struct('<c')

def read_short(f, endian):
    """Read a 2-Byte integer from file f
    with a given endianness (byte order).
    endian can be either 'big' or 'little'.
    """
    if endian != 'little':
        if endian != 'big':
            _logger.debug('File address:', f.tell())
            raise ByteOrderError(endian)
    else:
        data = f.read(2)
        if endian == 'big':
            s = B_short
        else:
            if endian == 'little':
                s = L_short
        return s.unpack(data)[0]


def read_ushort(f, endian):
    """Read a 2-Byte integer from file f
    with a given endianness (byte order).
    endian can be either 'big' or 'little'.
    """
    if endian != 'little':
        if endian != 'big':
            _logger.debug('File address:', f.tell())
            raise ByteOrderError(endian)
    else:
        data = f.read(2)
        if endian == 'big':
            s = B_ushort
        else:
            if endian == 'little':
                s = L_ushort
        return s.unpack(data)[0]


def read_long(f, endian):
    """Read a 4-Byte integer from file f
    with a given endianness (byte order).
    endian can be either 'big' or 'little'.
    """
    if endian != 'little':
        if endian != 'big':
            _logger.debug('File address:', f.tell())
            raise ByteOrderError(endian)
    else:
        data = f.read(4)
        if endian == 'big':
            s = B_long
        else:
            if endian == 'little':
                s = L_long
        return s.unpack(data)[0]


def read_ulong(f, endian):
    """Read a 4-Byte integer from file f
    with a given endianness (byte order).
    endian can be either 'big' or 'little'.
    """
    if endian != 'little':
        if endian != 'big':
            _logger.debug('File address:', f.tell())
            raise ByteOrderError(endian)
    else:
        data = f.read(4)
        if endian == 'big':
            s = B_ulong
        else:
            if endian == 'little':
                s = L_ulong
        return s.unpack(data)[0]


def read_float(f, endian):
    """Read a 4-Byte floating point from file f
    with a given endianness (byte order).
    endian can be either 'big' or 'little'.
    """
    if endian != 'little':
        if endian != 'big':
            _logger.debug('File address:', f.tell())
            raise ByteOrderError(endian)
    else:
        data = f.read(4)
        if endian == 'big':
            s = B_float
        else:
            if endian == 'little':
                s = L_float
        return s.unpack(data)[0]


def read_double(f, endian):
    """Read a 8-Byte floating point from file f
    with a given endianness (byte order).
    endian can be either 'big' or 'little'.
    """
    if endian != 'little':
        if endian != 'big':
            _logger.debug('File address:', f.tell())
            raise ByteOrderError(endian)
    else:
        data = f.read(8)
        if endian == 'big':
            s = B_double
        else:
            if endian == 'little':
                s = L_double
        return s.unpack(data)[0]


def read_boolean(f, endian):
    """Read a 1-Byte charater from file f
    with a given endianness (byte order).
    endian can be either 'big' or 'little'.
    """
    if endian != 'little':
        if endian != 'big':
            _logger.debug('File address:', f.tell())
            raise ByteOrderError(endian)
    else:
        data = f.read(1)
        if endian == 'big':
            s = B_bool
        else:
            if endian == 'little':
                s = L_bool
        return s.unpack(data)[0]


def read_byte(f, endian):
    """Read a 1-Byte charater from file f
    with a given endianness (byte order).
    endian can be either 'big' or 'little'.
    """
    if endian != 'little':
        if endian != 'big':
            _logger.debug('File address:', f.tell())
            raise ByteOrderError(endian)
    else:
        data = f.read(1)
        if endian == 'big':
            s = B_byte
        else:
            if endian == 'little':
                s = L_byte
        return s.unpack(data)[0]


def read_char(f, endian):
    """Read a 1-Byte charater from file f
    with a given endianness (byte order).
    endian can be either 'big' or 'little'.
    """
    if endian != 'little':
        if endian != 'big':
            _logger.debug('File address:', f.tell())
            raise ByteOrderError(endian)
    else:
        data = f.read(1)
        if endian == 'big':
            s = B_char
        else:
            if endian == 'little':
                s = L_char
        return s.unpack(data)[0]