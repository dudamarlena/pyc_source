# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
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