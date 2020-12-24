# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
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