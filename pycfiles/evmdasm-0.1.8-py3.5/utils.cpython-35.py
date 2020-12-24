# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\evmdasm\utils.py
# Compiled at: 2018-10-12 15:53:23
# Size of source mod 2**32: 869 bytes
import string, binascii

def str_to_bytes(s):
    """
    Convert 0xHexString to bytes
    :param s: 0x hexstring
    :return:  byte sequence
    """
    try:
        return bytes.fromhex(s.replace('0x', ''))
    except (NameError, AttributeError):
        return s.decode('hex')


def bytes_to_str(s, prefix='0x'):
    return '%s%s' % (prefix, binascii.hexlify(s).decode('utf-8'))


def strip_0x_prefix(s):
    if not s.startswith('0x'):
        return s
    return s[2:]


def is_hexstring(s):
    hex_digits = set(string.hexdigits)
    return all(c in hex_digits for c in s)


def int2bytes(i):
    hex_string = '%x' % i
    n = len(hex_string)
    return binascii.unhexlify(hex_string.zfill(n + (n & 1)))