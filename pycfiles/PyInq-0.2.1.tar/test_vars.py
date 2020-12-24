# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\Auzzy\Documents\git\pyinq\examples\test_vars.py
# Compiled at: 2013-10-27 20:36:12
import random
from pyinq.asserts import *
from pyinq.tags import *

@testClass
class TestSequenceFunctions:

    @before
    def setUp():
        self.seq = range(10)

    @test
    def test_shuffle():
        random.shuffle(self.seq)
        self.seq.sort()
        assert_equal(self.seq, range(10))
        assert_raises(TypeError, random.shuffle, (1, 2, 3))

    @test
    def test_choice():
        element = random.choice(self.seq)
        assert_true(element in self.seq)

    @test
    def test_sample():
        assert_raises(ValueError, random.sample, self.seq, 20)
        for element in random.sample(self.seq, 5):
            assert_in(element, self.seq)


@test(expect=NameError)
def outside_test():
    print self