# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/Products/eCards/tests/test_interfaces.py
# Compiled at: 2008-11-11 20:26:20
import os, sys
if __name__ == '__main__':
    execfile(os.path.join(sys.path[0], 'framework.py'))
from Products.eCards.tests import base
from Products.CMFCore.utils import getToolByName
from Products.eCards.interfaces import IECardCollection, IECard, IECardCollectionView, IECardPopupView
from zope.interface.verify import verifyObject, verifyClass
from Products.eCards.content.ecard import eCard
from Products.eCards.content.ecardcollection import eCardCollection
from Products.eCards.browser import eCardCollectionView, eCardPopupView

class TestProductInterfaces(base.eCardTestCase):
    """ Ensure that our eCard product classes and objects
        fullfill their contractual interfaces
    """
    __module__ = __name__

    def afterSetUp(self):
        pass

    def testContentInterfaces(self):
        """ Some basic boiler plate testing of Interfaces and objects"""
        self.failUnless(IECardCollection.implementedBy(eCardCollection))
        self.failUnless(verifyClass(IECardCollection, eCardCollection))
        self.failUnless(IECard.implementedBy(eCard))
        self.failUnless(verifyClass(IECard, eCard))

    def testObjectInstances(self):
        self.setupContainedECard()
        self.failUnless(isinstance(self.folder.collection, eCardCollection))
        self.failUnless(isinstance(self.folder.collection.ecard, eCard))

    def testContentObjectsVerify(self):
        self.setupContainedECard()
        self.failUnless(verifyObject(IECardCollection, self.folder.collection))
        self.failUnless(verifyObject(IECard, self.folder.collection.ecard))

    def testBrowserViewInterfaces(self):
        self.failUnless(IECardCollectionView.implementedBy(eCardCollectionView))
        self.failUnless(verifyClass(IECardCollectionView, eCardCollectionView))
        self.failUnless(IECardPopupView.implementedBy(eCardPopupView))
        self.failUnless(verifyClass(IECardPopupView, eCardPopupView))

    def testBrowserViewsVerify(self):
        self.setupCollection()
        self.setupContainedECard()
        collection_view = self.folder.collection.restrictedTraverse('ecardcollection_browserview')
        popup_view = self.folder.collection.ecard.restrictedTraverse('ecardpopup_browserview')
        self.failUnless(isinstance(collection_view, eCardCollectionView))
        self.failUnless(verifyObject(IECardCollectionView, collection_view))
        self.failUnless(isinstance(popup_view, eCardPopupView))
        self.failUnless(verifyObject(IECardPopupView, popup_view))


if __name__ == '__main__':
    framework()

def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestProductInterfaces))
    return suite