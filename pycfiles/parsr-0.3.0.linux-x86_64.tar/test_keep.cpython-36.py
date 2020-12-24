# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/csams/git_repos/personal/parsr/lib/python3.6/site-packages/parsr/tests/test_keep.py
# Compiled at: 2019-01-13 18:16:03
# Size of source mod 2**32: 444 bytes
from parsr import Colon, QuotedString

def test_keepleft():
    key = QuotedString << Colon
    if not key('"key":') == 'key':
        raise AssertionError
    else:
        key = Colon << QuotedString
        assert key(':"key"') == ':'


def test_keepright():
    key = QuotedString >> Colon
    if not key('"key":') == ':':
        raise AssertionError
    else:
        key = Colon >> QuotedString
        assert key(':"key"') == 'key'


def test_middle():
    key = Colon >> QuotedString << Colon
    assert key(':"key":') == 'key'