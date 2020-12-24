# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\Auzzy\Documents\git\pyinq\examples\fixture_asserts.py
# Compiled at: 2013-10-27 20:36:12
from pyinq.tags import *
from pyinq.asserts import *

@beforeClass
def setupClass():
    assert_true(False)


@before
def setup():
    assert_true(False)


@test
def test():
    print 'TEST'
    assert_true(False)


@after
def teardown():
    assert_true('AFTER')


@afterClass
def teardownClass():
    assert_true(True)