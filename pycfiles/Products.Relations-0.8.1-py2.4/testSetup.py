# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-fat/egg/Products/Relations/tests/testSetup.py
# Compiled at: 2008-09-11 19:48:09
import os, sys
if __name__ == '__main__':
    execfile(os.path.join(sys.path[0], 'framework.py'))
from Products.PloneTestCase import PloneTestCase
import common
common.installWithinPortal()

class TestPloneSetup(PloneTestCase.PloneTestCase):
    __module__ = __name__

    def afterSetUp(self):
        self.loginAsPortalOwner()
        qi = self.portal.portal_quickinstaller
        qi.installProducts(('Relations', ))

    def testReinstall(self):
        self.loginAsPortalOwner()
        qi = self.portal.portal_quickinstaller
        qi.reinstallProducts(('Relations', ))


class TestCreateSnapshot(PloneTestCase.PloneTestCase):
    __module__ = __name__

    def testCreateSnapshot(self):
        self.loginAsPortalOwner()
        st = self.portal.portal_setup
        snapshot_id = st._mangleTimestampName('snapshot')
        st.createSnapshot(snapshot_id)


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestPloneSetup))
    suite.addTest(makeSuite(TestCreateSnapshot))
    return suite


if __name__ == '__main__':
    framework()