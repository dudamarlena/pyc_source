# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/csams/git_repos/personal/parsr/lib/python3.6/site-packages/parsr/tests/test_many.py
# Compiled at: 2019-05-28 16:56:48
# Size of source mod 2**32: 1217 bytes
import pytest
from parsr import Char, Many

def test_many():
    a = Char('a')
    b = Char('b')
    x = Char('x')
    xs = Many(x)
    if not xs('') == []:
        raise AssertionError
    else:
        if not xs('a') == []:
            raise AssertionError
        else:
            if not xs('x') == ['x']:
                raise AssertionError
            else:
                if not xs('xxxxx') == ['x', 'x', 'x', 'x', 'x']:
                    raise AssertionError
                else:
                    if not xs('xxxxb') == ['x', 'x', 'x', 'x']:
                        raise AssertionError
                    else:
                        ab = Many(a + b)
                        assert ab('') == []
                    assert ab('ba') == []
                assert ab('ab') == [['a', 'b']]
            assert ab('ababab') == [['a', 'b'], ['a', 'b'], ['a', 'b']]
        ab = Many(a | b)
        assert ab('aababb') == ['a', 'a', 'b', 'a', 'b', 'b']


def test_many1():
    a = Char('a')
    b = Char('b')
    x = Char('x')
    xs = Many(x, lower=1)
    with pytest.raises(Exception):
        xs('')
    with pytest.raises(Exception):
        xs('a')
    if not xs('x') == ['x']:
        raise AssertionError
    else:
        if not xs('xxxxx') == ['x', 'x', 'x', 'x', 'x']:
            raise AssertionError
        else:
            if not xs('xxxxb') == ['x', 'x', 'x', 'x']:
                raise AssertionError
            else:
                ab = Many((a + b), lower=1)
                with pytest.raises(Exception):
                    ab('')
                with pytest.raises(Exception):
                    ab('ba')
                assert ab('ab') == [['a', 'b']]
            assert ab('ababab') == [['a', 'b'], ['a', 'b'], ['a', 'b']]
        ab = Many((a | b), lower=1)
        assert ab('aababb') == ['a', 'a', 'b', 'a', 'b', 'b']