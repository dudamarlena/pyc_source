# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/quintagroup/pingtool/tests/test_pinginfo.py
# Compiled at: 2009-03-31 04:47:32
from base import *

class TestPingInfo(TestCase):
    __module__ = __name__

    def afterSetUp(self):
        self.loginAsPortalOwner()
        self.pt1 = getToolByName(self.portal, 'portal_pingtool')
        self.pt1.invokeFactory('PingInfo', id='pi1', title='Ping Info 1')

    def testAddedPingInfo(self):
        self.pi1 = getattr(self.pt1, 'pi1', None)
        self.pi1.setUrl('http://nohost')
        self.failUnlessEqual(self.pi1.getUrl(), 'http://nohost')
        self.failUnlessEqual(self.pi1.getMethod_name(), 'weblogUpdates.ping')
        self.pi1.setMethod_name('testmethod')
        self.failUnlessEqual(self.pi1.getMethod_name(), 'testmethod')
        self.pi1.setRss_version(self.pi1.Vocabulary('rss_version')[0][(-1)])
        self.failUnlessEqual(self.pi1.getRss_version(), 'RSS2')
        return


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestPingInfo))
    return suite