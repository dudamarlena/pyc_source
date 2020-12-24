# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/Dani/Documents/Projects/Golismero_2.0/src_github/thirdparty_libs/netaddr/strategy/eui64.py
# Compiled at: 2013-08-26 10:52:44
"""
IEEE 64-bit EUI (Extended Unique Indentifier) logic.
"""
import struct as _struct, re as _re
AF_EUI64 = 64
from netaddr.core import AddrFormatError
from netaddr.strategy import BYTES_TO_BITS as _BYTES_TO_BITS, valid_words as _valid_words, int_to_words as _int_to_words, words_to_int as _words_to_int, valid_bits as _valid_bits, bits_to_int as _bits_to_int, int_to_bits as _int_to_bits, valid_bin as _valid_bin, int_to_bin as _int_to_bin, bin_to_int as _bin_to_int
width = 64
word_size = 8
word_fmt = '%.2X'
word_sep = '-'
family = AF_EUI64
family_name = 'EUI-64'
version = 64
word_base = 16
max_int = 2 ** width - 1
num_words = width // word_size
max_word = 2 ** word_size - 1
RE_EUI64_FORMAT = _re.compile('^' + ('-').join(['([0-9A-F]{1,2})'] * 8) + '$', _re.IGNORECASE)

def valid_str(addr):
    """
    :param addr: An IEEE EUI-64 indentifier in string form.

    :return: ``True`` if EUI-64 indentifier is valid, ``False`` otherwise.
    """
    try:
        match_result = RE_EUI64_FORMAT.findall(addr)
        if len(match_result) != 0:
            return True
    except TypeError:
        pass

    return False


def str_to_int(addr):
    """
    :param addr: An IEEE EUI-64 indentifier in string form.

    :return: An unsigned integer that is equivalent to value represented
        by EUI-64 string identifier.
    """
    words = []
    try:
        match_result = RE_EUI64_FORMAT.findall(addr)
        if not match_result:
            raise TypeError
    except TypeError:
        raise AddrFormatError('invalid IEEE EUI-64 identifier: %r!' % addr)

    words = match_result[0]
    if len(words) != num_words:
        raise AddrFormatError('bad word count for EUI-64 identifier: %r!' % addr)
    return int(('').join([ '%.2x' % int(w, 16) for w in words ]), 16)


def int_to_str(int_val, dialect=None):
    """
    :param int_val: An unsigned integer.

    :param dialect: (optional) a Python class defining formatting options
        (Please Note - not currently in use).

    :return: An IEEE EUI-64 identifier that is equivalent to unsigned integer.
    """
    words = int_to_words(int_val)
    tokens = [ word_fmt % i for i in words ]
    addr = word_sep.join(tokens)
    return addr


def int_to_packed(int_val):
    """
    :param int_val: the integer to be packed.

    :return: a packed string that is equivalent to value represented by an
    unsigned integer.
    """
    words = int_to_words(int_val)
    return _struct.pack('>8B', *words)


def packed_to_int(packed_int):
    """
    :param packed_int: a packed string containing an unsigned integer.
        It is assumed that string is packed in network byte order.

    :return: An unsigned integer equivalent to value of network address
        represented by packed binary string.
    """
    words = list(_struct.unpack('>8B', packed_int))
    int_val = 0
    for i, num in enumerate(reversed(words)):
        word = num
        word = word << 8 * i
        int_val = int_val | word

    return int_val


def valid_words(words, dialect=None):
    return _valid_words(words, word_size, num_words)


def int_to_words(int_val, dialect=None):
    return _int_to_words(int_val, word_size, num_words)


def words_to_int(words, dialect=None):
    return _words_to_int(words, word_size, num_words)


def valid_bits(bits, dialect=None):
    return _valid_bits(bits, width, word_sep)


def bits_to_int(bits, dialect=None):
    return _bits_to_int(bits, width, word_sep)


def int_to_bits(int_val, dialect=None):
    return _int_to_bits(int_val, word_size, num_words, word_sep)


def valid_bin(bin_val):
    return _valid_bin(bin_val, width)


def int_to_bin(int_val):
    return _int_to_bin(int_val, width)


def bin_to_int(bin_val):
    return _bin_to_int(bin_val, width)