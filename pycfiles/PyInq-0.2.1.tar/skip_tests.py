# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\Auzzy\Documents\git\pyinq\examples\skip_tests.py
# Compiled at: 2013-10-27 20:36:12
from pyinq.tags import *

@testClass
class Class(object):

    @skip
    @test
    def test1():
        assert False

    @test
    @skip
    def test2():
        assert False

    @test
    def test3():
        assert True

    @skipIf(True)
    @test
    def test4():
        assert False

    @test
    @skipIf(True)
    def test5():
        assert False

    @skipIf(False)
    @test
    def test6():
        assert True

    @test
    @skipIf(False)
    def test7():
        assert True

    @skipUnless(True)
    @test
    def test8():
        assert True

    @test
    @skipUnless(True)
    def test9():
        assert True

    @skipUnless(False)
    @test
    def test10():
        assert False

    @test
    @skipUnless(False)
    def test11():
        assert False


@skip
@test
def test1():
    assert False


@test
@skip
def test2():
    assert False


@test
def test3():
    assert True


@skipIf(True)
@test
def test4():
    assert False


@test
@skipIf(True)
def test5():
    assert False


@skipIf(False)
@test
def test6():
    assert True


@test
@skipIf(False)
def test7():
    assert True


@skipUnless(True)
@test
def test8():
    assert True


@test
@skipUnless(True)
def test9():
    assert True


@skipUnless(False)
@test
def test10():
    assert False


@test
@skipUnless(False)
def test11():
    assert False