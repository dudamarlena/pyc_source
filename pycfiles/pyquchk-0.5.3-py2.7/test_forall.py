# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/tests/test_forall.py
# Compiled at: 2013-09-21 05:43:10
from pyquchk import *
from pyquchk.arbitraries import *
from pytest import *

def test_simple_true():
    assert for_all(lambda x: x * 2 / 2 == x, x=int_)


def test_simple_false():
    assert not for_all(lambda x: x * 3 / 2 == x, x=int_)


def test_float_add_associativity():
    assert not for_all(lambda a, b, c: a + (b + c) == a + b + c, a=float, b=float, c=float)
    assert not for_all(lambda a, b, c: a + (b + c) == a + b + c, a=float_(1, 1.1), b=float_(1, 1.1), c=float_(1, 1.1))
    assert not for_all(lambda lst: sum(lst) == sum(reversed(lst)), lst=list_(length=int_(1, 20), elements=float_()))


def test_assume():
    assert not for_all(lambda x, y: len(x) == len(y), x=list, y=list)
    res = for_all(lambda x, y: assume(len(x) == len(y)) is None and len(x) == len(y), x=list, y=list)
    assert res
    assert len(res.datas) == 500
    with raises(RuntimeError):
        for_all(lambda x: assume(False), x=int)