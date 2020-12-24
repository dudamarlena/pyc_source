# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\py_mysql\lib\mysql\connector\utils.py
# Compiled at: 2017-12-07 02:34:36
# Size of source mod 2**32: 9161 bytes
"""Utilities
"""
from __future__ import print_function
__MYSQL_DEBUG__ = False
import struct
from .catch23 import struct_unpack

def intread(buf):
    """Unpacks the given buffer to an integer"""
    try:
        if isinstance(buf, int):
            return buf
        else:
            length = len(buf)
            if length == 1:
                return buf[0]
            if length <= 4:
                tmp = buf + b'\x00' * (4 - length)
                return struct_unpack('<I', tmp)[0]
            tmp = buf + b'\x00' * (8 - length)
            return struct_unpack('<Q', tmp)[0]
    except:
        raise


def int1store(i):
    """
    Takes an unsigned byte (1 byte) and packs it as a bytes-object.

    Returns string.
    """
    if i < 0 or i > 255:
        raise ValueError('int1store requires 0 <= i <= 255')
    else:
        return bytearray(struct.pack('<B', i))


def int2store(i):
    """
    Takes an unsigned short (2 bytes) and packs it as a bytes-object.

    Returns string.
    """
    if i < 0 or i > 65535:
        raise ValueError('int2store requires 0 <= i <= 65535')
    else:
        return bytearray(struct.pack('<H', i))


def int3store(i):
    """
    Takes an unsigned integer (3 bytes) and packs it as a bytes-object.

    Returns string.
    """
    if i < 0 or i > 16777215:
        raise ValueError('int3store requires 0 <= i <= 16777215')
    else:
        return bytearray(struct.pack('<I', i)[0:3])


def int4store(i):
    """
    Takes an unsigned integer (4 bytes) and packs it as a bytes-object.

    Returns string.
    """
    if i < 0 or i > 4294967295:
        raise ValueError('int4store requires 0 <= i <= 4294967295')
    else:
        return bytearray(struct.pack('<I', i))


def int8store(i):
    """
    Takes an unsigned integer (8 bytes) and packs it as string.

    Returns string.
    """
    if i < 0 or i > 18446744073709551616:
        raise ValueError('int8store requires 0 <= i <= 2^64')
    else:
        return bytearray(struct.pack('<Q', i))


def intstore(i):
    """
    Takes an unsigned integers and packs it as a bytes-object.

    This function uses int1store, int2store, int3store,
    int4store or int8store depending on the integer value.

    returns string.
    """
    if i < 0 or i > 18446744073709551616:
        raise ValueError('intstore requires 0 <= i <=  2^64')
    else:
        if i <= 255:
            formed_string = int1store
        else:
            if i <= 65535:
                formed_string = int2store
            else:
                if i <= 16777215:
                    formed_string = int3store
                else:
                    if i <= 4294967295:
                        formed_string = int4store
                    else:
                        formed_string = int8store
    return formed_string(i)


def lc_int(i):
    """
    Takes an unsigned integer and packs it as bytes,
    with the information of how much bytes the encoded int takes.
    """
    if i < 0 or i > 18446744073709551616:
        raise ValueError('Requires 0 <= i <= 2^64')
    if i < 251:
        return bytearray(struct.pack('<B', i))
    if i <= 65535:
        return b'\xfc' + bytearray(struct.pack('<H', i))
    else:
        if i <= 16777215:
            return b'\xfd' + bytearray(struct.pack('<I', i)[0:3])
        return b'\xfe' + bytearray(struct.pack('<Q', i))


def read_bytes(buf, size):
    """
    Reads bytes from a buffer.

    Returns a tuple with buffer less the read bytes, and the bytes.
    """
    res = buf[0:size]
    return (buf[size:], res)


def read_lc_string(buf):
    """
    Takes a buffer and reads a length coded string from the start.

    This is how Length coded strings work

    If the string is 250 bytes long or smaller, then it looks like this:

      <-- 1b  -->
      +----------+-------------------------
      |  length  | a string goes here
      +----------+-------------------------

    If the string is bigger than 250, then it looks like this:

      <- 1b -><- 2/3/8 ->
      +------+-----------+-------------------------
      | type |  length   | a string goes here
      +------+-----------+-------------------------

      if type == ü:
          length is code in next 2 bytes
      elif type == ý:
          length is code in next 3 bytes
      elif type == þ:
          length is code in next 8 bytes

    NULL has a special value. If the buffer starts with û then
    it's a NULL and we return None as value.

    Returns a tuple (trucated buffer, bytes).
    """
    if buf[0] == 251:
        return (
         buf[1:], None)
    else:
        length = lsize = 0
        fst = buf[0]
        if fst <= 250:
            length = fst
            return (buf[1 + length:], buf[1:length + 1])
        if fst == 252:
            lsize = 2
        else:
            if fst == 253:
                lsize = 3
        if fst == 254:
            lsize = 8
        length = intread(buf[1:lsize + 1])
        return (buf[lsize + length + 1:], buf[lsize + 1:length + lsize + 1])


def read_lc_string_list(buf):
    """Reads all length encoded strings from the given buffer

    Returns a list of bytes
    """
    byteslst = []
    sizes = {252:2, 
     253:3,  254:8}
    buf_len = len(buf)
    pos = 0
    while pos < buf_len:
        first = buf[pos]
        if first == 255:
            return
        if first == 251:
            byteslst.append(None)
            pos += 1
        elif first <= 250:
            length = first
            byteslst.append(buf[pos + 1:length + (pos + 1)])
            pos += 1 + length
        else:
            lsize = 0
            try:
                lsize = sizes[first]
            except KeyError:
                return
            else:
                length = intread(buf[pos + 1:lsize + (pos + 1)])
                byteslst.append(buf[pos + 1 + lsize:length + lsize + (pos + 1)])
            pos += 1 + lsize + length

    return tuple(byteslst)


def read_string(buf, end=None, size=None):
    """
    Reads a string up until a character or for a given size.

    Returns a tuple (trucated buffer, string).
    """
    if end is None:
        if size is None:
            raise ValueError('read_string() needs either end or size')
    else:
        if end is not None:
            try:
                idx = buf.index(end)
            except ValueError:
                raise ValueError('end byte not present in buffer')

            return (
             buf[idx + 1:], buf[0:idx])
        if size is not None:
            return read_bytes(buf, size)
    raise ValueError('read_string() needs either end or size (weird)')


def read_int(buf, size):
    """Read an integer from buffer

    Returns a tuple (truncated buffer, int)
    """
    try:
        res = intread(buf[0:size])
    except:
        raise

    return (
     buf[size:], res)


def read_lc_int(buf):
    """
    Takes a buffer and reads an length code string from the start.

    Returns a tuple with buffer less the integer and the integer read.
    """
    if not buf:
        raise ValueError('Empty buffer.')
    else:
        lcbyte = buf[0]
        if lcbyte == 251:
            return (
             buf[1:], None)
        if lcbyte < 251:
            return (
             buf[1:], int(lcbyte))
        if lcbyte == 252:
            return (
             buf[3:], struct_unpack('<xH', buf[0:3])[0])
        if lcbyte == 253:
            return (
             buf[4:], struct_unpack('<I', buf[1:4] + b'\x00')[0])
        if lcbyte == 254:
            return (
             buf[9:], struct_unpack('<xQ', buf[0:9])[0])
    raise ValueError('Failed reading length encoded integer')


def _digest_buffer(buf):
    """Debug function for showing buffers"""
    if not isinstance(buf, str):
        return ''.join(['\\x%02x' % c for c in buf])
    else:
        return ''.join(['\\x%02x' % ord(c) for c in buf])


def print_buffer(abuffer, prefix=None, limit=30):
    """Debug function printing output of _digest_buffer()"""
    if prefix:
        if limit:
            if limit > 0:
                digest = _digest_buffer(abuffer[0:limit])
        else:
            digest = _digest_buffer(abuffer)
        print(prefix + ': ' + digest)
    else:
        print(_digest_buffer(abuffer))