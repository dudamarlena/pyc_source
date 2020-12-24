# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/Products/ZScheduler/tests/testCrontab.py
# Compiled at: 2015-07-18 19:40:58
from Testing.ZopeTestCase import ZopeTestCase

class TestCrontab(ZopeTestCase):

    def testImport(self):
        from Products.ZScheduler.timers.Crontab import Crontab


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestCrontab))
    return suite