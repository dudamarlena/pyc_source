# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\tests\plugins\poweradminbf3\test_cmd_scramblemode.py
# Compiled at: 2016-03-08 18:42:10
from mock import Mock
from b3.config import CfgConfigParser
from b3.plugins.poweradminbf3 import Poweradminbf3Plugin
from tests.plugins.poweradminbf3 import Bf3TestCase

class Test_cmd_scramblemode(Bf3TestCase):

    def setUp(self):
        Bf3TestCase.setUp(self)
        self.conf = CfgConfigParser()
        self.conf.loadFromString('[commands]\nscramblemode: 20\n        ')
        self.p = Poweradminbf3Plugin(self.console, self.conf)
        self.p.onLoadConfig()
        self.p.onStartup()
        self.p._scrambler = Mock()
        self.superadmin.connects('superadmin')
        self.superadmin.clearMessageHistory()

    def test_no_arguments(self):
        self.superadmin.says('!scramblemode')
        self.assertEqual(["invalid data. Expecting 'random' or 'score'"], self.superadmin.message_history)
        self.assertFalse(self.p._scrambler.setStrategy.called)

    def test_bad_arguments(self):
        self.superadmin.says('!scramblemode f00')
        self.assertEqual(["invalid data. Expecting 'random' or 'score'"], self.superadmin.message_history)
        self.assertFalse(self.p._scrambler.setStrategy.called)

    def test_random(self):
        self.superadmin.says('!scramblemode random')
        self.assertEqual(['Scrambling strategy is now: random'], self.superadmin.message_history)
        self.p._scrambler.setStrategy.assert_called_once_with('random')

    def test_r(self):
        self.superadmin.says('!scramblemode r')
        self.assertEqual(['Scrambling strategy is now: random'], self.superadmin.message_history)
        self.p._scrambler.setStrategy.assert_called_once_with('random')

    def test_score(self):
        self.superadmin.says('!scramblemode score')
        self.assertEqual(['Scrambling strategy is now: score'], self.superadmin.message_history)
        self.p._scrambler.setStrategy.assert_called_once_with('score')

    def test_s(self):
        self.superadmin.says('!scramblemode s')
        self.assertEqual(['Scrambling strategy is now: score'], self.superadmin.message_history)
        self.p._scrambler.setStrategy.assert_called_once_with('score')