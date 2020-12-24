# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/klmitch/devel/src/dtest/tests/test_inheritance.py
# Compiled at: 2011-04-11 16:22:28
from dtest import *
from dtest.util import *

class TestInheritanceBase(DTestCase):
    class_setup = None
    instance_setup = None

    @classmethod
    def setUpClass(cls):
        assert_is_none(cls.class_setup)
        cls.class_setup = True

    @classmethod
    def tearDownClass(cls):
        assert_false(cls.class_setup)

    def setUp(self):
        assert_is_none(self.instance_setup)
        self.instance_setup = True

    def tearDown(self):
        assert_false(self.instance_setup)


class TestInheritance(TestInheritanceBase):

    @attr(must_skip=True)
    def test_inheritance(self):
        assert_true(self.class_setup)
        assert_true(self.instance_setup)
        TestInheritanceBase.class_setup = False
        self.instance_setup = False


class TestInheritanceTwo(TestInheritance):

    def test_inheritance(self):
        super(TestInheritanceTwo, self).test_inheritance()