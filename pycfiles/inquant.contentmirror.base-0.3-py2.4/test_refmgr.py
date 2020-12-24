# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/inquant/contentmirror/base/tests/test_refmgr.py
# Compiled at: 2008-04-14 11:51:37
__author__ = 'Stefan Eletzhofer <stefan.eletzhofer@inquant.de>'
__docformat__ = 'plaintext'
__revision__ = '$Revision: 62293 $'
__version__ = '$Revision: 62293 $'[11:-2]
import unittest
from zope import component
from zope import interface
from zope.app.testing import ztapi
from inquant.contentmirror.base.interfaces import IMirroredContentManager
from inquant.contentmirror.base.interfaces import IMirrorContentLocator
from inquant.contentmirror.base.interfaces import IMirrorReferenceManager
from inquant.contentmirror.base.manager import DefaultReferenceManager
from inquant.contentmirror.base.traverser import MirrorObjectTraverser
from inquant.contentmirror.base.tests import base

class TestRefmgr(base.CMTestCase):
    __module__ = __name__

    def afterSetUp(self):
        self.setRoles(('Manager', ))
        self.folder.invokeFactory('Folder', 'f1')
        self.folder.invokeFactory('Folder', 'f2')
        self.f1 = self.folder.f1
        self.f2 = self.folder.f2
        self.f1.invokeFactory('Document', 'doc', title='Muh')
        component.provideAdapter(MirrorObjectTraverser)
        component.provideAdapter(DefaultReferenceManager)
        manager = component.getUtility(IMirroredContentManager)
        manager.addMirror(self.f1.doc, self.f2)
        self.original = self.f1.doc
        self.mirror = IMirrorContentLocator(self.f2).locate('doc')

    def testRefMgrLookup(self):
        self.failUnless(IMirrorReferenceManager(self.original))
        self.failUnless(IMirrorReferenceManager(self.mirror))

    def testRefMgrKeys(self):
        rm = IMirrorReferenceManager(self.mirror)
        self.assertEqual(len(rm.storage.keys()), 1)
        self.assertEqual(rm.storage.keys(), ['/plone/Members/test_user_1_/f2/doc'])

    def testIsMirror(self):
        rm = IMirrorReferenceManager(self.mirror)
        self.failUnless(rm.isMirror(self.mirror, self.f2))
        rm = IMirrorReferenceManager(self.original)
        self.failUnless(rm.isMirror(self.mirror, self.f2))

    def testGetOriginal(self):
        rm = IMirrorReferenceManager(self.mirror)
        self.assertEqual(self.original.getPhysicalPath(), rm.getOriginal().getPhysicalPath())


def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestRefmgr))
    return suite