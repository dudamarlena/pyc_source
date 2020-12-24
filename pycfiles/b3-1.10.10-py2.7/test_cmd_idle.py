# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\tests\plugins\poweradminbf3\test_cmd_idle.py
# Compiled at: 2016-03-08 18:42:10
import logging
from mock import Mock
from mockito import when, verify, unstub
from b3.parsers.frostbite2.protocol import CommandFailedError
from tests.plugins.poweradminbf3 import Bf3TestCase, logging_disabled
from b3.config import CfgConfigParser
from b3.plugins.poweradminbf3 import Poweradminbf3Plugin

class Test_cmd_idle(Bf3TestCase):

    def setUp(self):
        super(Test_cmd_idle, self).setUp()
        self.conf = CfgConfigParser()
        self.conf.loadFromString('[commands]\nidle: 40\n        ')
        with logging_disabled():
            self.p = Poweradminbf3Plugin(self.console, self.conf)
            self.p.onLoadConfig()
            self.p.onStartup()
        self.p.error = Mock(wraps=self.p.error)
        logging.getLogger('output').setLevel(logging.DEBUG)

    def test_no_argument_while_unknown(self):
        when(self.console).write(('vars.idleTimeout', )).thenRaise(CommandFailedError(['foo']))
        self.superadmin.connects('god')
        self.superadmin.message_history = []
        self.superadmin.says('!idle')
        self.assertEqual(['Idle kick is [unknown]'], self.superadmin.message_history)
        self.assertFalse(self.p.error.called)

    def test_no_argument_while_on(self):
        when(self.console).write(('vars.idleTimeout', )).thenReturn(['600'])
        self.superadmin.connects('god')
        self.superadmin.message_history = []
        self.superadmin.says('!idle')
        self.assertEqual(['Idle kick is [10 min]'], self.superadmin.message_history)
        self.assertFalse(self.p.error.called)

    def test_no_argument_while_off(self):
        when(self.console).write(('vars.idleTimeout', )).thenReturn(['0'])
        self.superadmin.connects('god')
        self.superadmin.message_history = []
        self.superadmin.says('!idle')
        self.assertEqual(['Idle kick is [OFF]'], self.superadmin.message_history)
        self.assertFalse(self.p.error.called)

    def test_with_argument_foo(self):
        when(self.console).write(('vars.idleTimeout', )).thenReturn(['0'])
        self.superadmin.connects('god')
        self.superadmin.message_history = []
        self.superadmin.says('!idle f00')
        self.assertEqual(["unexpected value 'f00'. Available modes : on, off or a number of minutes"], self.superadmin.message_history)
        self.assertFalse(self.p.error.called)

    def test_with_argument_on_while_already_on(self):
        self.p._last_idleTimeout = str(1020)
        when(self.console).write(('vars.idleTimeout', )).thenReturn(['600'])
        self.superadmin.connects('god')
        self.superadmin.message_history = []
        self.superadmin.says('!idle on')
        self.assertEqual(['Idle kick is already ON and set to 10 min'], self.superadmin.message_history)
        self.assertFalse(self.p.error.called)

    def test_with_argument_on_while_already_off(self):
        self.p._last_idleTimeout = str(1020)
        when(self.console).write(('vars.idleTimeout', )).thenReturn(['0'])
        self.superadmin.connects('god')
        self.superadmin.message_history = []
        self.assertEqual(str(1020), self.p._last_idleTimeout)
        self.superadmin.says('!idle on')
        verify(self.console).write(('vars.idleTimeout', str(1020)))
        self.assertEqual(['Idle kick is now [17 min]'], self.superadmin.message_history)
        self.assertFalse(self.p.error.called)

    def test_on_off_on_15_on_off(self):
        self.superadmin.connects('god')
        self.assertEqual(300, self.p._last_idleTimeout)
        unstub()
        when(self.console).write(('vars.idleTimeout', )).thenReturn(['0'])
        self.superadmin.message_history = []
        self.superadmin.says('!idle on')
        verify(self.console).write(('vars.idleTimeout', 300))
        self.assertEqual(['Idle kick is now [5 min]'], self.superadmin.message_history)
        self.assertFalse(self.p.error.called)
        self.assertEqual(300, self.p._last_idleTimeout)
        unstub()
        when(self.console).write(('vars.idleTimeout', )).thenReturn(['300'])
        self.superadmin.message_history = []
        self.superadmin.says('!idle off')
        verify(self.console).write(('vars.idleTimeout', 0))
        self.assertEqual(['Idle kick is now [OFF]'], self.superadmin.message_history)
        self.assertFalse(self.p.error.called)
        self.assertEqual('300', self.p._last_idleTimeout)
        unstub()
        when(self.console).write(('vars.idleTimeout', )).thenReturn(['0'])
        self.superadmin.message_history = []
        self.superadmin.says('!idle on')
        verify(self.console).write(('vars.idleTimeout', '300'))
        self.assertEqual(['Idle kick is now [5 min]'], self.superadmin.message_history)
        self.assertFalse(self.p.error.called)
        self.assertEqual('300', self.p._last_idleTimeout)
        unstub()
        when(self.console).write(('vars.idleTimeout', )).thenReturn(['300'])
        self.superadmin.message_history = []
        self.superadmin.says('!idle 15')
        verify(self.console).write(('vars.idleTimeout', 900))
        self.assertEqual(['Idle kick is now [15 min]'], self.superadmin.message_history)
        self.assertFalse(self.p.error.called)
        self.assertEqual('300', self.p._last_idleTimeout)
        unstub()
        when(self.console).write(('vars.idleTimeout', )).thenReturn([str(900)])
        self.superadmin.message_history = []
        self.superadmin.says('!idle on')
        self.assertEqual(['Idle kick is already ON and set to 15 min'], self.superadmin.message_history)
        self.assertFalse(self.p.error.called)
        self.assertEqual('300', self.p._last_idleTimeout)
        unstub()
        when(self.console).write(('vars.idleTimeout', )).thenReturn([str(900)])
        self.superadmin.message_history = []
        self.superadmin.says('!idle off')
        verify(self.console).write(('vars.idleTimeout', 0))
        self.assertEqual(['Idle kick is now [OFF]'], self.superadmin.message_history)
        self.assertFalse(self.p.error.called)
        self.assertEqual(str(900), self.p._last_idleTimeout)