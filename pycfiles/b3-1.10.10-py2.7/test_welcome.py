# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: H:\workspaces\workspace-python\big-brother-bot\tests\plugins\test_welcome.py
# Compiled at: 2015-05-20 18:47:18
import os
from textwrap import dedent
from mock import Mock, patch, call
import unittest2 as unittest
from mockito import when
import b3
from b3.plugins.admin import AdminPlugin
from b3.plugins.welcome import WelcomePlugin, F_FIRST, F_NEWB, F_ANNOUNCE_USER, F_ANNOUNCE_FIRST, F_USER, F_CUSTOM_GREETING
from b3.config import CfgConfigParser
from b3.fake import FakeClient
from tests import B3TestCase, logging_disabled
from b3 import __file__ as b3_module__file__
ADMIN_CONFIG_FILE = os.path.normpath(os.path.join(os.path.dirname(b3_module__file__), 'conf/plugin_admin.ini'))
WELCOME_CONFIG_FILE = os.path.normpath(os.path.join(os.path.dirname(b3_module__file__), 'conf/plugin_welcome.ini'))

@unittest.skipUnless(os.path.exists(ADMIN_CONFIG_FILE), reason='cannot get default plugin config file at %s' % ADMIN_CONFIG_FILE)
class Welcome_functional_test(B3TestCase):

    def setUp(self):
        B3TestCase.setUp(self)
        with logging_disabled():
            self.adminPlugin = AdminPlugin(self.console, ADMIN_CONFIG_FILE)
            when(self.console).getPlugin('admin').thenReturn(self.adminPlugin)
            self.adminPlugin.onLoadConfig()
            self.adminPlugin.onStartup()
            self.conf = CfgConfigParser()
            self.p = WelcomePlugin(self.console, self.conf)
            self.joe = FakeClient(self.console, name='Joe', guid='joeguid', groupBits=1, team=b3.TEAM_RED)
            self.mike = FakeClient(self.console, name='Mike', guid='mikeguid', groupBits=1, team=b3.TEAM_RED)
            self.bill = FakeClient(self.console, name='Bill', guid='billguid', groupBits=1, team=b3.TEAM_RED)
            self.superadmin = FakeClient(self.console, name='SuperAdmin', guid='superadminguid', groupBits=128, team=b3.TEAM_RED)

    def load_config(self, config_content=None):
        """
        load the given config content, or the default config if config_content is None.
        """
        if config_content is None:
            if not os.path.exists(WELCOME_CONFIG_FILE):
                self.skipTest('cannot get default plugin config file at %s' % WELCOME_CONFIG_FILE)
            else:
                self.conf.load(WELCOME_CONFIG_FILE)
        else:
            self.conf.loadFromString(config_content)
        self.p.onLoadConfig()
        self.p.onStartup()
        return


@unittest.skipUnless(os.path.exists(WELCOME_CONFIG_FILE), reason='cannot get default plugin config file at %s' % WELCOME_CONFIG_FILE)
class Test_default_config(Welcome_functional_test):

    def setUp(self):
        Welcome_functional_test.setUp(self)
        self.load_config()

    def test_settings_flags(self):
        self.assertEqual(63, self.p._welcomeFlags)

    def test_settings_newb_connections(self):
        self.assertEqual(15, self.p._newbConnections)

    def test_settings_delay(self):
        self.assertEqual(30, self.p._welcomeDelay)

    def test_settings_min_gap(self):
        self.assertEqual(3600, self.p._min_gap)

    def test_messages_user(self):
        self.assertEqual("^7[^2Authed^7] Welcome back $name ^7[^3@$id^7], last visit ^3$lastVisit^7, you're a ^2$group^7, played $connections times", self.conf.get('messages', 'user'))

    def test_messages_newb(self):
        self.assertEqual('^7[^2Authed^7] Welcome back $name ^7[^3@$id^7], last visit ^3$lastVisit. Type !register in chat to register. Type !help for help', self.conf.get('messages', 'newb'))

    def test_messages_announce_user(self):
        self.assertEqual('^7Everyone welcome back $name^7, player number ^3#$id^7, to the server, played $connections times', self.conf.get('messages', 'announce_user'))

    def test_messages_first(self):
        self.assertEqual('^7Welcome $name^7, this must be your first visit, you are player ^3#$id. Type !help for help', self.conf.get('messages', 'first'))

    def test_messages_announce_first(self):
        self.assertEqual('^7Everyone welcome $name^7, player number ^3#$id^7, to the server', self.conf.get('messages', 'announce_first'))

    def test_messages_greeting(self):
        self.assertEqual('^7$name^7 joined: $greeting', self.conf.get('messages', 'greeting'))

    def test_messages_greeting_empty(self):
        self.assertEqual('^7You have no greeting set', self.conf.get('messages', 'greeting_empty'))

    def test_messages_greeting_yours(self):
        self.assertEqual('^7Your greeting is %s', self.conf.get('messages', 'greeting_yours'))

    def test_messages_greeting_bad(self):
        self.assertEqual('^7Greeting is not formatted properly: %s', self.conf.get('messages', 'greeting_bad'))

    def test_messages_greeting_changed(self):
        self.assertEqual('^7Greeting changed to: %s', self.conf.get('messages', 'greeting_changed'))

    def test_messages_greeting_cleared(self):
        self.assertEqual('^7Greeting cleared', self.conf.get('messages', 'greeting_cleared'))


class Test_config_flags(Welcome_functional_test):

    def test_flags_nominal(self):
        self.load_config(dedent('\n            [settings]\n            flags: 34\n        '))
        self.assertEqual(34, self.p._welcomeFlags)

    def test_flags_empty(self):
        self.load_config(dedent('\n            [settings]\n            flags: \n        '))
        self.assertEqual(63, self.p._welcomeFlags)

    def test_flags_junk(self):
        self.load_config(dedent('\n            [settings]\n            flags: f00\n        '))
        self.assertEqual(63, self.p._welcomeFlags)

    def test_settings_no_flags(self):
        self.load_config(dedent('\n            [settings]\n        '))
        self.assertEqual(63, self.p._welcomeFlags)

    def test_welcome_first(self):
        self.p._welcomeFlags = 0
        self.load_config(dedent('\n            [settings]\n            welcome_first: yes\n        '))
        self.assertTrue(F_FIRST & self.p._welcomeFlags)
        self.load_config(dedent('\n            [settings]\n            welcome_first: no\n        '))
        self.assertFalse(F_FIRST & self.p._welcomeFlags)

    def test_welcome_newb(self):
        self.p._welcomeFlags = 0
        self.load_config(dedent('\n            [settings]\n            welcome_newb: yes\n        '))
        self.assertTrue(F_NEWB & self.p._welcomeFlags)
        self.load_config(dedent('\n            [settings]\n            welcome_newb: no\n        '))
        self.assertFalse(F_NEWB & self.p._welcomeFlags)

    def test_welcome_user(self):
        self.p._welcomeFlags = 0
        self.load_config(dedent('\n            [settings]\n            welcome_user: yes\n        '))
        self.assertTrue(F_USER & self.p._welcomeFlags)
        self.load_config(dedent('\n            [settings]\n            welcome_user: no\n        '))
        self.assertFalse(F_USER & self.p._welcomeFlags)

    def test_announce_first(self):
        self.p._welcomeFlags = 0
        self.load_config(dedent('\n            [settings]\n            announce_first: yes\n        '))
        self.assertTrue(F_ANNOUNCE_FIRST & self.p._welcomeFlags)
        self.load_config(dedent('\n            [settings]\n            announce_first: no\n        '))
        self.assertFalse(F_ANNOUNCE_FIRST & self.p._welcomeFlags)

    def test_announce_user(self):
        self.p._welcomeFlags = 0
        self.load_config(dedent('\n            [settings]\n            announce_user: yes\n        '))
        self.assertTrue(F_ANNOUNCE_USER & self.p._welcomeFlags)
        self.load_config(dedent('\n            [settings]\n            announce_user: no\n        '))
        self.assertFalse(F_ANNOUNCE_USER & self.p._welcomeFlags)

    def test_show_user_greeting(self):
        self.p._welcomeFlags = 0
        self.load_config(dedent('\n            [settings]\n            show_user_greeting: yes\n        '))
        self.assertTrue(F_CUSTOM_GREETING & self.p._welcomeFlags)
        self.load_config(dedent('\n            [settings]\n            show_user_greeting: no\n        '))
        self.assertFalse(F_CUSTOM_GREETING & self.p._welcomeFlags)

    def test_nonce_set(self):
        self.p._welcomeFlags = 0
        self.load_config(dedent('\n            [settings]\n            welcome_first: no\n            welcome_newb: no\n            welcome_user: no\n            announce_first: no\n            announce_user: no\n            show_user_greeting: no\n        '))
        self.assertEqual(0, self.p._welcomeFlags)

    def test_all_set(self):
        self.p._welcomeFlags = 0
        self.load_config(dedent('\n            [settings]\n            welcome_first: yes\n            welcome_newb: yes\n            welcome_user: yes\n            announce_first: yes\n            announce_user: yes\n            show_user_greeting: yes\n        '))
        self.assertEqual(F_FIRST | F_NEWB | F_USER | F_ANNOUNCE_FIRST | F_ANNOUNCE_USER | F_CUSTOM_GREETING, self.p._welcomeFlags)

    def test_partly_set(self):
        self.p._welcomeFlags = 0
        self.load_config(dedent('\n            [settings]\n            welcome_first: yes\n            welcome_newb: no\n            welcome_user: yes\n            announce_first: yes\n            announce_user: no\n            show_user_greeting: yes\n        '))
        self.assertEqual(F_FIRST | F_USER | F_ANNOUNCE_FIRST | F_CUSTOM_GREETING, self.p._welcomeFlags)

    def test_mix_old_style_and_new_style(self):
        """
        Old style config uses settings/flags.
        New style uses welcome_first, welcome_newb, etc.
        When both styles are found, ignore old style.
        Also a missing new style option is assumed to be 'yes'
        """
        self.p._welcomeFlags = 0
        self.load_config(dedent('\n            [settings]\n            flags: 54\n            ; welcome_first: no\n            welcome_newb: no\n            welcome_user: no\n            announce_first: no\n            announce_user: yes\n            show_user_greeting: no\n        '))
        self.assertEqual(F_FIRST | F_ANNOUNCE_USER, self.p._welcomeFlags)


class Test_config(Welcome_functional_test):

    def test_settings_newb_connections(self):
        self.load_config(dedent('\n            [settings]\n            newb_connections: 27\n        '))
        self.assertEqual(27, self.p._newbConnections)
        self.load_config(dedent('\n            [settings]\n            newb_connections: \n        '))
        self.assertEqual(15, self.p._newbConnections)
        self.load_config(dedent('\n            [settings]\n            newb_connections: f00\n        '))
        self.assertEqual(15, self.p._newbConnections)

    def test_settings_delay(self):
        self.load_config(dedent('\n            [settings]\n            delay: 15\n        '))
        self.assertEqual(15, self.p._welcomeDelay)
        self.load_config(dedent('\n            [settings]\n            delay: \n        '))
        self.assertEqual(30, self.p._welcomeDelay)
        self.load_config(dedent('\n            [settings]\n            delay: f00\n        '))
        self.assertEqual(30, self.p._welcomeDelay)
        self.load_config(dedent('\n            [settings]\n            delay: 5\n        '))
        self.assertEqual(30, self.p._welcomeDelay)
        self.load_config(dedent('\n            [settings]\n            delay: 500\n        '))
        self.assertEqual(30, self.p._welcomeDelay)

    def test_settings_min_gap(self):
        self.load_config(dedent('\n            [settings]\n            min_gap: 540\n        '))
        self.assertEqual(540, self.p._min_gap)
        self.load_config(dedent('\n            [settings]\n            min_gap: \n        '))
        self.assertEqual(3600, self.p._min_gap)
        self.load_config(dedent('\n            [settings]\n            min_gap: f00\n        '))
        self.assertEqual(3600, self.p._min_gap)
        self.load_config(dedent('\n            [settings]\n            min_gap: -15\n        '))
        self.assertEqual(0, self.p._min_gap)


class Test_cmd_greeting(Welcome_functional_test):

    def setUp(self):
        Welcome_functional_test.setUp(self)
        self.load_config()
        self.p.onEvent = lambda *args, **kwargs: None
        self.superadmin.connects('0')
        self.superadmin._connections = 3

    def test_no_parameter(self):
        self.superadmin.greeting = ''
        self.superadmin.clearMessageHistory()
        self.superadmin.says('!greeting')
        self.assertListEqual(['You have no greeting set'], self.superadmin.message_history)
        self.superadmin.greeting = 'hi f00'
        self.superadmin.clearMessageHistory()
        self.superadmin.says('!greeting')
        self.assertListEqual(['Your greeting is hi f00'], self.superadmin.message_history)

    def test_set_new_greeting_none(self):
        self.superadmin.greeting = 'f00'
        self.superadmin.says('!greeting none')
        self.assertListEqual(['Greeting cleared'], self.superadmin.message_history)
        self.assertEqual('', self.superadmin.greeting)

    def test_set_new_greeting_nominal(self):
        self.superadmin.greeting = ''
        self.superadmin.says('!greeting f00')
        self.assertListEqual(['Greeting Test: f00', 'Greeting changed to: f00'], self.superadmin.message_history)
        self.assertEqual('f00', self.superadmin.greeting)

    def test_set_new_greeting_too_long(self):
        self.superadmin.greeting = 'f00'
        self.superadmin.says('!greeting %s' % ('x' * 256))
        self.assertListEqual(['Your greeting is too long'], self.superadmin.message_history)
        self.assertEqual('f00', self.superadmin.greeting)

    def test_set_new_greeting_with_placeholder_name(self):
        self.superadmin.greeting = 'f00'
        self.superadmin.says('!greeting |$name|')
        self.assertListEqual(['Greeting Test: |SuperAdmin|', 'Greeting changed to: |$name|'], self.superadmin.message_history)
        self.assertEqual('|%(name)s|', self.superadmin.greeting)

    def test_set_new_greeting_with_placeholder_greeting(self):
        """
        make sure that '$greeting' cannot be taken as a placeholder or we would allow recursive greeting.
        """
        self.superadmin.greeting = 'f00'
        self.superadmin.says('!greeting |$greeting|')
        self.assertListEqual(['Greeting Test: |$greeting|', 'Greeting changed to: |$greeting|'], self.superadmin.message_history)
        self.assertEqual('|$greeting|', self.superadmin.greeting)

    def test_set_new_greeting_with_placeholder_maxLevel(self):
        self.superadmin.greeting = 'f00'
        self.superadmin.says('!greeting |$maxLevel|')
        self.assertListEqual(['Greeting Test: |100|', 'Greeting changed to: |$maxLevel|'], self.superadmin.message_history)
        self.assertEqual('|%(maxLevel)s|', self.superadmin.greeting)

    def test_set_new_greeting_with_placeholder_group(self):
        self.superadmin.greeting = 'f00'
        self.superadmin.says('!greeting |$group|')
        self.assertListEqual(['Greeting Test: |Super Admin|', 'Greeting changed to: |$group|'], self.superadmin.message_history)
        self.assertEqual('|%(group)s|', self.superadmin.greeting)

    def test_set_new_greeting_with_placeholder_connections(self):
        self.superadmin.greeting = 'f00'
        self.superadmin.says('!greeting |$connections|')
        self.assertListEqual(['Greeting Test: |3|', 'Greeting changed to: |$connections|'], self.superadmin.message_history)
        self.assertEqual('|%(connections)s|', self.superadmin.greeting)


class Test_welcome(Welcome_functional_test):

    def setUp(self):
        Welcome_functional_test.setUp(self)
        self.load_config()
        self.p.onEvent = lambda *args, **kwargs: None
        self.client = FakeClient(console=self.console, name='Jack', guid='JackGUID')
        self.client._connections = 0
        self.client.greeting = 'hi everyone :)'
        self.client.connects('0')
        self.superadmin.connects('1')
        self.say_patcher = patch.object(self.console, 'say')
        self.say_mock = self.say_patcher.start()

    def tearDown(self):
        Welcome_functional_test.tearDown(self)
        self.say_patcher.stop()

    def Test_get_client_info(self):
        self.parser_conf.add_section('b3')
        self.parser_conf.set('b3', 'time_zone', 'CET')
        self.parser_conf.set('b3', 'time_format', '%I:%M%p %Z %m/%d/%y')
        self.assertDictEqual({'connections': '1', 'group': 'Super Admin', 
           'id': '2', 
           'lastVisit': 'Unknown', 
           'level': '100', 
           'name': 'SuperAdmin^7'}, self.p.get_client_info(self.superadmin))
        self.superadmin.lastVisit = 1364821993
        self.superadmin._connections = 2
        self.assertDictEqual({'connections': '2', 'group': 'Super Admin', 
           'id': '2', 
           'lastVisit': '02:13PM CET 04/01/13', 
           'level': '100', 
           'name': 'SuperAdmin^7'}, self.p.get_client_info(self.superadmin))
        self.superadmin.says('!mask mod')
        self.assertDictEqual({'connections': '2', 'group': 'Moderator', 
           'id': '2', 
           'lastVisit': '02:13PM CET 04/01/13', 
           'level': '20', 
           'name': 'SuperAdmin^7'}, self.p.get_client_info(self.superadmin))

    def test_0(self):
        self.p._welcomeFlags = 0
        self.p.welcome(self.superadmin)
        self.assertListEqual([], self.say_mock.mock_calls)
        self.assertListEqual([], self.superadmin.message_history)

    def test_first(self):
        self.client._connections = 0
        self.p._welcomeFlags = F_FIRST
        self.p.welcome(self.client)
        self.assertListEqual([], self.say_mock.mock_calls)
        self.assertListEqual(['Welcome Jack, this must be your first visit, you are player #1. Type !help for help'], self.client.message_history)

    def test_newb(self):
        self.client._connections = 2
        self.p._welcomeFlags = F_NEWB
        self.p.welcome(self.client)
        self.assertListEqual([], self.say_mock.mock_calls)
        self.assertListEqual(['[Authed] Welcome back Jack [@1], last visit Unknown. Type !register in chat to register. Type !help for help'], self.client.message_history)

    def test_user(self):
        self.client._connections = 2
        self.p._welcomeFlags = F_USER
        self.client.says('!register')
        self.client.clearMessageHistory()
        self.p.welcome(self.client)
        self.assertListEqual([call('^7Jack^7 ^7put in group User')], self.say_mock.mock_calls)
        self.assertListEqual(["[Authed] Welcome back Jack [@1], last visit Unknown, you're a User, played 2 times"], self.client.message_history)

    def test_announce_first(self):
        self.client._connections = 0
        self.p._welcomeFlags = F_ANNOUNCE_FIRST
        self.p.welcome(self.client)
        self.assertListEqual([call('^7Everyone welcome Jack^7^7, player number ^3#1^7, to the server')], self.say_mock.mock_calls)
        self.assertListEqual([], self.client.message_history)

    def test_announce_user(self):
        self.client._connections = 2
        self.p._welcomeFlags = F_ANNOUNCE_USER
        self.client.says('!register')
        self.client.clearMessageHistory()
        self.p.welcome(self.client)
        self.assertListEqual([call('^7Jack^7 ^7put in group User'),
         call('^7Everyone welcome back Jack^7^7, player number ^3#1^7, to the server, played 2 times')], self.say_mock.mock_calls)
        self.assertListEqual([], self.client.message_history)

    def test_custom_greeting(self):
        self.client._connections = 2
        self.p._welcomeFlags = F_CUSTOM_GREETING
        self.client.says('!register')
        self.client.clearMessageHistory()
        self.p.welcome(self.client)
        self.assertListEqual([call('^7Jack^7 ^7put in group User'), call('^7Jack^7^7 joined: hi everyone :)')], self.say_mock.mock_calls)
        self.assertListEqual([], self.client.message_history)