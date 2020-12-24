# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/klmitch/devel/src/dtest/tests/test_alternate.py
# Compiled at: 2011-04-11 11:42:34
from dtest import *
from dtest.util import *

class TestAlternate(DTestCase):
    alternate = None

    def setUp(self):
        assert_is_none(self.alternate)
        self.alternate = False

    def tearDown(self):
        assert_false(self.alternate)

    def test1(self):
        assert_false(self.alternate)

    @istest
    def test2(self):
        assert_true(self.alternate)

    @test2.setUp
    def alternateSetUp(self):
        assert_is_none(self.alternate)
        self.alternate = True

    @test2.tearDown
    def alternateTearDown(self):
        assert_true(self.alternate)