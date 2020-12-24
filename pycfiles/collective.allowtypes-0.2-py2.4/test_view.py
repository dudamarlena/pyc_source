# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/collective/allowtypes/tests/test_view.py
# Compiled at: 2008-11-10 16:50:41
__author__ = 'Ramon Bartl <ramon.bartl@inquant.de>'
__docformat__ = 'plaintext'
from zope.component import queryMultiAdapter
from base import PackageTestCase

class TestView(PackageTestCase):
    __module__ = __name__

    def afterSetUp(self):
        self.view = queryMultiAdapter((self.portal, self.portal.REQUEST), name='allowtypes')

    def test_document_allowed_under_folder(self):
        self.failUnless('Document' in [ t['type'] for t in self.view.allowed(self.folder) ])


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestView))
    return suite