# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/iqpp/plone/rotating/tests/test_rotating.py
# Compiled at: 2008-08-04 04:28:54
from AccessControl import Unauthorized
from DateTime import DateTime
from zope.interface import directlyProvides
from zope.component import provideUtility, queryUtility
from Products.CMFCore.utils import getToolByName
from Products.AdvancedQuery import In, Eq, Ge, Le
from base import RotatingTestCase
from iqpp.plone.rotating.interfaces import IRotating
from iqpp.plone.rotating.interfaces import IRotatingOptions

class TestRotating(RotatingTestCase):
    """
    """
    __module__ = __name__

    def afterSetUp(self):
        """
        """
        self.loginAsPortalOwner()
        self.folder.invokeFactory('Topic', id='topic')
        self.topic = self.folder.topic
        crit = self.topic.addCriterion('portal_type', 'ATSimpleStringCriterion')
        crit.setValue('Image')
        self.folder.invokeFactory('Image', id='test_1')
        self.folder.invokeFactory('Image', id='test_2')
        self.folder.invokeFactory('Image', id='test_3')
        self.folder.invokeFactory('Image', id='test_4')

    def testRotating_1(self):
        """Is always a item found?
        """
        r = IRotating(self.topic)
        for i in range(1, 10):
            self.failIf(r.getItem() is None)

        return

    def testRotatingLimit(self):
        """Test limit
        """
        r = IRotating(self.topic)
        items = r.getItems(limit=4)
        self.failUnless(len(items), 4)
        for item in items:
            self.failUnless(item['id'] in [ o.id for o in self.topic.queryCatalog() ])

        item_ids = [ item['id'] for item in items ]
        for id in ('test_1', 'test_2', 'test_3', 'test_4'):
            self.failUnless(id in item_ids)

    def testRotatingSelected_1(self):
        """No reset
        """
        ro = IRotatingOptions(self.topic)
        ro.setOptions(show_already_selected=False, reset_already_selected=False)
        r = IRotating(self.topic)
        items = []
        for i in range(0, 4):
            item = r.getItem()
            items.append(item)

        item_ids = [ item['id'] for item in items ]
        for id in ('test_1', 'test_2', 'test_3', 'test_4'):
            self.failUnless(id in item_ids)

        item = r.getItem()
        self.failUnless(item is None)
        items = r.getItems()
        self.failUnless(items == [])
        return

    def testRotatingSelected_2(self):
        """Reset
        """
        ro = IRotatingOptions(self.topic)
        ro.setOptions(show_already_selected=False, reset_already_selected=True)
        r = IRotating(self.topic)
        items = []
        for i in range(0, 4):
            item = r.getItem()
            items.append(item)

        item_ids = [ item['id'] for item in items ]
        for id in ('test_1', 'test_2', 'test_3', 'test_4'):
            self.failUnless(id in item_ids)

        items = []
        for i in range(0, 4):
            item = r.getItem()
            items.append(item)

        item_ids = [ item['id'] for item in items ]
        for id in ('test_1', 'test_2', 'test_3', 'test_4'):
            self.failUnless(id in item_ids)

    def testRotatingDateUpdate_1(self):
        """
        """
        ro = IRotatingOptions(self.topic)
        ro.setOptions(update_intervall=1)
        r = IRotating(self.topic)
        result_1 = r.getItem()
        self.failIf(result_1 is None)
        for i in range(0, 10):
            result_2 = r.getItem()
            self.failUnless(result_1['id'] == result_2['id'])

        return


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestRotating))
    return suite