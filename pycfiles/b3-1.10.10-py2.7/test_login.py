# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: H:\workspaces\workspace-python\big-brother-bot\tests\plugins\test_login.py
# Compiled at: 2015-02-24 17:29:43
import logging, os
from textwrap import dedent
from mockito import when
from b3.fake import FakeClient
from b3.plugins.admin import AdminPlugin
from tests import B3TestCase
import unittest2 as unittest
from b3.plugins.login import LoginPlugin
from b3.config import CfgConfigParser
from b3 import __file__ as b3__file__
default_plugin_file = os.path.normpath(os.path.join(os.path.dirname(b3__file__), 'conf/plugin_login.ini'))
ADMIN_CONFIG_FILE = os.path.normpath(os.path.join(os.path.dirname(b3__file__), 'conf/plugin_admin.ini'))
F00_MD5 = '9f06f2538cdbb40bce9973f60506de09'

class LoginTestCase(B3TestCase):
    """ Ease testcases that need an working B3 console and need to control the censor plugin config """

    def setUp(self):
        self.log = logging.getLogger('output')
        self.log.propagate = False
        B3TestCase.setUp(self)
        admin_conf = CfgConfigParser()
        admin_conf.load(ADMIN_CONFIG_FILE)
        self.adminPlugin = AdminPlugin(self.console, admin_conf)
        when(self.console).getPlugin('admin').thenReturn(self.adminPlugin)
        self.adminPlugin.onLoadConfig()
        self.adminPlugin.onStartup()
        self.console.gameName = 'theGame'
        self.console.startup()
        self.log.propagate = True

    def tearDown(self):
        B3TestCase.tearDown(self)

    def init_plugin(self, config_content=None):
        self.conf = CfgConfigParser()
        if config_content:
            self.conf.loadFromString(config_content)
        else:
            self.conf.load(default_plugin_file)
        self.p = LoginPlugin(self.console, self.conf)
        self.log.setLevel(logging.DEBUG)
        self.log.info('============================= Login plugin: loading config ============================')
        self.p.onLoadConfig()
        self.log.info('============================= Login plugin: starting  =================================')
        self.p.onStartup()


@unittest.skipUnless(os.path.exists(default_plugin_file), reason='cannot get default plugin_login.xml config file at %s' % default_plugin_file)
class Test_default_config(LoginTestCase):

    def setUp(self):
        LoginTestCase.setUp(self)
        self.init_plugin()

    def test_thresholdlevel(self):
        self.assertEqual(40, self.p._threshold)

    def test_passwdlevel(self):
        self.assertEqual(40, self.p._passwdlevel)


class Test_load_config(LoginTestCase):

    def test_empty_conf(self):
        self.init_plugin(dedent('\n            [settings]\n        '))
        self.assertEqual(1000, self.p._threshold)
        self.assertEqual(100, self.p._passwdlevel)

    def test_thresholdlevel_empty(self):
        self.init_plugin(dedent('\n            [settings]\n            thresholdlevel:\n        '))
        self.assertEqual(1000, self.p._threshold)

    def test_thresholdlevel_junk(self):
        self.init_plugin(dedent('\n            [settings]\n            thresholdlevel: f00\n        '))
        self.assertEqual(1000, self.p._threshold)

    def test_passwdlevel_empty(self):
        self.init_plugin(dedent('\n            [settings]\n            passwdlevel:\n        '))
        self.assertEqual(100, self.p._passwdlevel)

    def test_passwdlevel_junk(self):
        self.init_plugin(dedent('\n            [settings]\n            passwdlevel: f00\n        '))
        self.assertEqual(100, self.p._passwdlevel)


class Test_cmd_setpassword(LoginTestCase):

    def setUp(self):
        LoginTestCase.setUp(self)
        self.init_plugin()
        self.joe = FakeClient(self.console, name='Joe', guid='joeguid', groupBits=128)

    def test_no_parameter(self):
        self.joe.connects('0')
        self.joe._groupBits = 128
        self.assertEqual('', self.joe.password)
        joe_db = self.p._get_client_from_db(self.joe.id)
        self.assertEqual('', joe_db.password)
        self.joe.clearMessageHistory()
        self.joe.says('!setpassword')
        self.assertEqual(['Usage: !setpassword <new password> [<client>]'], self.joe.message_history)
        self.assertEqual('', self.joe.password)
        joe_db = self.p._get_client_from_db(self.joe.id)
        self.assertEqual('', joe_db.password)

    def test_nominal(self):
        self.joe.connects('0')
        self.joe._groupBits = 128
        self.assertEqual('', self.joe.password)
        joe_db = self.p._get_client_from_db(self.joe.id)
        self.assertEqual('', joe_db.password)
        self.joe.clearMessageHistory()
        self.joe.says('!setpassword f00')
        self.assertEqual(['Your new password has been saved'], self.joe.message_history)
        self.assertEqual(F00_MD5, self.joe.password)
        joe_db = self.p._get_client_from_db(self.joe.id)
        self.assertEqual(F00_MD5, joe_db.password)

    def test_change_someone_else(self):
        self.joe.connects('0')
        self.joe._groupBits = 128
        jack = FakeClient(self.console, name='Jack', guid='jackguid')
        jack.connects('1')
        self.assertEqual('', jack.password)
        jack_db = self.p._get_client_from_db(jack.id)
        self.assertEqual('', jack_db.password)
        self.joe.clearMessageHistory()
        self.joe.says('!setpassword f00 jack')
        self.assertEqual(['New password for Jack saved'], self.joe.message_history)
        self.assertEqual(F00_MD5, jack.password)
        jack_db = self.p._get_client_from_db(jack.id)
        self.assertEqual(F00_MD5, jack_db.password)

    def test_change_someone_else_not_found(self):
        self.joe.connects('0')
        self.joe._groupBits = 128
        self.joe.clearMessageHistory()
        self.joe.says('!setpassword new_password jack')
        self.assertEqual(['No players found matching jack'], self.joe.message_history)


class Test_auth(LoginTestCase):

    def setUp(self):
        LoginTestCase.setUp(self)
        self.init_plugin()

    def test_low_level(self):
        joe = FakeClient(self.console, name='Joe', guid='joeguid', groupBits=8)
        joe.clearMessageHistory()
        joe.connects('0')
        self.assertEqual([], joe.message_history)
        self.assertEqual(8, joe.groupBits)

    def test_high_level_no_password_set(self):
        joe = FakeClient(self.console, name='Joe', guid='joeguid', groupBits=128)
        joe.clearMessageHistory()
        joe.connects('0')
        self.assertEqual(['You need a password to use all your privileges: ask the administrator to set a password for you'], joe.message_history)
        self.assertEqual(2, joe.groupBits)

    def test_high_level_having_password(self):
        joe = FakeClient(self.console, name='Joe', guid='joeguid', groupBits=128, password=F00_MD5)
        joe.save()
        joe.clearMessageHistory()
        joe.connects('0')
        self.assertEqual(['Login via console: /tell 0 !login yourpassword'], joe.message_history)
        self.assertEqual(2, joe.groupBits)


class Test_cmd_login(LoginTestCase):

    def setUp(self):
        LoginTestCase.setUp(self)
        self.init_plugin()
        self.jack = FakeClient(self.console, name='Jack', guid='jackguid', groupBits=128, password=F00_MD5)
        self.jack.save()

    def test_already_logged_in(self):
        joe = FakeClient(self.console, name='Joe', guid='joeguid', groupBits=128)
        joe.setvar(self.p, 'loggedin', 1)
        joe.connects('0')
        joe.clearMessageHistory()
        joe.says('!login')
        self.assertEqual(['You are already logged in'], joe.message_history)

    def test_low_level(self):
        joe = FakeClient(self.console, name='Joe', guid='joeguid', groupBits=8)
        joe.connects('0')
        joe.clearMessageHistory()
        joe.says('!login')
        self.assertEqual(['You do not need to log in'], joe.message_history)
        self.assertFalse(self.jack.isvar(self.p, 'loggedin'))

    def test_high_level_no_parameter(self):
        self.jack.connects('0')
        self.assertEqual(2, self.jack.groupBits)
        self.jack.clearMessageHistory()
        self.jack.says('!login')
        self.assertEqual(['Usage (via console): /tell 0 !login yourpassword'], self.jack.message_history)
        self.assertEqual(2, self.jack.groupBits)
        self.assertFalse(self.jack.isvar(self.p, 'loggedin'))

    def test_high_level_wrong_password(self):
        self.jack.connects('0')
        self.assertEqual(2, self.jack.groupBits)
        self.jack.clearMessageHistory()
        self.jack.says('!login qsfddqsf')
        self.assertEqual(['***Access denied***'], self.jack.message_history)
        self.assertEqual(2, self.jack.groupBits)
        self.assertFalse(self.jack.isvar(self.p, 'loggedin'))

    def test_high_level_correct_password(self):
        self.jack.connects('0')
        self.assertEqual(2, self.jack.groupBits)
        self.jack.clearMessageHistory()
        self.jack.says('!login f00')
        self.assertEqual(['You are successfully logged in'], self.jack.message_history)
        self.assertEqual(128, self.jack.groupBits)
        self.assertTrue(self.jack.isvar(self.p, 'loggedin'))

    def test_high_level_spoofed_password_with_compromised_client_object(self):
        """
        in some B3 game parser implementation there is an issue which could let the 'password' property of client
        objects be compromised.
        """
        batman_md5 = 'ec0e2603172c73a8b644bb9456c1ff6e'
        self.jack.connects('0')
        self.assertEqual(2, self.jack.groupBits)
        self.jack.password = batman_md5
        self.jack.clearMessageHistory()
        self.jack.says('!login batman')
        self.assertEqual(['***Access denied***'], self.jack.message_history)
        self.assertEqual(2, self.jack.groupBits)
        self.assertFalse(self.jack.isvar(self.p, 'loggedin'))

    def test_high_level_correct_password_with_compromised_client_object(self):
        """
        in some B3 game parser implementation there is an issue which could let the 'password' property of client
        objects be compromised.
        """
        batman_md5 = 'ec0e2603172c73a8b644bb9456c1ff6e'
        self.jack.connects('0')
        self.assertEqual(2, self.jack.groupBits)
        self.jack.password = batman_md5
        self.jack.clearMessageHistory()
        self.jack.says('!login f00')
        self.assertEqual(['You are successfully logged in'], self.jack.message_history)
        self.assertEqual(128, self.jack.groupBits)
        self.assertTrue(self.jack.isvar(self.p, 'loggedin'))