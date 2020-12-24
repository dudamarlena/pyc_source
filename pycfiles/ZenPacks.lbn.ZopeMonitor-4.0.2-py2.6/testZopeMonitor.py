# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ZenPacks/lbn/ZopeMonitor/tests/testZopeMonitor.py
# Compiled at: 2013-01-08 07:16:47
from Products.ZenTestCase.BaseTestCase import BaseTestCase
import ZenPacks.lbn.ZopeMonitor

class TestZopeMonitor(BaseTestCase):

    def setUp(self):
        BaseTestCase.setUp(self)

    def testEventsSetup(self):
        self.failUnless(self.dmd.Events.Status.Zope)

    def testTemplatesSetup(self):
        self.failUnless(self.dmd.Devices.Server.rrdTemplates.ZopeServer)


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestZopeMonitor))
    return suite