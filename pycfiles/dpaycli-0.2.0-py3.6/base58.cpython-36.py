# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/dpaycligraphenebase/base58.py
# Compiled at: 2018-10-15 03:27:18
# Size of source mod 2**32: 6093 bytes
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
from builtins import str
from builtins import object
from builtins import chr
from future.utils import python_2_unicode_compatible
from binascii import hexlify, unhexlify
from .py23 import py23_bytes, py23_chr, bytes_types, integer_types, string_types, text_type
import hashlib, string, logging
log = logging.getLogger(__name__)
PREFIX = 'GPH'
known_prefixes = [
 PREFIX,
 'BTS',
 'MUSE',
 'TEST',
 'TST',
 'DWB',
 'STX',
 'GLX',
 'GLS',
 'EOS',
 'VIT',
 'WKA',
 'EUR',
 'WLS']

@python_2_unicode_compatible
class Base58(object):
    __doc__ = 'Base58 base class\n\n    This class serves as an abstraction layer to deal with base58 encoded\n    strings and their corresponding hex and binary representation throughout the\n    library.\n\n    :param data: Data to initialize object, e.g. pubkey data, address data, ...\n    :type data: hex, wif, bip38 encrypted wif, base58 string\n    :param str prefix: Prefix to use for Address/PubKey strings (defaults to ``GPH``)\n    :return: Base58 object initialized with ``data``\n    :rtype: Base58\n    :raises ValueError: if data cannot be decoded\n\n    * ``bytes(Base58)``: Returns the raw data\n    * ``str(Base58)``:   Returns the readable ``Base58CheckEncoded`` data.\n    * ``repr(Base58)``:  Gives the hex representation of the data.\n    *  ``format(Base58,_format)`` Formats the instance according to ``_format``:\n        * ``"btc"``: prefixed with ``0x80``. Yields a valid btc address\n        * ``"wif"``: prefixed with ``0x00``. Yields a valid wif key\n        * ``"bts"``: prefixed with ``BTS``\n        * etc.\n\n    '

    def __init__(self, data, prefix=PREFIX):
        self._prefix = prefix
        if isinstance(data, Base58):
            data = repr(data)
        else:
            if all(c in string.hexdigits for c in data):
                self._hex = data
            else:
                if data[0] == '5' or data[0] == '6':
                    self._hex = base58CheckDecode(data)
                else:
                    if data[0] == 'K' or data[0] == 'L':
                        self._hex = base58CheckDecode(data)[:-2]
                    else:
                        if data[:len(self._prefix)] == self._prefix:
                            self._hex = gphBase58CheckDecode(data[len(self._prefix):])
                        else:
                            raise ValueError('Error loading Base58 object')

    def __format__(self, _format):
        """ Format output according to argument _format (wif,btc,...)

            :param str _format: Format to use
            :return: formatted data according to _format
            :rtype: str

        """
        if _format.upper() == 'WIF':
            return base58CheckEncode(128, self._hex)
        else:
            if _format.upper() == 'ENCWIF':
                return base58encode(self._hex)
            else:
                if _format.upper() == 'BTC':
                    return base58CheckEncode(0, self._hex)
                if _format.upper() in known_prefixes:
                    return _format.upper() + str(self)
            log.warn("Format %s unknown. You've been warned!\n" % _format)
            return _format.upper() + str(self)

    def __repr__(self):
        """ Returns hex value of object

            :return: Hex string of instance's data
            :rtype: hex string
        """
        return self._hex

    def __str__(self):
        """ Return graphene-base58CheckEncoded string of data

            :return: Base58 encoded data
            :rtype: str
        """
        return gphBase58CheckEncode(self._hex)

    def __bytes__(self):
        """ Return raw bytes

            :return: Raw bytes of instance
            :rtype: bytes

        """
        return unhexlify(self._hex)


BASE58_ALPHABET = b'123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'

def base58decode(base58_str):
    base58_text = py23_bytes(base58_str, 'ascii')
    n = 0
    leading_zeroes_count = 0
    for b in base58_text:
        if isinstance(b, integer_types):
            n = n * 58 + BASE58_ALPHABET.find(py23_chr(b))
        else:
            n = n * 58 + BASE58_ALPHABET.find(b)
        if n == 0:
            leading_zeroes_count += 1

    res = bytearray()
    while n >= 256:
        div, mod = divmod(n, 256)
        res.insert(0, mod)
        n = div
    else:
        res.insert(0, n)

    return hexlify(bytearray(1) * leading_zeroes_count + res).decode('ascii')


def base58encode(hexstring):
    byteseq = py23_bytes(unhexlify(py23_bytes(hexstring, 'ascii')))
    n = 0
    leading_zeroes_count = 0
    for c in byteseq:
        n = n * 256 + c
        if n == 0:
            leading_zeroes_count += 1

    res = bytearray()
    while n >= 58:
        div, mod = divmod(n, 58)
        res.insert(0, BASE58_ALPHABET[mod])
        n = div
    else:
        res.insert(0, BASE58_ALPHABET[n])

    return (BASE58_ALPHABET[0:1] * leading_zeroes_count + res).decode('ascii')


def ripemd160(s):
    ripemd160 = hashlib.new('ripemd160')
    ripemd160.update(unhexlify(s))
    return ripemd160.digest()


def doublesha256(s):
    return hashlib.sha256(hashlib.sha256(unhexlify(s)).digest()).digest()


def b58encode(v):
    return base58encode(v)


def b58decode(v):
    return base58decode(v)


def base58CheckEncode(version, payload):
    s = '%.2x' % version + payload
    checksum = doublesha256(s)[:4]
    result = s + hexlify(checksum).decode('ascii')
    return base58encode(result)


def base58CheckDecode(s):
    s = unhexlify(base58decode(s))
    dec = hexlify(s[:-4]).decode('ascii')
    checksum = doublesha256(dec)[:4]
    if not s[-4:] == checksum:
        raise AssertionError()
    return dec[2:]


def gphBase58CheckEncode(s):
    checksum = ripemd160(s)[:4]
    result = s + hexlify(checksum).decode('ascii')
    return base58encode(result)


def gphBase58CheckDecode(s):
    s = unhexlify(base58decode(s))
    dec = hexlify(s[:-4]).decode('ascii')
    checksum = ripemd160(dec)[:4]
    if not s[-4:] == checksum:
        raise AssertionError()
    return dec