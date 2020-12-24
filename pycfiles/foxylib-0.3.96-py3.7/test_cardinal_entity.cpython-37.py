# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.15-x86_64/egg/foxylib/tools/entity/cardinal/tests/test_cardinal_entity.py
# Compiled at: 2020-01-24 12:49:23
# Size of source mod 2**32: 489 bytes
import logging
from unittest import TestCase
from foxylib.tools.entity.cardinal.cardinal_entity import CardinalEntity
from foxylib.tools.log.foxylib_logger import FoxylibLogger

class TestCardinalEntity(TestCase):

    @classmethod
    def setUpClass(cls):
        FoxylibLogger.attach_stderr2loggers(logging.DEBUG)

    def test_01(self):
        hyp = CardinalEntity.str2entity_list('46')
        ref = [{'span':(0, 2),  'text':'46',  'value':46}]
        self.assertEqual(hyp, ref)