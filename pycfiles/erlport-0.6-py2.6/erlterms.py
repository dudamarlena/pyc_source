# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/erlport/erlterms.py
# Compiled at: 2010-04-26 08:54:13
"""Erlang external term format.

See Erlang External Term Format for details:
    http://www.erlang.org/doc/apps/erts/erl_ext_dist.html
"""
__author__ = 'Dmitry Vasiliev <dima@hlabs.spb.ru>'
from struct import pack, unpack
from array import array
from zlib import decompressobj, compress
from datetime import datetime

class IncompleteData(ValueError):
    """Need more data."""
    pass


class Atom(str):
    """Erlang atom."""

    def __new__(cls, s):
        if len(s) > 255:
            raise ValueError('invalid atom length')
        return super(Atom, cls).__new__(cls, s)

    def __repr__(self):
        return 'atom(%s)' % self


class String(unicode):
    """Erlang list/string wrapper."""

    def __new__(cls, s):
        if isinstance(s, list):
            s = ('').join(unichr(i) for i in s)
        elif not isinstance(s, unicode):
            raise TypeError('list or unicode object expected')
        return super(String, cls).__new__(cls, s)

    def __repr__(self):
        return 'string(%s)' % super(String, self).__repr__()


class BitBinary(str):
    """Erlang bitstring whose length in bits is not a multiple of 8."""

    def __new__(cls, s, bits):
        obj = super(BitBinary, cls).__new__(cls, s)
        obj.bits = bits
        return obj

    def __repr__(self):
        return 'bits(%s, %s)' % (self.bits, super(BitBinary, self).__repr__())


def decode(string):
    """Decode Erlang external term."""
    if len(string) < 1:
        raise IncompleteData('incomplete data: %r' % string)
    version = ord(string[0])
    if version != 131:
        raise ValueError('unknown protocol version: %i' % version)
    if string[1:2] == 'P':
        if len(string) < 6:
            raise IncompleteData('incomplete data: %r' % string)
        d = decompressobj()
        zlib_data = string[6:]
        term_string = d.decompress(zlib_data) + d.flush()
        uncompressed_size = unpack('>I', string[2:6])[0]
        if len(term_string) != uncompressed_size:
            raise ValueError('invalid compressed tag, %d bytes but got %d' % (
             uncompressed_size, len(term_string)))
        return (
         decode_term(term_string)[0], d.unused_data)
    return decode_term(string[1:])


def decode_term(string, len=len, ord=ord, unpack=unpack, tuple=tuple, float=float, BitBinary=BitBinary, Atom=Atom):
    if len(string) < 1:
        raise IncompleteData('incomplete data: %r' % string)
    tag = ord(string[0])
    tail = string[1:]
    if tag == 97:
        if not tail:
            raise IncompleteData('incomplete data: %r' % string)
        return (ord(tail[:1]), tail[1:])
    else:
        if tag == 98:
            if len(tail) < 4:
                raise IncompleteData('incomplete data: %r' % string)
            (i,) = unpack('>i', tail[:4])
            return (
             i, tail[4:])
        if tag == 106:
            return ([], tail)
        if tag == 107:
            if len(tail) < 2:
                raise IncompleteData('incomplete data: %r' % string)
            (length,) = unpack('>H', tail[:2])
            tail = tail[2:]
            if len(tail) < length:
                raise IncompleteData('incomplete data: %r' % string)
            return ([ ord(i) for i in tail[:length] ], tail[length:])
        if tag == 108:
            if len(tail) < 4:
                raise IncompleteData('incomplete data: %r' % string)
            (length,) = unpack('>I', tail[:4])
            tail = tail[4:]
            lst = []
            while length > 0:
                (term, tail) = decode_term(tail)
                lst.append(term)
                length -= 1

            (ignored, tail) = decode_term(tail)
            return (
             lst, tail)
        if tag == 109:
            if len(tail) < 4:
                raise IncompleteData('incomplete data: %r' % string)
            (length,) = unpack('>I', tail[:4])
            tail = tail[4:]
            if len(tail) < length:
                raise IncompleteData('incomplete data: %r' % string)
            return (tail[:length], tail[length:])
        if tag == 100:
            if len(tail) < 2:
                raise IncompleteData('incomplete data: %r' % string)
            (length,) = unpack('>H', tail[:2])
            tail = tail[2:]
            if len(tail) < length:
                raise IncompleteData('incomplete data: %r' % string)
            name = tail[:length]
            tail = tail[length:]
            if name == 'true':
                return (True, tail)
            if name == 'false':
                return (False, tail)
            if name == 'none':
                return (None, tail)
            return (Atom(name), tail)
        if tag == 104 or tag == 105:
            if tag == 104:
                if not tail:
                    raise IncompleteData('incomplete data: %r' % string)
                arity = ord(tail[0])
                tail = tail[1:]
            else:
                if len(tail) < 4:
                    raise IncompleteData('incomplete data: %r' % string)
                (arity,) = unpack('>I', tail[:4])
                tail = tail[4:]
            lst = []
            while arity > 0:
                (term, tail) = decode_term(tail)
                lst.append(term)
                arity -= 1

            return (tuple(lst), tail)
        if tag == 70:
            (term,) = unpack('>d', tail[:8])
            return (
             term, tail[8:])
        if tag == 99:
            return (
             float(tail[:31].split('\x00', 1)[0]), tail[31:])
        if tag == 110 or tag == 111:
            if tag == 110:
                if len(tail) < 2:
                    raise IncompleteData('incomplete data: %r' % string)
                (length, sign) = unpack('>BB', tail[:2])
                tail = tail[2:]
            else:
                if len(tail) < 5:
                    raise IncompleteData('incomplete data: %r' % string)
                (length, sign) = unpack('>IB', tail[:5])
                tail = tail[5:]
            if len(tail) < length:
                raise IncompleteData('incomplete data: %r' % string)
            n = 0
            for i in array('B', tail[length - 1::-1]):
                n = n << 8 | i

            if sign:
                n = -n
            return (n, tail[length:])
        if tag == 77:
            if len(tail) < 5:
                raise IncompleteData('incomplete data: %r' % string)
            (length, bits) = unpack('>IB', tail[:5])
            tail = tail[5:]
            if len(tail) < length:
                raise IncompleteData('incomplete daata: %r' % string)
            return (BitBinary(tail[:length], bits), tail[length:])
        raise ValueError('unsupported data tag: %i' % tag)
        return


def encode(term, compressed=False):
    """Encode Erlang external term."""
    encoded_term = encode_term(term)
    if compressed:
        if compressed is True:
            compressed = 6
        zlib_term = compress(encoded_term, compressed)
        if len(zlib_term) + 5 <= len(encoded_term):
            return b'\x83P' + pack('>I', len(encoded_term)) + zlib_term
    return b'\x83' + encoded_term


def encode_term(term, pack=pack, tuple=tuple, len=len, isinstance=isinstance, list=list, int=int, long=long, array=array, unicode=unicode, Atom=Atom, BitBinary=BitBinary, str=str, float=float, ord=ord, dict=dict, datetime=datetime, True=True, False=False, ValueError=ValueError, OverflowError=OverflowError):
    if isinstance(term, tuple):
        arity = len(term)
        if arity <= 255:
            header = 'h%c' % arity
        elif arity <= 4294967295:
            header = pack('>BI', 105, arity)
        else:
            raise ValueError('invalid tuple arity')
        _encode_term = encode_term
        return header + ('').join(_encode_term(t) for t in term)
    else:
        if isinstance(term, list):
            if not term:
                return 'j'
                length = len(term)
                if length <= 65535:
                    try:
                        for t in term:
                            if not isinstance(t, (int, long)):
                                raise TypeError

                        bytes = array('B', term).tostring()
                    except (TypeError, OverflowError):
                        pass
                    else:
                        if len(bytes) == length:
                            return pack('>BH', 107, length) + bytes
                elif length > 4294967295:
                    raise ValueError('invalid list length')
                header = pack('>BI', 108, length)
                _encode_term = encode_term
                return header + ('').join(_encode_term(t) for t in term) + 'j'
            if isinstance(term, unicode):
                if not term:
                    return 'j'
                length = len(term)
                if length <= 65535:
                    try:
                        bytes = term.encode('latin1')
                    except UnicodeEncodeError:
                        pass
                    else:
                        return pack('>BH', 107, length) + bytes
                return encode_term([ ord(i) for i in term ])
            if isinstance(term, Atom):
                return pack('>BH', 100, len(term)) + term
            if isinstance(term, BitBinary):
                return pack('>BIB', 77, len(term), term.bits) + term
            if isinstance(term, str):
                length = len(term)
                if length > 4294967295:
                    raise ValueError('invalid binary length')
                return pack('>BI', 109, length) + term
            if term is True or term is False:
                term = term and 'true' or 'false'
                return pack('>BH', 100, len(term)) + term
            if isinstance(term, (int, long)) and 0 <= term <= 255:
                return 'a%c' % term
            if -2147483648 <= term <= 2147483647:
                return pack('>Bi', 98, term)
            if term >= 0:
                sign = 0
            else:
                sign = 1
                term = -term
            bytes = array('B')
            while term > 0:
                bytes.append(term & 255)
                term >>= 8

            length = len(bytes)
            if length <= 255:
                return pack('>BBB', 110, length, sign) + bytes.tostring()
            if length <= 4294967295:
                return pack('>BIB', 111, length, sign) + bytes.tostring()
            raise ValueError('invalid integer value')
        else:
            if isinstance(term, float):
                return pack('>Bd', 70, term)
            if isinstance(term, dict):
                return encode_term(sorted(term.iteritems()))
            if term is None:
                return pack('>BH', 100, 4) + 'none'
            if isinstance(term, datetime):
                return encode_term(((term.year, term.month, term.day),
                 (
                  term.hour, term.minute, term.second)))
        raise ValueError('unsupported data type: %s' % type(term))
        return