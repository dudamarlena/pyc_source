# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: H:\workspaces\workspace-python\big-brother-bot\tests\plugins\test_spamcontrol.py
# Compiled at: 2015-03-18 18:55:42
import logging, new, os
from textwrap import dedent
from mockito import when
from mock import Mock, patch
import unittest2 as unittest
from b3.events import Event
from b3.fake import FakeClient
from b3.plugins.admin import AdminPlugin
from b3.plugins.spamcontrol import SpamcontrolPlugin
from tests import B3TestCase
from b3 import __file__ as b3_module__file__
from b3.config import CfgConfigParser
ADMIN_CONFIG_FILE = os.path.normpath(os.path.join(os.path.dirname(b3_module__file__), 'conf/plugin_admin.ini'))
SPAMCONTROM_CONFIG_FILE = os.path.normpath(os.path.join(os.path.dirname(b3_module__file__), 'conf/plugin_spamcontrol.ini'))

class SpamcontrolTestCase(B3TestCase):
    """ Ease testcases that need an working B3 console and need to control the Spamcontrol plugin config """

    def setUp(self):
        self.timer_patcher = patch('threading.Timer')
        self.timer_patcher.start()
        self.log = logging.getLogger('output')
        self.log.propagate = False
        B3TestCase.setUp(self)
        self.console.startup()
        self.log.propagate = True

    def tearDown(self):
        B3TestCase.tearDown(self)
        self.timer_patcher.stop()

    def init_plugin(self, config_content):
        self.conf = CfgConfigParser()
        self.conf.loadFromString(config_content)
        self.p = SpamcontrolPlugin(self.console, self.conf)
        self.log.setLevel(logging.DEBUG)
        self.log.info('============================= Spamcontrol plugin: loading config ============================')
        self.p.onLoadConfig()
        self.log.info('============================= Spamcontrol plugin: starting  =================================')
        self.p.onStartup()


class Test_config(SpamcontrolTestCase):
    """ test different config are correctly loaded """
    default_max_spamins = 10
    default_mod_level = 20
    default_falloff_rate = 6.5

    @unittest.skipUnless(os.path.exists(SPAMCONTROM_CONFIG_FILE), reason='cannot get default plugin config file at %s' % SPAMCONTROM_CONFIG_FILE)
    def test_default_conf(self):
        with open(SPAMCONTROM_CONFIG_FILE) as (default_conf):
            self.init_plugin(default_conf.read())
        self.assertEqual(self.default_max_spamins, self.p._maxSpamins)
        self.assertEqual(self.default_mod_level, self.p._modLevel)
        self.assertEqual(self.default_falloff_rate, self.p._falloffRate)

    def test_emtpy_conf(self):
        self.init_plugin('\n        ')
        self.assertEqual(self.default_max_spamins, self.p._maxSpamins)
        self.assertEqual(self.default_mod_level, self.p._modLevel)
        self.assertEqual(self.default_falloff_rate, self.p._falloffRate)

    def test_max_spamins_empty(self):
        self.init_plugin(dedent('\n            [settings]\n            max_spamins:\n        '))
        self.assertEqual(self.default_max_spamins, self.p._maxSpamins)

    def test_max_spamins_NaN(self):
        self.init_plugin(dedent('\n            [settings]\n            max_spamins: fo0\n        '))
        self.assertEqual(self.default_max_spamins, self.p._maxSpamins)

    def test_max_spamins_negative(self):
        self.init_plugin(dedent('\n            [settings]\n            max_spamins: -15\n        '))
        self.assertEqual(0, self.p._maxSpamins)

    def test_mod_level_empty(self):
        self.init_plugin(dedent('\n            [settings]\n            mod_level:\n        '))
        self.assertEqual(0, self.p._modLevel)

    def test_mod_level_NaN(self):
        self.init_plugin(dedent('\n            [settings]\n            mod_level: fo0\n        '))
        self.assertEqual(self.default_mod_level, self.p._modLevel)

    def test_mod_level_nominal(self):
        self.init_plugin(dedent('\n            [settings]\n            mod_level: 60\n        '))
        self.assertEqual(60, self.p._modLevel)

    def test_mod_level_by_group_keyword(self):
        self.init_plugin(dedent('\n            [settings]\n            mod_level: senioradmin\n        '))
        self.assertEqual(80, self.p._modLevel)


@unittest.skipUnless(os.path.exists(SPAMCONTROM_CONFIG_FILE), reason='cannot get default plugin config file at %s' % SPAMCONTROM_CONFIG_FILE)
class Test_plugin(SpamcontrolTestCase):

    def setUp(self):
        SpamcontrolTestCase.setUp(self)
        self.adminPlugin = AdminPlugin(self.console, ADMIN_CONFIG_FILE)
        when(self.console).getPlugin('admin').thenReturn(self.adminPlugin)
        self.adminPlugin.onLoadConfig()
        self.adminPlugin.onStartup()
        with open(SPAMCONTROM_CONFIG_FILE) as (default_conf):
            self.init_plugin(default_conf.read())
        self.joe = FakeClient(self.console, name='Joe', guid='zaerezarezar', groupBits=1)
        self.joe.connects('1')
        self.superadmin = FakeClient(self.console, name='Superadmin', guid='superadmin_guid', groupBits=128)
        self.superadmin.connects('2')

    def assertSpaminsPoints(self, client, points):
        actual = client.var(self.p, 'spamins', 0).value
        self.assertEqual(points, actual, 'expecting %s to have %s spamins points' % (client.name, points))

    def test_say(self):
        when(self.p).getTime().thenReturn(0).thenReturn(1).thenReturn(20).thenReturn(120)
        self.assertSpaminsPoints(self.joe, 0)
        self.joe.says('doh')
        self.assertSpaminsPoints(self.joe, 2)
        self.joe.says('foo')
        self.assertSpaminsPoints(self.joe, 4)
        self.joe.says('bar')
        self.assertSpaminsPoints(self.joe, 3)
        self.joe.says('hi')
        self.assertSpaminsPoints(self.joe, 0)

    def test_cmd_spamins(self):
        when(self.p).getTime().thenReturn(0).thenReturn(3).thenReturn(4).thenReturn(4).thenReturn(500)
        self.joe.says('doh')
        self.joe.says('doh')
        self.joe.says('doh')
        self.superadmin.clearMessageHistory()
        self.superadmin.says('!spamins joe')
        self.assertListEqual(['Joe currently has 9 spamins, peak was 9'], self.superadmin.message_history)
        self.superadmin.clearMessageHistory()
        self.superadmin.says('!spamins joe')
        self.assertListEqual(['Joe currently has 0 spamins, peak was 9'], self.superadmin.message_history)

    def test_cmd_spamins_lowercase(self):
        mike = FakeClient(self.console, name='Mike')
        mike.connects('3')
        self.superadmin.clearMessageHistory()
        self.superadmin.says('!spamins mike')
        self.assertListEqual(['Mike currently has 0 spamins, peak was 0'], self.superadmin.message_history)

    def test_cmd_spamins_uppercase(self):
        mike = FakeClient(self.console, name='Mike')
        mike.connects('3')
        self.superadmin.clearMessageHistory()
        self.superadmin.says('!spamins MIKE')
        self.assertListEqual(['Mike currently has 0 spamins, peak was 0'], self.superadmin.message_history)

    def test_cmd_spamins_unknown_player(self):
        self.superadmin.clearMessageHistory()
        self.superadmin.says('!spamins nobody')
        self.assertListEqual(['No players found matching nobody'], self.superadmin.message_history)

    def test_cmd_spamins_no_argument(self):
        self.console.getPlugin('admin')._warn_command_abusers = True
        self.joe.clearMessageHistory()
        self.joe.says('!spamins')
        self.assertListEqual(['You need to be in group Moderator to use !spamins'], self.joe.message_history)
        self.superadmin.says('!putgroup joe mod')
        self.joe.clearMessageHistory()
        self.joe.says('!spamins')
        self.assertListEqual(['Joe is too cool to spam'], self.joe.message_history)

    def test_joe_gets_warned(self):
        when(self.p).getTime().thenReturn(0)
        self.joe.warn = Mock()
        self.joe.says('doh 1')
        self.joe.says('doh 2')
        self.joe.says('doh 3')
        self.joe.says('doh 4')
        self.joe.says('doh 5')
        self.assertEqual(1, self.joe.warn.call_count)


class Test_game_specific_spam(SpamcontrolTestCase):

    def setUp(self):
        SpamcontrolTestCase.setUp(self)
        with open(SPAMCONTROM_CONFIG_FILE) as (default_conf):
            self.init_plugin(default_conf.read())
        self.joe = FakeClient(self.console, name='Joe', exactName='Joe', guid='zaerezarezar', groupBits=1)
        self.joe.connects('1')
        EVT_CLIENT_RADIO = self.console.Events.createEvent('EVT_CLIENT_RADIO', 'Event client radio')

        def onRadio(this, event):
            new_event = Event(type=event.type, client=event.client, target=event.target, data=event.data['text'])
            this.onChat(new_event)

        self.p.onRadio = new.instancemethod(onRadio, self.p, SpamcontrolPlugin)
        self.p.registerEvent('EVT_CLIENT_RADIO', self.p.onRadio)

        def radios(me, text):
            me.console.queueEvent(Event(type=EVT_CLIENT_RADIO, client=me, data={'text': text}))

        self.joe.radios = new.instancemethod(radios, self.joe, FakeClient)

    def test_radio_spam(self):
        when(self.p).getTime().thenReturn(0)
        self.joe.warn = Mock()
        self.joe.says('doh 1')
        self.joe.radios('doh 2')
        self.joe.says('doh 3')
        self.joe.radios('doh 4')
        self.joe.says('doh 5')
        self.assertEqual(1, self.joe.warn.call_count)