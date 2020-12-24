# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/anz/dashboard/tests/test_calendarwidgetview.py
# Compiled at: 2010-09-26 21:53:53
import os, sys
from DateTime import DateTime
if __name__ == '__main__':
    execfile(os.path.join(sys.path[0], 'framework.py'))
from anz.dashboard.tests.base import AnzDashBoardTestCase

class TestCalendarWidgetView(AnzDashBoardTestCase):
    __module__ = __name__

    def afterSetUp(self):
        self.wf = self.portal.portal_workflow
        self.folder.invokeFactory(type_name='Document', id='doc1', title='doc 1')
        self.folder.doc1.indexObject()
        self.folder.invokeFactory(type_name='Anz Dashboard', id='dashboard1', title='dashboard 1')
        self.folder.dashboard1.indexObject()

    def test_viewApplied(self):
        view = self.folder.doc1.restrictedTraverse('@@calendarWidget', None)
        self.assert_(view is None)
        view = self.folder.dashboard1.restrictedTraverse('@@calendarWidget', None)
        self.assert_(view is not None)
        return

    def test_getReviewStateString(self):
        view = self.folder.dashboard1.restrictedTraverse('@@calendarWidget', None)
        result = 'review_state=published&amp;'
        self.assertEqual(result, view.getReviewStateString(False)['stateStr'])
        self.portal.portal_calendar.calendar_states = ('visible', 'published')
        result = 'review_state=visible&amp;review_state=published&amp;'
        self.assertEqual(result, view.getReviewStateString(False)['stateStr'])
        return

    def test_events(self):
        self.setRoles(['Manager'])
        self._addEvent('1', DateTime('2010/02/01 10:00:00'), DateTime('2010/02/01 12:00:00'))
        self._addEvent('2', DateTime('2010/02/02 11:00:00'), DateTime('2010/02/02 12:00:00'))
        self._addEvent('3', DateTime('2010/01/28 10:00:00'), DateTime('2010/02/04 12:00:00'))
        self._addEvent('4', DateTime('2010/02/02 10:00:00'), DateTime('2010/02/05 12:00:00'))
        self._addEvent('5', DateTime('2010/02/05 10:00:00'), DateTime('2010/02/15 12:00:00'))
        view = self.folder.dashboard1.restrictedTraverse('@@calendarWidget', None)
        start = '2010/02/01 10:00:00'
        end = '2010/02/07 10:00:00'
        ret = view.events(start, end, retJson=False)
        self.assertEqual(ret['success'], True)
        self.assertEqual(len(ret['events'].keys()), 7)
        events = ret['events']
        self.assertEqual(len(events['20100201']), 2)
        self.assertEqual(len(events['20100202']), 3)
        self.assertEqual(len(events['20100203']), 2)
        self.assertEqual(len(events['20100204']), 2)
        self.assertEqual(len(events['20100205']), 2)
        self.assertEqual(len(events['20100206']), 1)
        self.assertEqual(len(events['20100207']), 1)
        start = 'wrong start date'
        end = DateTime('2010/02/07 10:00:00')
        ret = view.events(start, end, retJson=False)
        self.assertEqual(ret['success'], False)
        self.assert_(ret['msg'] != None)
        return

    def _addEvent(self, id, start, end):
        self.folder.invokeFactory(type_name='Event', id=id, title='event %s' % id, startDate=start, endDate=end)
        event = getattr(self.folder, id)
        event.indexObject()
        self.wf.doActionFor(event, 'publish')


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestCalendarWidgetView))
    return suite


if __name__ == '__main__':
    framework()