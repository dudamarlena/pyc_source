# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/collective/portlet/recentactivity/tests/test_utils.py
# Compiled at: 2010-05-19 10:20:52
from collective.portlet.recentactivity.tests.base import TestCase
from Products.CMFCore.utils import getToolByName
from collective.portlet.recentactivity.utils import *

class TestComputeTime(TestCase):
    __module__ = __name__

    def test_seconds(self):
        self.assertEquals(compute_time(12), {'hours': 0, 'minutes': 0, 'days': 0})

    def test_minutes(self):
        self.assertEquals(compute_time(62), {'hours': 0, 'minutes': 1, 'days': 0})

    def test_hours(self):
        self.assertEquals(compute_time(7260), {'hours': 2, 'minutes': 1, 'days': 0})

    def test_days(self):
        self.assertEquals(compute_time(172800), {'hours': 0, 'minutes': 0, 'days': 2})


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestComputeTime))
    return suite