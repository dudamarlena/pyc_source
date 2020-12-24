# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/nowandnext/tests/test_basic.py
# Compiled at: 2009-05-11 19:02:38
import unittest, datetime, pprint
from nowandnext.utils.cmdline import cmdline
from nowandnext.calendar.calQuery import CalQuery, CalendarException, NoCalendarEntry

class test_basic(cmdline):
    ONE_DAY = datetime.timedelta(days=1)
    HALF_DAY = datetime.timedelta(days=0.5)
    TWO_DAYS = ONE_DAY * 2
    CFG = 'resonance_pinger.cfg'

    def setUp(self):
        configpath = self.getConfigFileLocation(self.CFG)
        config = self.getconfiguration(configpath)
        self.calargs = (
         config.get('pinger', 'account'),
         config.get('pinger', 'password'),
         config.get('pinger', 'calendar_name'))
        self.cal = CalQuery(*self.calargs)

    def tearDown(self):
        pass