# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\tests\plugins\welcome\test_config.py
# Compiled at: 2016-03-08 18:42:10
from textwrap import dedent
from b3.plugins.welcome import F_FIRST, F_NEWB, F_ANNOUNCE_USER, F_ANNOUNCE_FIRST, F_USER, F_CUSTOM_GREETING
from tests.plugins.welcome import Welcome_functional_test

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