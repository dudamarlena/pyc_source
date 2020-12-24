# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: C:\Users\Auzzy\Documents\git\pyinq\examples\suite_structure.py
# Compiled at: 2013-10-27 20:36:12
from pyinq.tags import *

@beforeModule
def setupModule():
    print 'set up module'


@afterModule
def teardownModule():
    print 'tear down module'


@beforeSuite
def setupGlobalSuite():
    print 'setting up global suite'


@beforeSuite(suite='suite1')
def setupSuite1():
    print 'setup suite 1'


@afterSuite(suite='suite1')
def teardownSuite1():
    print 'tear down suite 1'


@testClass
class Class1:

    @beforeClass
    def setup():
        print 'setup Class1'

    @beforeSuite(suite='suite4')
    def setupSuite4():
        print 'setup suite 4'

    @test(suite='suite1')
    def test1():
        print 'test1 in Class1'

    @test(suite='suite2')
    def test2():
        print 'test2 in Class1'

    @test(suite='suite3')
    def test3():
        print 'test3 in Class1'

    @test
    def test4():
        print 'test4 in Class1'

    @test(suite='suite4')
    def suite_fixture_test1():
        print 'test1 in suite4'

    @afterClass
    def teardown():
        print 'teardown Class1'


@testClass
class Class2:

    @before
    def setup():
        print 'setup test in Class2'

    @test(suite='suite1')
    def test5():
        print 'test5 in Class2'

    @test(suite='suite2')
    def test6():
        print 'test6 in Class2'

    @test(suite='suite3')
    def test7():
        print 'test7 in Class2'

    @test
    def test8():
        print 'test8 in Class2'

    @test(suite='suite4')
    def suite_fixture_test2():
        print 'test2 in suite4'

    @after
    def teardown():
        print 'teardown test in Class2'


@afterSuite(suite='suite2')
def teardownSuite2():
    print 'tear down suite 2'


@afterSuite
def teardownGlobalSuite():
    print 'tearing down global suite'