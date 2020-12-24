# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-build-ed191__6/jeepney/jeepney/tests/test_auth.py
# Compiled at: 2020-01-10 16:25:36
# Size of source mod 2**32: 542 bytes
from jeepney import auth

def test_make_auth_external():
    b = auth.make_auth_external()
    assert b.startswith(b'AUTH EXTERNAL')


def test_make_auth_anonymous():
    b = auth.make_auth_anonymous()
    assert b.startswith(b'AUTH ANONYMOUS')


def test_parser():
    p = auth.SASLParser()
    p.feed(b'OK 728d62bc2eb394')
    if not not p.authenticated:
        raise AssertionError
    else:
        p.feed(b'1ebbb0b42958b1e0d6\r\n')
        assert p.authenticated


def test_parser_rejected():
    p = auth.SASLParser()
    p.feed(b'REJECTED EXTERNAL\r\n')
    assert not p.authenticated