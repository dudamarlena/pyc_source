# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/csams/git_repos/personal/parsr/lib/python3.6/site-packages/parsr/examples/tests/test_arith.py
# Compiled at: 2019-05-28 16:55:16
# Size of source mod 2**32: 490 bytes
from parsr.examples.arith import evaluate

def test_single_ops():
    if not evaluate('2+3') == 5:
        raise AssertionError
    else:
        if not evaluate('1-3') == -2:
            raise AssertionError
        elif not evaluate('2*3') == 6:
            raise AssertionError
        assert evaluate('4/2') == 2


def test_multiple_ops():
    if not evaluate('2+3+4') == 9:
        raise AssertionError
    else:
        if not evaluate('1-3+2') == 0:
            raise AssertionError
        elif not evaluate('2*3*4') == 24:
            raise AssertionError
        assert evaluate('3*4/2') == 6


def test_nested():
    assert evaluate('24-2*(3+4)') == 10


def test_spaces():
    assert evaluate('24 - 2 * ( 3 + 4 )') == 10