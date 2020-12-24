# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: H:\workspaces\workspace-python\big-brother-bot\tests\plugins\test_cmdmanager.py
# Compiled at: 2015-02-24 17:29:43
import os, unittest2 as unittest
from textwrap import dedent
from mockito import when
from b3.plugins.admin import AdminPlugin
from b3.plugins.cmdmanager import CmdmanagerPlugin
from b3.plugins.cmdmanager import GRANT_SET_ATTR
from b3.config import CfgConfigParser
from b3.fake import FakeClient
from tests import B3TestCase
from b3 import __file__ as b3_module__file__
ADMIN_CONFIG_FILE = os.path.normpath(os.path.join(os.path.dirname(b3_module__file__), 'conf/plugin_admin.ini'))

@unittest.skipUnless(os.path.exists(ADMIN_CONFIG_FILE), reason='cannot get default plugin config file at %s' % ADMIN_CONFIG_FILE)
class Cmdmanager_TestCase(B3TestCase):

    def setUp(self):
        B3TestCase.setUp(self)
        self.console.gameName = 'f00'
        self.adminPlugin = AdminPlugin(self.console, ADMIN_CONFIG_FILE)
        when(self.console).getPlugin('admin').thenReturn(self.adminPlugin)
        self.adminPlugin.onLoadConfig()
        self.adminPlugin.onStartup()
        self.conf = CfgConfigParser()
        self.conf.loadFromString(dedent('\n            [settings]\n            update_config_file: no\n\n            [commands]\n            cmdlevel: fulladmin\n            cmdalias: fulladmin\n            cmdgrant: superadmin\n            cmdrevoke: superadmin\n            cmduse: superadmin\n        '))
        self.p = CmdmanagerPlugin(self.console, self.conf)
        self.p.onLoadConfig()
        self.p.onStartup()

    def assert_cmd_groups(self, cmd_name, groups):
        """
        Assert a command has the given authorized groups set correctly.
        :param cmd_name: str name of a command
        :param groups: str minimum group required to run the command or group range
        """
        cmd = self.adminPlugin._commands[cmd_name]
        self.assertIsNotNone(cmd, 'could not find command %r' % cmd_name)
        self.assertEqual(groups, self.p.get_command_level_string(cmd))

    def assert_cmd_alias(self, cmd_name, alias_name):
        """
        Assert a command has the given alias.
        :param cmd_name: str command name
        :param alias_name: str expected alias name, or None
        """
        cmd = self.adminPlugin._commands[cmd_name]
        self.assertIsNotNone(cmd, 'could not find command %r' % cmd_name)
        self.assertEqual(alias_name if alias_name is not None else '', cmd.alias)
        return


@unittest.skipUnless(os.path.exists(ADMIN_CONFIG_FILE), reason='cannot get default plugin config file at %s' % ADMIN_CONFIG_FILE)
class Test_commands(Cmdmanager_TestCase):

    def test_cmdlevel_no_parameter(self):
        superadmin = FakeClient(self.console, name='superadmin', guid='superadminguid', groupBits=128)
        superadmin.connects('1')
        superadmin.clearMessageHistory()
        superadmin.says('!cmdlevel help')
        self.assertListEqual(['command help level: guest'], superadmin.message_history)

    def test_cmdlevel_no_parameter_no_access(self):
        mike = FakeClient(self.console, name='Mike', guid='mikeguid', groupBits=32)
        mike.connects('1')
        mike.clearMessageHistory()
        mike.says('!cmdlevel die')
        self.assertListEqual(['no sufficient access to die command'], mike.message_history)

    def test_cmdlevel_invalid_command(self):
        superadmin = FakeClient(self.console, name='superadmin', guid='superadminguid', groupBits=128)
        superadmin.connects('1')
        superadmin.clearMessageHistory()
        superadmin.says('!cmdlevel fakecommand')
        self.assertListEqual(['could not find command fakecommand'], superadmin.message_history)

    def test_cmdlevel_single_valid_minlevel(self):
        superadmin = FakeClient(self.console, name='superadmin', guid='superadminguid', groupBits=128)
        superadmin.connects('1')
        superadmin.clearMessageHistory()
        superadmin.says('!cmdlevel help admin')
        self.assertListEqual(['command help level changed: admin'], superadmin.message_history)
        self.assert_cmd_groups('help', '^2admin')

    def test_cmdlevel_single_invalid_minlevel(self):
        superadmin = FakeClient(self.console, name='superadmin', guid='superadminguid', groupBits=128)
        superadmin.connects('1')
        self.assert_cmd_groups('help', '^2guest')
        superadmin.clearMessageHistory()
        superadmin.says('!cmdlevel help fakegroup')
        self.assertListEqual(['invalid level specified: fakegroup'], superadmin.message_history)
        self.assert_cmd_groups('help', '^2guest')

    def test_cmdlevel_double_valid_minlevel_maxlevel(self):
        superadmin = FakeClient(self.console, name='superadmin', guid='superadminguid', groupBits=128)
        superadmin.connects('1')
        self.assert_cmd_groups('help', '^2guest')
        superadmin.clearMessageHistory()
        superadmin.says('!cmdlevel help admin-senioradmin')
        self.assertListEqual(['command help level changed: admin-senioradmin'], superadmin.message_history)
        self.assert_cmd_groups('help', '^2admin^7-^2senioradmin')

    def test_cmdlevel_double_invalid_minlevel_maxlevel(self):
        superadmin = FakeClient(self.console, name='superadmin', guid='superadminguid', groupBits=128)
        superadmin.connects('1')
        self.assert_cmd_groups('help', '^2guest')
        superadmin.clearMessageHistory()
        superadmin.says('!cmdlevel help admin-fakegroup')
        self.assertListEqual(['invalid level specified: fakegroup'], superadmin.message_history)
        self.assert_cmd_groups('help', '^2guest')

    def test_cmdlevel_double_minlevel_greater_than_maxlevel(self):
        superadmin = FakeClient(self.console, name='superadmin', guid='superadminguid', groupBits=128)
        superadmin.connects('1')
        self.assert_cmd_groups('help', '^2guest')
        superadmin.clearMessageHistory()
        superadmin.says('!cmdlevel help fulladmin-admin')
        self.assertListEqual(['invalid level: fulladmin is greater than admin'], superadmin.message_history)
        self.assert_cmd_groups('help', '^2guest')

    def test_cmdalias_invalid_command(self):
        superadmin = FakeClient(self.console, name='superadmin', guid='superadminguid', groupBits=128)
        superadmin.connects('1')
        superadmin.clearMessageHistory()
        superadmin.says('!cmdalias fakecommand')
        self.assertListEqual(['could not find command fakecommand'], superadmin.message_history)

    def test_cmdalias_no_parameter(self):
        superadmin = FakeClient(self.console, name='superadmin', guid='superadminguid', groupBits=128)
        superadmin.connects('1')
        superadmin.clearMessageHistory()
        superadmin.says('!cmdalias help')
        self.assertListEqual(['command help alias: h'], superadmin.message_history)

    def test_cmdalias_no_parameter_no_alias(self):
        superadmin = FakeClient(self.console, name='superadmin', guid='superadminguid', groupBits=128)
        superadmin.connects('1')
        superadmin.clearMessageHistory()
        superadmin.says('!cmdalias register')
        self.assertListEqual(['command register has not alias set'], superadmin.message_history)

    def test_cmdalias_no_parameter_no_access(self):
        mike = FakeClient(self.console, name='Mike', guid='mikeguid', groupBits=32)
        mike.connects('1')
        mike.clearMessageHistory()
        mike.says('!cmdalias die')
        self.assertListEqual(['no sufficient access to die command'], mike.message_history)

    def test_cmdalias_invalid_alias_specified(self):
        superadmin = FakeClient(self.console, name='superadmin', guid='superadminguid', groupBits=128)
        superadmin.connects('1')
        self.assert_cmd_alias('help', 'h')
        superadmin.clearMessageHistory()
        superadmin.says('!cmdalias help !')
        self.assertListEqual(['invalid data, try !help cmdalias'], superadmin.message_history)
        self.assert_cmd_alias('help', 'h')

    def test_cmdalias_already_in_use(self):
        superadmin = FakeClient(self.console, name='superadmin', guid='superadminguid', groupBits=128)
        superadmin.connects('1')
        self.assert_cmd_alias('ban', 'b')
        superadmin.clearMessageHistory()
        superadmin.says('!cmdalias ban tempban')
        self.assertListEqual(['command tempban is already in use'], superadmin.message_history)
        self.assert_cmd_alias('ban', 'b')

    def test_cmdalias_add_alias(self):
        superadmin = FakeClient(self.console, name='superadmin', guid='superadminguid', groupBits=128)
        superadmin.connects('1')
        self.assert_cmd_alias('register', None)
        superadmin.clearMessageHistory()
        superadmin.says('!cmdalias register newregister')
        self.assertListEqual(['added alias for command register: newregister'], superadmin.message_history)
        self.assert_cmd_alias('register', 'newregister')
        return

    def test_cmdalias_update_alias(self):
        superadmin = FakeClient(self.console, name='superadmin', guid='superadminguid', groupBits=128)
        superadmin.connects('1')
        self.assert_cmd_alias('help', 'h')
        superadmin.clearMessageHistory()
        superadmin.says('!cmdalias help newhelp')
        self.assertListEqual(['updated alias for command help: newhelp'], superadmin.message_history)
        self.assert_cmd_alias('help', 'newhelp')

    def test_cmdgrant_with_invalid_command(self):
        superadmin = FakeClient(self.console, name='superadmin', guid='superadminguid', groupBits=128)
        superadmin.connects('1')
        mike = FakeClient(self.console, name='mike', guid='mikeguid', groupBits=1)
        mike.connects('2')
        superadmin.clearMessageHistory()
        superadmin.says('!cmdgrant mike fakecommand')
        self.assertListEqual(['could not find command fakecommand'], superadmin.message_history)

    def test_cmdgrant_with_lower_group_level(self):
        superadmin = FakeClient(self.console, name='superadmin', guid='superadminguid', groupBits=128)
        superadmin.connects('1')
        mike = FakeClient(self.console, name='mike', guid='mikeguid', groupBits=1)
        mike.connects('2')
        superadmin.clearMessageHistory()
        mike.clearMessageHistory()
        mike.says('!cmdlevel cmdlevel')
        superadmin.says('!cmdgrant mike cmdlevel')
        mike.says('!cmdlevel cmdlevel')
        grantlist = getattr(mike, GRANT_SET_ATTR, None)
        self.assertIsNotNone(grantlist)
        self.assertIn('cmdlevel', grantlist)
        self.assertLess(mike.maxLevel, self.adminPlugin._commands['cmdlevel'].level[0])
        self.assertListEqual(['mike has now a grant for cmdlevel command'], superadmin.message_history)
        self.assertListEqual(['You need to be in group Full Admin to use !cmdlevel',
         'command cmdlevel level: fulladmin'], mike.message_history)
        return

    def test_cmdgrant_with_higher_group_level(self):
        superadmin = FakeClient(self.console, name='superadmin', guid='superadminguid', groupBits=128)
        superadmin.connects('1')
        mike = FakeClient(self.console, name='mike', guid='mikeguid', groupBits=64)
        mike.connects('2')
        superadmin.clearMessageHistory()
        superadmin.says('!cmdgrant mike cmdlevel')
        grantlist = getattr(mike, GRANT_SET_ATTR, None)
        self.assertIsNone(grantlist)
        self.assertListEqual(['mike is already able to use cmdlevel command'], superadmin.message_history)
        return

    def test_cmdgrant_with_client_reconnection(self):
        superadmin = FakeClient(self.console, name='superadmin', guid='superadminguid', groupBits=128)
        superadmin.connects('1')
        mike = FakeClient(self.console, id='10', name='mike', guid='mikeguid', groupBits=1)
        mike.connects('2')
        superadmin.clearMessageHistory()
        superadmin.says('!cmdgrant mike cmdlevel')
        mike.disconnects()
        del mike
        mike = FakeClient(self.console, id='10', name='mike', guid='mikeguid', groupBits=1)
        mike.connects('2')
        grantlist = getattr(mike, GRANT_SET_ATTR, None)
        self.assertIsNotNone(grantlist)
        self.assertIsInstance(grantlist, set)
        self.assertEqual(1, len(grantlist))
        return

    def test_cmdrevoke_with_no_grant_given(self):
        superadmin = FakeClient(self.console, name='superadmin', guid='superadminguid', groupBits=128)
        superadmin.connects('1')
        mike = FakeClient(self.console, name='mike', guid='mikeguid', groupBits=64)
        mike.connects('2')
        superadmin.clearMessageHistory()
        superadmin.says('!cmdrevoke mike cmdlevel')
        self.assertListEqual(['mike has no grant for cmdlevel command'], superadmin.message_history)

    def test_cmdrevoke_with_previously_given_grant(self):
        superadmin = FakeClient(self.console, name='superadmin', guid='superadminguid', groupBits=128)
        superadmin.connects('1')
        mike = FakeClient(self.console, name='mike', guid='mikeguid', groupBits=1)
        mike.connects('2')
        superadmin.says('!cmdgrant mike cmdlevel')
        superadmin.clearMessageHistory()
        superadmin.says('!cmdrevoke mike cmdlevel')
        self.assertListEqual(["mike's grant for cmdlevel command has been removed"], superadmin.message_history)

    def test_cmdrevoke_with_previously_given_grant_and_high_group_level(self):
        superadmin = FakeClient(self.console, name='superadmin', guid='superadminguid', groupBits=128)
        superadmin.connects('1')
        mike = FakeClient(self.console, name='mike', guid='mikeguid', groupBits=1)
        mike.connects('2')
        superadmin.says('!cmdgrant mike cmdlevel')
        mike.groupBits = 64
        mike._maxLevel = 80
        superadmin.clearMessageHistory()
        superadmin.says('!cmdrevoke mike cmdlevel')
        self.assertListEqual(["mike's grant for cmdlevel command has been removed",
         'but his group level is high enough to access the command'], superadmin.message_history)

    def test_cmdrevoke_with_client_reconnection(self):
        superadmin = FakeClient(self.console, name='superadmin', guid='superadminguid', groupBits=128)
        superadmin.connects('1')
        mike = FakeClient(self.console, id='10', name='mike', guid='mikeguid', groupBits=1)
        mike.connects('2')
        superadmin.clearMessageHistory()
        superadmin.says('!cmdgrant mike cmdlevel')
        superadmin.says('!cmdrevoke mike cmdlevel')
        mike.disconnects()
        del mike
        mike = FakeClient(self.console, id='10', name='mike', guid='mikeguid', groupBits=1)
        mike.connects('2')
        grantlist = getattr(mike, GRANT_SET_ATTR, None)
        self.assertIsNotNone(grantlist)
        self.assertIsInstance(grantlist, set)
        self.assertEqual(0, len(grantlist))
        return

    def test_cmduse_no_access(self):
        superadmin = FakeClient(self.console, name='superadmin', guid='superadminguid', groupBits=128)
        superadmin.connects('1')
        mike = FakeClient(self.console, name='mike', guid='mikeguid', groupBits=1)
        mike.connects('2')
        superadmin.clearMessageHistory()
        superadmin.says('!cmduse mike cmdlevel')
        self.assertListEqual(['mike has no access to cmdlevel command'], superadmin.message_history)

    def test_cmduse_access(self):
        superadmin = FakeClient(self.console, name='superadmin', guid='superadminguid', groupBits=128)
        superadmin.connects('1')
        mike = FakeClient(self.console, name='mike', guid='mikeguid', groupBits=64)
        mike.connects('2')
        superadmin.clearMessageHistory()
        superadmin.says('!cmduse mike cmdlevel')
        self.assertListEqual(['mike has access to cmdlevel command'], superadmin.message_history)