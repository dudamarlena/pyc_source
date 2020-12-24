# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/nowandnext/tests/test_schedule_items.py
# Compiled at: 2009-05-11 19:02:38
import unittest, datetime, pprint, logging
log = logging.getLogger(__name__)
from nowandnext.tests.test_basic import test_basic
from nowandnext.calendar.scheduleevent import scheduleevent

class test_schedule_items(test_basic, unittest.TestCase):

    def testInstancesOneWeekFetch(self):
        now = datetime.datetime.now()
        evs1 = [ scheduleevent(e) for e in self.cal.getEventInstances(now, now + self.ONE_DAY * 3) ]
        evs2 = [ scheduleevent(e) for e in self.cal.getEventInstances(now + self.ONE_DAY, now + self.ONE_DAY * 2) ]

    def testGetPresenterEmails(self):
        now = datetime.datetime.now()
        evs1 = [ scheduleevent(e) for e in self.cal.getEventInstances(now, now + self.ONE_DAY * 21) ]
        email_dict = {}
        for ev in evs1:
            ev_description = ev.getDescriptionDict()
            try:
                email = ev_description['email']
                if email not in email_dict.keys():
                    email_dict[email] = []
                email_dict[email].append(ev)
            except KeyError, ke:
                log.warn('No email for %s' % str(ev))
                continue