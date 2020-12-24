# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/tests/test_dummy.py
# Compiled at: 2020-03-03 07:34:32
from unittest import TestCase, skip

class UnitTest(TestCase):

    def test_pass(self):
        self.assertTrue(True)

    @skip('Will always fail')
    def test_fail(self):
        self.assertTrue(False)

    @skip('Will also always fail')
    def test_fail_2(self):
        self.assertTrue(False)