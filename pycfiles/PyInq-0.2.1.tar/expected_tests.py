# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\Auzzy\Documents\git\pyinq\examples\expected_tests.py
# Compiled at: 2013-10-27 20:36:12
from pyinq.tags import *
from pyinq.asserts import *
import mod

@test(expect=ValueError)
def test1():
    mod.parse('hjhwr')
    assert_true(True)


@test(expect=WindowsError)
def test2():
    mod.parse('hjhwr')


@test(expect=ValueError)
def test3():
    parse('4')


def parse(val):
    int(val)