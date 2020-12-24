# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.15-x86_64/egg/foxylib/tools/videogame/overwatch/hero/tests/test_overwatch_hero.py
# Compiled at: 2020-02-07 15:10:57
# Size of source mod 2**32: 743 bytes
import logging
from unittest import TestCase
from future.utils import lfilter
from foxylib.tools.log.foxylib_logger import FoxylibLogger
from foxylib.tools.videogame.overwatch.hero.overwatch_hero import OverwatchHero

class TestOverwatchHero(TestCase):

    @classmethod
    def setUpClass(cls):
        FoxylibLogger.attach_stderr2loggers(logging.DEBUG)

    def test_01(self):
        logger = FoxylibLogger.func_level2logger(self.test_01, logging.DEBUG)
        j_brigitte = OverwatchHero.codename2j(OverwatchHero.Codename.BRIGITTE)
        self.assertTrue(j_brigitte)
        self.assertEqual(OverwatchHero.j_lang2name(j_brigitte, 'en'), 'Brigitte')
        self.assertEqual(OverwatchHero.j_lang2name(j_brigitte, 'ko'), '브리기테')