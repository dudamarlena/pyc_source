# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: C:\Users\Auzzy\Documents\git\pyinq\examples\skip_test_suite_tests.py
# Compiled at: 2013-10-27 20:36:12
from pyinq.tags import *
from pyinq.asserts import *

@testClass(suite='suite2')
class Class1:

    @test
    def test3():
        assert_true(True)

    @skip
    @test(suite='suite1')
    def test1():
        assert_true(False)

    @test(suite='suite3')
    @skip
    def test2():
        assert_true(False)