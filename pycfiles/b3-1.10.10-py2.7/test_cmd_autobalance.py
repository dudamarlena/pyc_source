# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\tests\plugins\poweradminbf3\test_cmd_autobalance.py
# Compiled at: 2016-03-08 18:42:10
from mock import Mock, patch
from b3.config import CfgConfigParser
from b3.plugins.poweradminbf3 import Poweradminbf3Plugin
from tests.plugins.poweradminbf3 import Bf3TestCase

class Test_cmd_autobalance(Bf3TestCase):

    def setUp(self):
        super(Test_cmd_autobalance, self).setUp()
        self.conf = CfgConfigParser()
        self.conf.loadFromString('\n[commands]\nautobalance: mod\n')
        self.p = Poweradminbf3Plugin(self.console, self.conf)
        self.p.onLoadConfig()
        self.p.onStartup()
        self.p.console._cron = Mock()

    def test_no_argument_while_off(self):
        self.p._autobalance = False
        self.moderator.connects('moderator')
        self.moderator.message_history = []
        self.moderator.says('!autobalance')
        self.assertEqual(1, len(self.moderator.message_history))
        self.assertEqual('Autobalance is currently off, use !autobalance on to turn on', self.moderator.message_history[0])

    def test_no_argument_while_on(self):
        self.p._autobalance = True
        self.moderator.connects('moderator')
        self.moderator.message_history = []
        self.moderator.says('!autobalance')
        self.assertEqual(1, len(self.moderator.message_history))
        self.assertEqual('Autobalance is currently on, use !autobalance off to turn off', self.moderator.message_history[0])

    def test_with_argument_foo(self):
        self.moderator.connects('moderator')
        self.moderator.message_history = []
        self.moderator.says('!autobalance foo')
        self.assertIn('invalid data. Expecting on, off or now', self.moderator.message_history)

    def test_with_argument_now(self):
        self.p.run_autobalance = Mock()
        self.moderator.connects('moderator')
        self.moderator.message_history = []
        self.moderator.says('!autobalance now')
        self.assertTrue(self.p.run_autobalance.called)

    def test_with_argument_on_while_currently_off_and_autoassign_off(self):
        self.p._autobalance = False
        self.p._autoassign = False
        self.p._one_round_over = False
        self.moderator.connects('moderator')
        self.moderator.message_history = []
        self.moderator.says('!autobalance on')
        self.assertIn('Autobalance will be enabled on next round start', self.moderator.message_history)
        self.assertIn('Autoassign now enabled', self.moderator.message_history)
        self.assertTrue(self.p._autobalance)
        self.assertTrue(self.p._autoassign)

    @patch('b3.cron.Cron')
    def test_with_argument_on_while_currently_off_and_one_round_is_over(self, MockCron):
        self.p._autobalance = False
        self.p._one_round_over = True
        self.p._cronTab_autobalance = None
        self.p.console._cron.__add__ = Mock()
        self.moderator.connects('moderator')
        self.moderator.message_history = []
        self.moderator.says('!autobalance on')
        self.assertIn('Autobalance now enabled', self.moderator.message_history)
        self.assertTrue(self.p._autobalance)
        self.assertIsNotNone(self.p._cronTab_autobalance)
        self.console.cron.__add__.assert_called_once_with(self.p._cronTab_autobalance)
        return

    @patch('b3.cron.Cron')
    def test_with_argument_on_while_currently_off_and_no_round_is_over(self, MockCron):
        self.p._autobalance = False
        self.p._one_round_over = False
        self.p._cronTab_autobalance = None
        self.p.console._cron.__add__ = Mock()
        self.moderator.connects('moderator')
        self.moderator.message_history = []
        self.moderator.says('!autobalance on')
        self.assertIn('Autobalance will be enabled on next round start', self.moderator.message_history)
        self.assertTrue(self.p._autobalance)
        self.assertIsNone(self.p._cronTab_autobalance)
        self.assertFalse(self.p.console.cron.__add__.called)
        return

    def test_with_argument_on_while_already_on(self):
        self.p._autobalance = True
        self.moderator.connects('moderator')
        self.moderator.message_history = []
        self.moderator.says('!autobalance on')
        self.assertEqual(['Autobalance is already enabled'], self.moderator.message_history)
        self.assertTrue(self.p._autobalance)

    @patch('b3.cron.Cron')
    def test_with_argument_off_while_currently_on(self, MockCron):
        self.p._autobalance = True
        self.p.console._cron.__sub__ = Mock()
        self.p._cronTab_autobalance = Mock()
        self.moderator.connects('moderator')
        self.moderator.message_history = []
        self.moderator.says('!autobalance off')
        self.assertEqual(['Autobalance now disabled'], self.moderator.message_history)
        self.assertFalse(self.p._autobalance)
        self.p.console.cron.__sub__.assert_called_once_with(self.p._cronTab_autobalance)

    def test_with_argument_off_while_already_off(self):
        self.p._autobalance = False
        self.moderator.connects('moderator')
        self.moderator.message_history = []
        self.moderator.says('!autobalance off')
        self.assertEqual(['Autobalance now disabled'], self.moderator.message_history)
        self.assertFalse(self.p._autobalance)