# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/okhin/git/orage.io/pygcrypt/env/lib/python3.6/site-packages/pygcrypt/test/test_ciphers.py
# Compiled at: 2016-01-01 08:00:46
# Size of source mod 2**32: 1204 bytes
import pytest, sys
print(sys.path)
from pygcrypt import ciphers

def test_init():
    """
    Let's test the initialisation of a cipher
    """
    c = ciphers.Cipher(b'AES', 'CBC')
    if not c.algo == b'AES':
        raise AssertionError
    elif not c.mode == 'CBC':
        raise AssertionError


def test_get_info():
    """
    Let's test getting keylen or blocksize from the cipher
    """
    c = ciphers.Cipher(b'AES', 'CBC')
    if not c.keylen == 16:
        raise AssertionError
    elif not c.blocksize == 16:
        raise AssertionError


def test_set_key_iv():
    """
    Let's try to set a key and an iv on a cipher.
    """
    c = ciphers.Cipher(b'AES', 'CBC')
    c.key = '0123456789ABCDEF'
    if not c.key == b'0123456789ABCDEF':
        raise AssertionError
    else:
        c.iv = '0123456789ABCDEF'
        assert c.iv == b'0123456789ABCDEF'


def test_reset_cipher():
    c = ciphers.Cipher(b'AES', 'CBC')
    c.key = '0123456789ABCDEF'
    c.iv = '0123456789ABCDEF'
    c.reset()
    if not c.key == b'0123456789ABCDEF':
        raise AssertionError
    elif not c.iv == None:
        raise AssertionError


def test_encrypt_decrypt():
    c = ciphers.Cipher(b'AES', 'CBC')
    c.key = '0123456789ABCDEF'
    c.iv = '0123456789ABCDEF'
    encrypt = c.encrypt(b'0123456789ABCDEF')
    c.reset()
    c.iv = '0123456789ABCDEF'
    assert c.decrypt(encrypt) == b'0123456789ABCDEF'