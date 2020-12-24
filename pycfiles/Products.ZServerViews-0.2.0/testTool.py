# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/Products/ZScheduler/tests/testTool.py
# Compiled at: 2015-07-18 19:40:58
from Testing import ZopeTestCase as ztc
from Products.PloneTestCase import PloneTestCase as ptc
from Products.ZScheduler.config import TOOLNAME
ztc.installProduct('ZScheduler')
ptc.setupPloneSite(products=['ZScheduler'])

class TestTool(ptc.PloneTestCase):

    def testSetup(self):
        self.failUnless(TOOLNAME in self.portal.objectIds())
        self.failUnless('ZSchedulerTool' in self.portal.getPhysicalRoot().objectIds())

    def testQueue(self):
        tool = getattr(self.portal, TOOLNAME)
        self.assertEqual(tool.queueValues(), [])


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestTool))
    return suite