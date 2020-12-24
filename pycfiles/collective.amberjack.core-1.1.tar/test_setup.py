# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
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