# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\Auzzy\Documents\git\pyinq\examples\skip_fixtures.py
# Compiled at: 2013-10-27 20:36:12
from pyinq.tags import *
from pyinq.asserts import *

@beforeSuite
@skip
def setup7():
    eval_true(False)


@skip
@beforeSuite
def setup8():
    eval_true(False)


@beforeModule
@skip
def setup5():
    eval_true(False)


@skip
@beforeModule
def setup6():
    eval_true(False)


@beforeClass
@skip
def setup3():
    eval_true(False)


@skip
@beforeClass
def setup4():
    eval_true(False)


@before
@skip
def setup1():
    eval_true(False)


@skip
@before
def setup2():
    eval_true(False)


@test
def test1():
    assert True