# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/Products/ZScheduler/tests/testDummy.py
# Compiled at: 2015-07-18 19:40:58
from Testing import ZopeTestCase

class TestDummy(ZopeTestCase.ZopeTestCase):

    def setUp(self):
        pass

    def testImport(self):
        from Products.ZScheduler.timers.Dummy import Dummy


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestDummy))
    return suite