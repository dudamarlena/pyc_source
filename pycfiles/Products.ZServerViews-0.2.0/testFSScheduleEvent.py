# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/Products/ZScheduler/tests/testFSScheduleEvent.py
# Compiled at: 2015-07-18 19:40:58
import os
from Testing import ZopeTestCase
ZopeTestCase.installProduct('ZScheduler')
try:
    __file__
except NameError:
    _prefix = os.path.abspath(curdir)
else:
    _prefix = os.path.abspath(os.path.dirname(__file__))

class TestFSScheduleEvent(ZopeTestCase.ZopeTestCase):

    def _makeOne(self, id, filename='event.sched'):
        from Products.ZScheduler.FSZScheduleEvent import FSZScheduleEvent
        return FSZScheduleEvent(id, os.path.join(_prefix, filename))

    def _extractFile(self):
        path = os.path.join(_prefix, 'event.sched')
        f = open(path, 'rb')
        try:
            data = f.read()
        finally:
            f.close()

        return (
         path, data)

    def test_ctor(self):
        path, ref = self._extractFile()
        event = self._makeOne('test_file')
        self.assertEqual(event.day_of_month, '*')
        self.assertEqual(event.day_of_week, '*')
        self.assertEqual(event.hour, '1')
        self.assertEqual(event.minute, '1')
        self.assertEqual(event.month, '3,6,9,12')
        self.assertEqual(event.tz, 'EADT')


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestFSScheduleEvent))
    return suite