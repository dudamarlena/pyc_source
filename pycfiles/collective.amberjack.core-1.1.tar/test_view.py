# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
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