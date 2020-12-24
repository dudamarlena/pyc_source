# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/bitpeer/util.py
# Compiled at: 2015-11-17 10:40:39
# Size of source mod 2**32: 937 bytes
base58_digits = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'

def base58_encode(address_bignum):
    """This function converts an address in bignum formatting
    to a string in base58, it doesn't prepend the '1' prefix
    for the Bitcoin address.

    :param address_bignum: The address in numeric format
    :returns: The string in base58
    """
    basedigits = []
    while address_bignum > 0:
        address_bignum, rem = divmod(address_bignum, 58)
        basedigits.insert(0, base58_digits[rem])

    return ''.join(basedigits)


def base58_decode(address):
    """This function converts an base58 string to a numeric
    format.

    :param address: The base58 string
    :returns: The numeric value decoded
    """
    address_bignum = 0
    for char in address:
        address_bignum *= 58
        digit = base58_digits.index(char)
        address_bignum += digit

    return address_bignum