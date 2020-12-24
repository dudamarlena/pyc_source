# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
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