# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/okhin/git/orage.io/pygcrypt/env/lib/python3.6/site-packages/pygcrypt/test/test_hash.py
# Compiled at: 2016-10-30 11:29:20
# Size of source mod 2**32: 1754 bytes
import pytest
from pygcrypt import hashcontext

def test_init(context):
    h = hashcontext.HashContext(algo='sha256')
    if not h.secure == True:
        raise AssertionError
    else:
        if not h.hmac == False:
            raise AssertionError
        else:
            h = hashcontext.HashContext(algo='sha256', secure=False, hmac=True)
            assert h.secure == False
        assert h.hmac == True


def test_valid(context):
    with pytest.raises(Exception):
        h = hashcontext.HashContext(algo='yadayada')


def test_getattr(context):
    h = hashcontext.HashContext(algo='sha256')
    if not h.algo == 'sha256'.upper():
        raise AssertionError
    elif not h.hashlen == 32:
        raise AssertionError


def test_enable(context):
    h = hashcontext.HashContext(algo='sha256')
    h.enable('sha512')
    with pytest.raises(Exception):
        h.enable('yadayada')


def test_setkey(context):
    h = hashcontext.HashContext(algo='sha256', hmac=True)
    assert h.hmac == True
    h.setkey('What a beautiful key')


def test_write(context):
    h = hashcontext.HashContext(algo='sha256')
    h.write("Let's write things to be hashed")


def test_read(context):
    h = hashcontext.HashContext(algo='sha256')
    h.write("Let's write things that will be hashed and with a long, ong text, bger than 32bytes. Stuff ike that. You know, long block of data.")
    hashed_data = h.read()
    if not hashed_data == b'\xb2m\x9a\x97\xe0\xa7\x1c\xe9\x0f<\x93\xee\rK3\x0b\x813|; q\x99\xf6\xef)\xe1\x9c\x93\xceG\xd8':
        raise AssertionError
    elif not len(hashed_data) == 32:
        raise AssertionError


def test_reset(context):
    h = hashcontext.HashContext(algo='sha256')
    h.write('tototatatiti')
    one = h.read()
    h.reset()
    h.write('tototatatiti')
    assert one == h.read()


def test_copy(context):
    h = hashcontext.HashContext(algo='sha256')
    h.write('yadayada')
    h2 = h.copy()
    assert h.read() == h2.read()