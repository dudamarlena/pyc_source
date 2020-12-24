# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/collective/portlet/recentactivity/tests/test_viewlet.py
# Compiled at: 2010-05-19 10:20:52
import unittest
from AccessControl import Unauthorized
from collective.portlet.recentactivity.tests.base import TestCase
from collective.portlet.recentactivity.viewlet import RecentActivityViewlet
from Products.CMFCore.utils import getToolByName

class TestRecentActivityViewlet(TestCase):
    __module__ = __name__

    def afterSetUp(self):
        self.loginAsPortalOwner()
        self.setRoles(['Manager'])

    def testRecentActivityViewlet(self):
        request = self.app.REQUEST
        viewlet = RecentActivityViewlet(self.portal, request, None, None)
        viewlet.update()
        request = self.app.REQUEST
        viewlet = RecentActivityViewlet(self.portal, request, None, None)
        viewlet.update()
        return

    def test_recent_activities(self):
        pass

    def test_available(self):
        pass

    def test_recently_modified_link(self):
        pass


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestRecentActivityViewlet))
    return suite