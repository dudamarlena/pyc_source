# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\Auzzy\Documents\git\pyinq\examples\assert_raises_tests.py
# Compiled at: 2013-11-14 20:26:07
from pyinq.tags import *
from pyinq.asserts import *

@test
def test1():
    assert_raises(ValueError, parse, 'hjhwr')
    eval_true(True)


@test
def test2():
    assert_raises(WindowsError, parse, 'hjhwr')
    eval_true(True)


@test
def test3():
    assert_raises(ValueError, parse, '4')
    eval_true(True)


@test
def test4():
    eval_raises(ValueError, parse, 'hjhwr')
    eval_true(True)


@test
def test5():
    eval_raises(WindowsError, parse, 'hjhwr')
    eval_true(True)


@test
def test6():
    eval_raises(ValueError, parse, '9')
    eval_true(True)


def parse(val):
    int(val)