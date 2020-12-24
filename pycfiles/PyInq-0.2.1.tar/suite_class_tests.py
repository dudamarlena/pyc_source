# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\Auzzy\Documents\git\pyinq\examples\suite_class_tests.py
# Compiled at: 2013-10-27 20:36:12
from pyinq.tags import *

@testClass(suite='suite1')
class Class1(object):

    @test
    def test1():
        assert True

    @test
    def test2():
        assert True


@testClass(suite='suite2')
class Class2(object):

    @test(suite='suite1')
    def test3():
        assert True

    @test(suite='suite2')
    def test4():
        assert True


@testClass
class Class3(object):

    @test
    def test5():
        assert True

    @test
    def test6():
        assert True