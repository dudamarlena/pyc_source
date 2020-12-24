# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/collective/allowtypes/tests/test_setup.py
# Compiled at: 2008-11-10 16:48:46
__author__ = 'Ramon Bartl <ramon.bartl@inquant.de>'
__docformat__ = 'plaintext'
from Products.CMFCore.utils import getToolByName
from zope.component import queryMultiAdapter
from base import PackageTestCase

class TestSetup(PackageTestCase):
    __module__ = __name__

    def test_view_registered(self):
        view = queryMultiAdapter((self.portal, self.portal.REQUEST), name='allowtypes')
        self.failUnless(view is not None)
        return

    def test_configlet_registered(self):
        cp = getToolByName(self.portal, 'portal_controlpanel')
        self.failUnless('allowtypesconfiglet' in [ action.getId() for action in cp.listActions() ])


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestSetup))
    return suite