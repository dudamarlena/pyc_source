# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/collective/portlet/recentactivity/tests/test_utility.py
# Compiled at: 2010-05-19 10:20:52
from collective.portlet.recentactivity.tests.base import TestCase
from Products.CMFCore.utils import getToolByName
from DateTime import DateTime
from Acquisition import aq_parent, aq_base
from datetime import datetime, timedelta
from zope.component import getUtility
from collective.portlet.recentactivity.interfaces import IRecentActivityUtility
from collective.portlet.recentactivity.utilities import RecentActivityUtility

class TestRecentActivityUtility(TestCase):
    __module__ = __name__

    def afterSetUp(self):
        self.setRoles(('Manager', ))
        self.activities = getUtility(IRecentActivityUtility)
        typetool = self.portal.portal_types
        typetool.constructContent('Document', self.portal, 'doc1')

    def testAddActivity(self):
        activity = self.activities.addActivity(DateTime(), 'added', 'johndoe', self.portal.doc1, aq_parent(self.portal.doc1))
        self.failUnless(activity)
        self.assert_(activity - int(DateTime() < 10))

    def testRecentActivity(self):
        activity = self.activities.addActivity(DateTime(), 'added', 'johndoe', self.portal.doc1, aq_parent(self.portal.doc1))
        activities = self.activities.getRecentActivity()
        self.assertEquals(len(activities), 1)
        self.assertEquals(activities[0][0], activity - int(DateTime() < 10))
        self.assertEquals(activities[0][1]['action'], 'added')
        self.assertEquals(aq_base(activities[0][1]['object']), aq_base(self.portal.doc1))
        self.assertEquals(activities[0][1]['object_url'], 'http://nohost/plone/doc1')
        self.assertEquals(aq_base(activities[0][1]['parent']), aq_base(self.portal))
        self.assertEquals(activities[0][1]['parent_url'], 'http://nohost/plone')
        self.assertEquals(activities[0][1]['user'], 'johndoe')
        new_id = self.activities.addActivity(DateTime() + 1, 'edited', 'johndoe', self.portal.doc1, aq_parent(self.portal.doc1))
        act = self.activities.getRecentActivity()


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestRecentActivityUtility))
    return suite