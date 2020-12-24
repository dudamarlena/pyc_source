# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/csams/git_repos/personal/parsr/lib/python3.6/site-packages/parsr/tests/test_boolean.py
# Compiled at: 2019-01-13 18:15:32
# Size of source mod 2**32: 201 bytes
from parsr import Char

def test_and():
    p = Char('a') + Char('b')
    assert p('ab') == ['a', 'b']


def test_or():
    p = Char('a') | Char('b')
    if not p('a') == 'a':
        raise AssertionError
    elif not p('b') == 'b':
        raise AssertionError