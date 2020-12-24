# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/Dani/Documents/Projects/Golismero_2.0/src_github/thirdparty_libs/netaddr/strategy/ipv6.py
# Compiled at: 2013-08-26 10:52:44
"""
IPv6 address logic.
"""
import struct as _struct
OPT_IMPORTS = False
try:
    import socket as _socket
    if not _socket.has_ipv6:
        raise Exception('IPv6 disabled')
    _socket.inet_pton
    _socket.AF_INET6
    from _socket import inet_pton as _inet_pton, inet_ntop as _inet_ntop, AF_INET6
    OPT_IMPORTS = True
except:
    from netaddr.fbsocket import inet_pton as _inet_pton, inet_ntop as _inet_ntop, AF_INET6

from netaddr.core import AddrFormatError
from netaddr.strategy import BYTES_TO_BITS as _BYTES_TO_BITS, valid_words as _valid_words, int_to_words as _int_to_words, words_to_int as _words_to_int, valid_bits as _valid_bits, bits_to_int as _bits_to_int, int_to_bits as _int_to_bits, valid_bin as _valid_bin, int_to_bin as _int_to_bin, bin_to_int as _bin_to_int
width = 128
word_size = 16
word_sep = ':'
family = AF_INET6
family_name = 'IPv6'
version = 6
word_base = 16
max_int = 2 ** width - 1
num_words = width // word_size
max_word = 2 ** word_size - 1
prefix_to_netmask = dict([ (i, max_int ^ 2 ** (width - i) - 1) for i in range(0, width + 1) ])
netmask_to_prefix = dict([ (max_int ^ 2 ** (width - i) - 1, i) for i in range(0, width + 1) ])
prefix_to_hostmask = dict([ (i, 2 ** (width - i) - 1) for i in range(0, width + 1) ])
hostmask_to_prefix = dict([ (2 ** (width - i) - 1, i) for i in range(0, width + 1) ])

class ipv6_compact(object):
    """An IPv6 dialect class - compact form."""
    word_fmt = '%x'
    compact = True


class ipv6_full(ipv6_compact):
    """An IPv6 dialect class - 'all zeroes' form."""
    compact = False


class ipv6_verbose(ipv6_compact):
    """An IPv6 dialect class - extra wide 'all zeroes' form."""
    word_fmt = '%.4x'
    compact = False


def valid_str(addr, flags=0):
    """
    :param addr: An IPv6 address in presentation (string) format.

    :param flags: decides which rules are applied to the interpretation of the
        addr value. Future use - currently has no effect.

    :return: ``True`` if IPv6 address is valid, ``False`` otherwise.
    """
    if addr == '':
        raise AddrFormatError('Empty strings are not supported!')
    try:
        _inet_pton(AF_INET6, addr)
    except:
        return False

    return True


def str_to_int(addr, flags=0):
    """
    :param addr: An IPv6 address in string form.

    :param flags: decides which rules are applied to the interpretation of the
        addr value. Future use - currently has no effect.

    :return: The equivalent unsigned integer for a given IPv6 address.
    """
    try:
        packed_int = _inet_pton(AF_INET6, addr)
        return packed_to_int(packed_int)
    except Exception:
        raise AddrFormatError('%r is not a valid IPv6 address string!' % addr)


def int_to_str(int_val, dialect=None):
    """
    :param int_val: An unsigned integer.

    :param dialect: (optional) a Python class defining formatting options.

    :return: The IPv6 presentation (string) format address equivalent to the
        unsigned integer provided.
    """
    if dialect is None:
        dialect = ipv6_compact
    addr = None
    try:
        packed_int = int_to_packed(int_val)
        if dialect.compact:
            addr = _inet_ntop(AF_INET6, packed_int)
        else:
            words = list(_struct.unpack('>8H', packed_int))
            tokens = [ dialect.word_fmt % word for word in words ]
            addr = word_sep.join(tokens)
    except Exception:
        raise ValueError('%r is not a valid 128-bit unsigned integer!' % int_val)

    return addr


def int_to_arpa(int_val):
    """
    :param int_val: An unsigned integer.

    :return: The reverse DNS lookup for an IPv6 address in network byte
        order integer form.
    """
    addr = int_to_str(int_val, ipv6_verbose)
    tokens = list(addr.replace(':', ''))
    tokens.reverse()
    tokens = tokens + ['ip6', 'arpa', '']
    return ('.').join(tokens)


def int_to_packed(int_val):
    """
    :param int_val: the integer to be packed.

    :return: a packed string that is equivalent to value represented by an
    unsigned integer.
    """
    words = int_to_words(int_val, 4, 32)
    return _struct.pack('>4I', *words)


def packed_to_int(packed_int):
    """
    :param packed_int: a packed string containing an unsigned integer.
        It is assumed that string is packed in network byte order.

    :return: An unsigned integer equivalent to value of network address
        represented by packed binary string.
    """
    words = list(_struct.unpack('>4I', packed_int))
    int_val = 0
    for i, num in enumerate(reversed(words)):
        word = num
        word = word << 32 * i
        int_val = int_val | word

    return int_val


def valid_words(words):
    return _valid_words(words, word_size, num_words)


def int_to_words(int_val, num_words=None, word_size=None):
    if num_words is None:
        num_words = globals()['num_words']
    if word_size is None:
        word_size = globals()['word_size']
    return _int_to_words(int_val, word_size, num_words)


def words_to_int(words):
    return _words_to_int(words, word_size, num_words)


def valid_bits(bits):
    return _valid_bits(bits, width, word_sep)


def bits_to_int(bits):
    return _bits_to_int(bits, width, word_sep)


def int_to_bits(int_val, word_sep=None):
    if word_sep is None:
        word_sep = globals()['word_sep']
    return _int_to_bits(int_val, word_size, num_words, word_sep)


def valid_bin(bin_val):
    return _valid_bin(bin_val, width)


def int_to_bin(int_val):
    return _int_to_bin(int_val, width)


def bin_to_int(bin_val):
    return _bin_to_int(bin_val, width)