# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/Dani/Documents/Projects/Golismero_2.0/src_github/thirdparty_libs/netaddr/strategy/ipv4.py
# Compiled at: 2013-08-26 10:52:44
"""IPv4 address logic."""
import sys as _sys, struct as _struct, socket as _socket
if _sys.platform in ('win32', 'cygwin'):
    from _socket import inet_aton as _inet_aton, inet_ntoa as _inet_ntoa
    from netaddr.fbsocket import inet_pton as _inet_pton, AF_INET
else:
    try:
        _socket.inet_aton('255.255.255.255')
        from _socket import inet_aton as _inet_aton, inet_ntoa as _inet_ntoa, inet_pton as _inet_pton, AF_INET
    except:
        from netaddr.fbsocket import inet_aton as _inet_aton, inet_ntoa as _inet_ntoa, inet_pton as _inet_pton, AF_INET

from netaddr.core import AddrFormatError, ZEROFILL, INET_PTON
from netaddr.strategy import valid_words as _valid_words, valid_bits as _valid_bits, bits_to_int as _bits_to_int, int_to_bits as _int_to_bits, valid_bin as _valid_bin, int_to_bin as _int_to_bin, bin_to_int as _bin_to_int
from netaddr.compat import _str_type
width = 32
word_size = 8
word_fmt = '%d'
word_sep = '.'
family = AF_INET
family_name = 'IPv4'
version = 4
word_base = 10
max_int = 2 ** width - 1
num_words = width // word_size
max_word = 2 ** word_size - 1
prefix_to_netmask = dict([ (i, max_int ^ 2 ** (width - i) - 1) for i in range(0, width + 1) ])
netmask_to_prefix = dict([ (max_int ^ 2 ** (width - i) - 1, i) for i in range(0, width + 1) ])
prefix_to_hostmask = dict([ (i, 2 ** (width - i) - 1) for i in range(0, width + 1) ])
hostmask_to_prefix = dict([ (2 ** (width - i) - 1, i) for i in range(0, width + 1) ])

def valid_str(addr, flags=0):
    """
    :param addr: An IPv4 address in presentation (string) format.

    :param flags: decides which rules are applied to the interpretation of the
        addr value. Supported constants are INET_PTON and ZEROFILL. See the
        netaddr.core docs for details.

    :return: ``True`` if IPv4 address is valid, ``False`` otherwise.
    """
    if addr == '':
        raise AddrFormatError('Empty strings are not supported!')
    validity = True
    if flags & ZEROFILL:
        addr = ('.').join([ '%d' % int(i) for i in addr.split('.') ])
    try:
        if flags & INET_PTON:
            _inet_pton(AF_INET, addr)
        else:
            _inet_aton(addr)
    except:
        validity = False

    return validity


def str_to_int(addr, flags=0):
    """
    :param addr: An IPv4 dotted decimal address in string form.

    :param flags: decides which rules are applied to the interpretation of the
        addr value. Supported constants are INET_PTON and ZEROFILL. See the
        netaddr.core docs for details.

    :return: The equivalent unsigned integer for a given IPv4 address.
    """
    if flags & ZEROFILL:
        addr = ('.').join([ '%d' % int(i) for i in addr.split('.') ])
    try:
        if flags & INET_PTON:
            return _struct.unpack('>I', _inet_pton(AF_INET, addr))[0]
        else:
            return _struct.unpack('>I', _inet_aton(addr))[0]

    except:
        raise AddrFormatError('%r is not a valid IPv4 address string!' % addr)


def int_to_str(int_val, dialect=None):
    """
    :param int_val: An unsigned integer.

    :param dialect: (unused) Any value passed in is ignored.

    :return: The IPv4 presentation (string) format address equivalent to the
        unsigned integer provided.
    """
    if 0 <= int_val <= max_int:
        return '%d.%d.%d.%d' % (
         int_val >> 24,
         int_val >> 16 & 255,
         int_val >> 8 & 255,
         int_val & 255)
    raise ValueError('%r is not a valid 32-bit unsigned integer!' % int_val)


def int_to_arpa(int_val):
    """
    :param int_val: An unsigned integer.

    :return: The reverse DNS lookup for an IPv4 address in network byte
        order integer form.
    """
    words = [ '%d' % i for i in int_to_words(int_val) ]
    words.reverse()
    words.extend(['in-addr', 'arpa', ''])
    return ('.').join(words)


def int_to_packed(int_val):
    """
    :param int_val: the integer to be packed.

    :return: a packed string that is equivalent to value represented by an
    unsigned integer.
    """
    return _struct.pack('>I', int_val)


def packed_to_int(packed_int):
    """
    :param packed_int: a packed string containing an unsigned integer.
        It is assumed that string is packed in network byte order.

    :return: An unsigned integer equivalent to value of network address
        represented by packed binary string.
    """
    return _struct.unpack('>I', packed_int)[0]


def valid_words(words):
    return _valid_words(words, word_size, num_words)


def int_to_words(int_val):
    """
    :param int_val: An unsigned integer.

    :return: An integer word (octet) sequence that is equivalent to value
        represented by an unsigned integer.
    """
    if not 0 <= int_val <= max_int:
        raise ValueError('%r is not a valid integer value supported by this address type!' % int_val)
    return (
     int_val >> 24,
     int_val >> 16 & 255,
     int_val >> 8 & 255,
     int_val & 255)


def words_to_int(words):
    """
    :param words: A list or tuple containing integer octets.

    :return: An unsigned integer that is equivalent to value represented
        by word (octet) sequence.
    """
    if not valid_words(words):
        raise ValueError('%r is not a valid octet list for an IPv4 address!' % words)
    return _struct.unpack('>I', _struct.pack('4B', *words))[0]


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


def expand_partial_address(addr):
    """
    Expands a partial IPv4 address into a full 4-octet version.

    :param addr: an partial or abbreviated IPv4 address

    :return: an expanded IP address in presentation format (x.x.x.x)

    """
    tokens = []
    error = AddrFormatError('invalid partial IPv4 address: %r!' % addr)
    if isinstance(addr, _str_type):
        if ':' in addr:
            raise error
        if '.' in addr:
            tokens = [ '%d' % int(o) for o in addr.split('.') ]
        else:
            try:
                tokens = [
                 '%d' % int(addr)]
            except ValueError:
                raise error

        if 1 <= len(tokens) <= 4:
            for i in range(4 - len(tokens)):
                tokens.append('0')

        else:
            raise error
    if not tokens:
        raise error
    return '%s.%s.%s.%s' % tuple(tokens)