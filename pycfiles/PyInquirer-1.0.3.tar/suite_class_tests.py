# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
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