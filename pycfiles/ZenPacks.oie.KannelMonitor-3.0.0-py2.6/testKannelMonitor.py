# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ZenPacks/oie/KannelMonitor/tests/testKannelMonitor.py
# Compiled at: 2010-09-01 21:26:14
import os, sys
if __name__ == '__main__':
    execfile(os.path.join(sys.path[0], 'framework.py'))
from Products.ZenTestCase.BaseTestCase import BaseTestCase

class TestKannelMonitor(BaseTestCase):

    def setUp(self):
        BaseTestCase.setUp(self)

    def testZenPack(self):
        from ZenPacks.oie.KannelMonitor import ZenPack
        self.failUnless(1)

    def testEventsSetup(self):
        self.failUnless(self.dmd.Events.Status.Kannel)

    def testTemplatesSetup(self):
        self.failUnless(self.dmd.Devices.rrdTemplates.KannelServer)

    def testCmd(self):
        device_class = self.dmd.Devices
        device = device_class.addDevice('test.box')
        datasource = device_class.rrdTemplates.KannelServer.datasources.kannel
        self.assertEqual(datasource.getCommand(device), '')


if __name__ == '__main__':
    framework()
else:

    def test_suite():
        from unittest import TestSuite, makeSuite
        suite = TestSuite()
        suite.addTest(makeSuite(TestKannelMonitor))
        return suite