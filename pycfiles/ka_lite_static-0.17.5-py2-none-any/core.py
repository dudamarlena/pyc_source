# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-jkXn_D/rsa/rsa/core.py
# Compiled at: 2018-07-11 18:15:32
"""Core mathematical operations.

This is the actual core RSA implementation, which is only defined
mathematically on integers.
"""
from rsa._compat import is_integer

def assert_int(var, name):
    if is_integer(var):
        return
    raise TypeError('%s should be an integer, not %s' % (name, var.__class__))


def encrypt_int(message, ekey, n):
    """Encrypts a message using encryption key 'ekey', working modulo n"""
    assert_int(message, 'message')
    assert_int(ekey, 'ekey')
    assert_int(n, 'n')
    if message < 0:
        raise ValueError('Only non-negative numbers are supported')
    if message > n:
        raise OverflowError('The message %i is too long for n=%i' % (message, n))
    return pow(message, ekey, n)


def decrypt_int(cyphertext, dkey, n):
    """Decrypts a cypher text using the decryption key 'dkey', working modulo n"""
    assert_int(cyphertext, 'cyphertext')
    assert_int(dkey, 'dkey')
    assert_int(n, 'n')
    message = pow(cyphertext, dkey, n)
    return message