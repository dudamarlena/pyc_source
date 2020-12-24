# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/csams/git_repos/personal/parsr/lib/python3.6/site-packages/parsr/tests/test_opt.py
# Compiled at: 2019-01-13 18:16:44
# Size of source mod 2**32: 211 bytes
from parsr import Char, Opt

def test_opt():
    a = Opt(Char('a'))
    if not a('a') == 'a':
        raise AssertionError
    elif not a('b') is None:
        raise AssertionError


def test_opt_default():
    a = Opt(Char('a'), 'Default')
    assert a('b') == 'Default'