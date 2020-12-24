# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
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