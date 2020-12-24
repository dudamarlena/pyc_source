# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\Auzzy\Documents\git\pyinq\examples\skip_class_tests.py
# Compiled at: 2013-10-27 20:36:12
from pyinq.tags import *
from pyinq.asserts import *

@testClass
@skip
class Test1(object):

    @BeforeClass
    def init():
        eval_true(False)

    @test
    def test1():
        assert False


@skip
@testClass
class Test2:

    @BeforeClass
    def init():
        eval_true(False)

    @test(suite='suite1')
    def test2():
        assert False