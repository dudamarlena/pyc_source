# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\tests\plugins\poweradminbf3\test_cmd_scramble.py
# Compiled at: 2016-03-08 18:42:10
from mock import Mock
from b3.config import CfgConfigParser
from b3.plugins.poweradminbf3 import Poweradminbf3Plugin
from tests.plugins.poweradminbf3 import Bf3TestCase

class Test_cmd_scramble(Bf3TestCase):

    def setUp(self):
        Bf3TestCase.setUp(self)
        self.conf = CfgConfigParser()
        self.conf.loadFromString('[commands]\nscramble: 20\n        ')
        self.p = Poweradminbf3Plugin(self.console, self.conf)
        self.p.onLoadConfig()
        self.p.onStartup()
        self.p._scrambler = Mock()
        self.superadmin.connects('superadmin')
        self.superadmin.clearMessageHistory()

    def test_none(self):
        self.p._scrambling_planned = None
        self.superadmin.says('!scramble')
        self.assertEqual(['Teams will be scrambled at next round start'], self.superadmin.message_history)
        self.assertTrue(self.p._scrambling_planned)
        return

    def test_true(self):
        self.p._scrambling_planned = True
        self.superadmin.says('!scramble')
        self.assertEqual(['Teams scrambling canceled for next round'], self.superadmin.message_history)
        self.assertFalse(self.p._scrambling_planned)

    def test_false(self):
        self.p._scrambling_planned = False
        self.superadmin.says('!scramble')
        self.assertEqual(['Teams will be scrambled at next round start'], self.superadmin.message_history)
        self.assertTrue(self.p._scrambling_planned)