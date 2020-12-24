# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.15-x86_64/egg/foxylib/tools/entity/calendar/hms/locale/ko/tests/test_hms_entity_ko.py
# Compiled at: 2020-01-28 20:29:02
# Size of source mod 2**32: 640 bytes
import logging
from unittest import TestCase
from foxylib.tools.log.foxylib_logger import FoxylibLogger

class TestTimespanEntityKo(TestCase):

    @classmethod
    def setUpClass(cls):
        FoxylibLogger.attach_stderr2loggers(logging.DEBUG)

    def test_01(self):
        str_in = '오후 3-6시'

    def test_02(self):
        str_in = '10-4'

    def test_03(self):
        str_in = '10시-11시'

    def test_04(self):
        str_in = '10 am - 11 pm'

    def test_05(self):
        str_in = '6pm - 2am'

    def test_06(self):
        str_in = '6:00 - 2:00'

    def test_07(self):
        str_in = '오후 6:00 - 새벽 2:00'