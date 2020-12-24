# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/Products/ZScheduler/tests/testZScheduler.py
# Compiled at: 2015-07-18 19:40:58
from Testing import ZopeTestCase
from Products.PloneTestCase import PloneTestCase as ptc
from Products.ZScheduler.ZScheduleEvent import ZScheduleEvent
ZopeTestCase.installProduct('ZScheduler')
ptc.setupPloneSite(products=['ZScheduler'])

class TestScheduler(ptc.PloneTestCase):

    def afterSetUp(self):
        portal = self.app
        portal._setObject('event1', ZScheduleEvent('event1', 'testing', 'no callable'))
        portal._setObject('event2', ZScheduleEvent('event2', 'testing', 'no callable'))
        portal._setObject('event3', ZScheduleEvent('event3', 'testing', 'no callable'))
        self.event1 = portal.event1

    def testSetup(self):
        self.failUnless('ZSchedulerTool' in self.app.objectIds())

    def testQueueCore(self):
        self.assertEqual(self.portal.event1._active, False)
        self.assertEqual(self.portal.event1.active, False)
        catalog = self.app.ZSchedulerTool.queue
        self.assertEqual(len(catalog.searchResults()), 3)
        self.assertEqual(len(catalog.searchResults(active=False)), 3)

    def testSchedulerAPI(self):
        zscheduler = self.app.ZSchedulerTool
        self.assertEqual(len(zscheduler.events()), 0)
        self.assertEqual(len(zscheduler.events(active=True)), 0)
        self.assertEqual(len(zscheduler.events(active=False)), 3)
        self.event1.manage_editSchedule('EST', '5', '*', '*', '*', '*', True)
        self.assertEqual(zscheduler.events(active=True), [self.event1])


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestScheduler))
    return suite