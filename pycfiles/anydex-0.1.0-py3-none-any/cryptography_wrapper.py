# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/martijndevos/Documents/anydex-core/anydex/../pyipv8/ipv8/attestation/wallet/bonehexact/cryptosystem/cryptography_wrapper.py
# Compiled at: 2019-06-07 08:10:38
from __future__ import absolute_import
from cryptography.hazmat.backends import default_backend
from .....util import cast_to_bin

def generate_safe_prime(bit_length, backend=default_backend()):
    """
    Generate a 'safe' prime p ((p-1)/2 is also prime).

    :param bit_length: the length of the generated prime in bits
    :type bit_length: int
    :param backend: the cryptography backend to use
    :type backend: Backend
    :return: the generated prime
    :rtype: int
    """
    generated = backend._lib.BN_new()
    err = backend._lib.BN_generate_prime_ex(generated, bit_length, 1, backend._ffi.NULL, backend._ffi.NULL, backend._ffi.NULL)
    if err == 0:
        backend._lib.BN_clear_free(generated)
        raise RuntimeError('Failed to generate prime!')
    generated_hex = backend._lib.BN_bn2hex(generated)
    out = int(backend._ffi.string(generated_hex), 16)
    backend._lib.OPENSSL_free(generated_hex)
    backend._lib.BN_clear_free(generated)
    return out


def is_prime(number, backend=default_backend()):
    """
    Check a number for primality.

    :param number: the number to check for primality
    :type number: int
    :param backend: the cryptography backend to use
    :type backend: Backend
    :return: True is the n is expected to be prime, False otherwise
    :rtype: bool
    """
    hex_n = hex(number)[2:]
    if hex_n.endswith('L'):
        hex_n = hex_n[:-1]
    hex_n = cast_to_bin(hex_n)
    generated = backend._lib.BN_new()
    bn_pp = backend._ffi.new('BIGNUM **', generated)
    err = backend._lib.BN_hex2bn(bn_pp, hex_n)
    if err == 0:
        backend._lib.BN_clear_free(generated)
        raise RuntimeError('Failed to read BIGNUM from hex string!')
    result = backend._lib.BN_is_prime_ex(generated, backend._lib.BN_prime_checks_for_size(int(len(hex_n) * 8)), backend._ffi.NULL, backend._ffi.NULL)
    backend._lib.BN_clear_free(generated)
    if result == 1:
        return True
    return False