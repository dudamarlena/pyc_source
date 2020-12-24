# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
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