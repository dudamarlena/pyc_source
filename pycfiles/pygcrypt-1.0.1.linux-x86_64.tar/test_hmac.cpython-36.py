# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/okhin/git/orage.io/pygcrypt/env/lib/python3.6/site-packages/pygcrypt/test/test_hmac.py
# Compiled at: 2016-10-30 11:29:20
# Size of source mod 2**32: 1295 bytes
import pytest
from pygcrypt import hmaccontext

def test_init(context):
    h = hmaccontext.HMACContext(algo='hmac_sha256')
    assert h.secure == True


def test_set(context):
    h = hmaccontext.HMACContext(algo='gmac_serpent')
    h.key = b'This is a key'
    h.iv = 'This is an IV'


def test_get(context):
    h = hmaccontext.HMACContext(algo='hmac_sha256')
    if not h.maclen == 32:
        raise AssertionError
    elif not h.keylen == 64:
        raise AssertionError


def test_write(context):
    h = hmaccontext.HMACContext(algo='hmac_sha256')
    h.key = b'This is a key'
    h.write('Yiah, data \\o/')


def test_read(context):
    h = hmaccontext.HMACContext(algo='hmac_sha256')
    h.key = b'This is a key'
    h.write('Yiah, data \\o/')
    assert h.read() == b'W\xc3\xa9yD\xb70\xfa\xef\x8f\xc6\xd4v\xc9\x8a\xe8|9\xed-\xca\x06\xa2\xb7W\xb1\xa7o %4@'


def test_reset(context):
    h = hmaccontext.HMACContext(algo='hmac_sha256')
    h.key = b'This is a key'
    h.write('yadayada')
    one = h.read()
    h.reset()
    h.write('yadayada')
    assert one == h.read()


def test_verify(context):
    h = hmaccontext.HMACContext(algo='hmac_sha256')
    h.key = b'This is a key'
    h.write('Yiah, data \\o/')
    assert h.verify(b'W\xc3\xa9yD\xb70\xfa\xef\x8f\xc6\xd4v\xc9\x8a\xe8|9\xed-\xca\x06\xa2\xb7W\xb1\xa7o %4@') == True