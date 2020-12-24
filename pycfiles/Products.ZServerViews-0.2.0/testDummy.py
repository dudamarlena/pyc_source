# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
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