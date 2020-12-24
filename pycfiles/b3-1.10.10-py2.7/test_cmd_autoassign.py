# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\tests\plugins\poweradminbf3\test_cmd_autoassign.py
# Compiled at: 2016-03-08 18:42:10
from tests.plugins.poweradminbf3 import Bf3TestCase
from b3.config import CfgConfigParser
from b3.plugins.poweradminbf3 import Poweradminbf3Plugin

class Test_cmd_autoassign(Bf3TestCase):

    def setUp(self):
        super(Test_cmd_autoassign, self).setUp()
        self.conf = CfgConfigParser()
        self.conf.loadFromString('\n[commands]\nautoassign: mod\n')
        self.p = Poweradminbf3Plugin(self.console, self.conf)
        self.p.onLoadConfig()
        self.p.onStartup()

    def test_no_argument_while_off(self):
        self.p._autoassign = False
        self.moderator.connects('moderator')
        self.moderator.message_history = []
        self.moderator.says('!autoassign')
        self.assertEqual(1, len(self.moderator.message_history))
        self.assertEqual('Autoassign is currently off, use !autoassign on to turn on', self.moderator.message_history[0])

    def test_no_argument_while_on(self):
        self.p._autoassign = True
        self.moderator.connects('moderator')
        self.moderator.message_history = []
        self.moderator.says('!autoassign')
        self.assertEqual(1, len(self.moderator.message_history))
        self.assertEqual('Autoassign is currently on, use !autoassign off to turn off', self.moderator.message_history[0])

    def test_with_argument_foo(self):
        self.moderator.connects('moderator')
        self.moderator.message_history = []
        self.moderator.says('!autoassign foo')
        self.assertIn('invalid data. Expecting on or off', self.moderator.message_history)

    def test_with_argument_on(self):
        self.p._autoassign = False
        self.moderator.connects('moderator')
        self.moderator.message_history = []
        self.moderator.says('!autoassign on')
        self.assertIn('Autoassign now enabled', self.moderator.message_history)
        self.assertTrue(self.p._autoassign)

    def test_with_argument_off_with_autobalance_on(self):
        self.p._autoassign = True
        self.p._autobalance = True
        self.moderator.connects('moderator')
        self.moderator.message_history = []
        self.moderator.says('!autoassign off')
        self.assertIn('Autoassign now disabled', self.moderator.message_history)
        self.assertFalse(self.p._autoassign)
        self.assertIn('Autobalance now disabled', self.moderator.message_history)
        self.assertFalse(self.p._autobalance)

    def test_with_argument_off_with_autobalance_off(self):
        self.p._autoassign = True
        self.p._autobalance = False
        self.moderator.connects('moderator')
        self.moderator.message_history = []
        self.moderator.says('!autoassign off')
        self.assertIn('Autoassign now disabled', self.moderator.message_history)
        self.assertFalse(self.p._autoassign)
        self.assertNotIn('Autobalance now disabled', self.moderator.message_history)
        self.assertFalse(self.p._autobalance)