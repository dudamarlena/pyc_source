# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.15-x86_64/egg/foxylib/tools/entity/calendar/dayofweek/locale/ko/tests/test_dayofweek_span_entity_ko.py
# Compiled at: 2020-01-28 18:03:18
# Size of source mod 2**32: 1425 bytes
import logging
from pprint import pprint
from unittest import TestCase
from foxylib.tools.entity.calendar.dayofweek.locale.ko.dayofweek_entity_ko import DayofweekEntityKo
from foxylib.tools.entity.calendar.dayofweek.locale.ko.dayofweek_span_entity_ko import DayofweekSpanEntityKo
from foxylib.tools.log.foxylib_logger import FoxylibLogger

class TestDayofweekSpanEntityKo(TestCase):

    @classmethod
    def setUpClass(cls):
        FoxylibLogger.attach_stderr2loggers(logging.DEBUG)

    def test_01(self):
        hyp = DayofweekSpanEntityKo.str2entity_list('월-목')
        ref = [{'span':(0, 3),  'text':'월-목',  'value':('monday', 'thursday')}]
        self.assertEqual(hyp, ref)

    def test_02(self):
        hyp = DayofweekSpanEntityKo.str2entity_list('월 ~ 목요일, 금')
        ref = [{'span':(9, 10),  'text':'금',  'value':('friday', )},
         {'span':(0, 7), 
          'text':'월 ~ 목요일',  'value':('monday', 'thursday')}]
        self.assertEqual(hyp, ref)

    def test_03(self):
        hyp = DayofweekSpanEntityKo.str2entity_list('월수금')
        ref = [{'span':(0, 1),  'text':'월',  'value':('monday', )},
         {'span':(1, 2), 
          'text':'수',  'value':('wednesday', )},
         {'span':(2, 3), 
          'text':'금',  'value':('friday', )}]
        self.assertEqual(hyp, ref)