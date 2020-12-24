# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\Auzzy\Documents\git\pyinq\examples\init.py
# Compiled at: 2013-10-27 20:36:12
from pyinq.asserts import *
from pyinq.tags import *

@testClass
class Class1:

    def __init__(self):
        self.num = 4

    @test
    def test1():
        assert_equal(self.num, 4)
        self.num += 1

    @test
    def test2():
        assert_equal(self.num, 4)
        self.num += 1