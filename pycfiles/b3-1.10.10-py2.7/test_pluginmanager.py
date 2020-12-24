# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: H:\workspaces\workspace-python\big-brother-bot\tests\plugins\test_pluginmanager.py
# Compiled at: 2015-05-27 19:37:28
import b3, b3.cron, os, unittest2 as unittest
from textwrap import dedent
from mock import Mock
from mockito import when
from b3.plugin import Plugin
from b3.plugins.admin import AdminPlugin
from b3.plugins.admin import Command
from b3.plugins.pluginmanager import PluginmanagerPlugin
from b3.config import CfgConfigParser
from b3.fake import FakeClient
from b3 import __file__ as b3_module__file__
from tests import B3TestCase
ADMIN_CONFIG_FILE = os.path.normpath(os.path.join(os.path.dirname(b3_module__file__), 'conf/plugin_admin.ini'))

@unittest.skipUnless(os.path.exists(ADMIN_CONFIG_FILE), reason='cannot get default plugin config file at %s' % ADMIN_CONFIG_FILE)
class Pluginmanager_TestCase(B3TestCase):

    def setUp(self):
        B3TestCase.setUp(self)
        self.console.gameName = 'f00'
        self.adminPlugin = AdminPlugin(self.console, ADMIN_CONFIG_FILE)
        when(self.console).getPlugin('admin').thenReturn(self.adminPlugin)
        self.adminPlugin.onLoadConfig()
        self.adminPlugin.onStartup()
        self.conf = CfgConfigParser()
        self.conf.loadFromString(dedent('\n            [commands]\n            plugin: superadmin\n        '))
        self.p = PluginmanagerPlugin(self.console, self.conf)
        when(self.console).getPlugin('pluginmanager').thenReturn(self.adminPlugin)
        self.p.onLoadConfig()
        self.p.onStartup()
        when(self.console.config).get_external_plugins_dir().thenReturn(b3.getAbsolutePath('@b3\\extplugins'))
        self.console._plugins['admin'] = self.adminPlugin
        self.console._plugins['pluginmanager'] = self.p

    def tearDown(self):
        self.console._plugins.clear()
        B3TestCase.tearDown(self)


@unittest.skipUnless(os.path.exists(ADMIN_CONFIG_FILE), reason='cannot get default plugin config file at %s' % ADMIN_CONFIG_FILE)
class Test_commands(Pluginmanager_TestCase):

    def test_cmd_plugin_no_parameters(self):
        superadmin = FakeClient(self.console, name='superadmin', guid='superadminguid', groupBits=128)
        superadmin.connects('1')
        superadmin.clearMessageHistory()
        superadmin.says('!plugin')
        self.assertListEqual(['invalid data, try !help plugin'], superadmin.message_history)

    def test_cmd_plugin_with_invalid_command_name(self):
        superadmin = FakeClient(self.console, name='superadmin', guid='superadminguid', groupBits=128)
        superadmin.connects('1')
        superadmin.clearMessageHistory()
        superadmin.says('!plugin fake')
        self.assertListEqual(['usage: !plugin <disable|enable|info|list|load|unload> [<data>]'], superadmin.message_history)

    def test_cmd_plugin_list(self):
        superadmin = FakeClient(self.console, name='superadmin', guid='superadminguid', groupBits=128)
        superadmin.connects('1')
        superadmin.clearMessageHistory()
        superadmin.says('!plugin list')
        self.assertListEqual(['Loaded plugins: admin, pluginmanager'], superadmin.message_history)

    def test_cmd_plugin_enable_with_no_plugin_name(self):
        superadmin = FakeClient(self.console, name='superadmin', guid='superadminguid', groupBits=128)
        superadmin.connects('1')
        superadmin.clearMessageHistory()
        superadmin.says('!plugin enable')
        self.assertListEqual(['usage: !plugin enable <name/s>'], superadmin.message_history)

    def test_cmd_plugin_enable_protected(self):
        superadmin = FakeClient(self.console, name='superadmin', guid='superadminguid', groupBits=128)
        superadmin.connects('1')
        superadmin.clearMessageHistory()
        superadmin.says('!plugin enable admin')
        self.assertListEqual(['Plugin admin is protected'], superadmin.message_history)

    def test_cmd_plugin_enable_with_invalid_plugin_name(self):
        superadmin = FakeClient(self.console, name='superadmin', guid='superadminguid', groupBits=128)
        superadmin.connects('1')
        superadmin.clearMessageHistory()
        superadmin.says('!plugin enable fake')
        self.assertListEqual(['Plugin fake is not loaded'], superadmin.message_history)

    def test_cmd_plugin_enable_with_already_enabled_plugin(self):
        mock_plugin = Mock(spec=Plugin)
        mock_plugin.isEnabled = Mock(return_value=True)
        when(self.console).getPlugin('mock').thenReturn(mock_plugin)
        superadmin = FakeClient(self.console, name='superadmin', guid='superadminguid', groupBits=128)
        superadmin.connects('1')
        superadmin.clearMessageHistory()
        superadmin.says('!plugin enable mock')
        self.assertListEqual(['Plugin mock is already enabled'], superadmin.message_history)

    def test_cmd_plugin_enable_succeed(self):
        mock_plugin = Mock(spec=Plugin)
        mock_plugin.isEnabled = Mock(return_value=False)
        when(self.console).getPlugin('mock').thenReturn(mock_plugin)
        superadmin = FakeClient(self.console, name='superadmin', guid='superadminguid', groupBits=128)
        superadmin.connects('1')
        superadmin.clearMessageHistory()
        superadmin.says('!plugin enable mock')
        self.assertListEqual(['Plugin mock is now enabled'], superadmin.message_history)

    def test_cmd_plugin_enable_succeed_multiple(self):
        mock_pluginA = Mock(spec=Plugin)
        mock_pluginA.isEnabled = Mock(return_value=False)
        when(self.console).getPlugin('mocka').thenReturn(mock_pluginA)
        mock_pluginB = Mock(spec=Plugin)
        mock_pluginB.isEnabled = Mock(return_value=False)
        when(self.console).getPlugin('mockb').thenReturn(mock_pluginB)
        superadmin = FakeClient(self.console, name='superadmin', guid='superadminguid', groupBits=128)
        superadmin.connects('1')
        superadmin.clearMessageHistory()
        superadmin.says('!plugin enable mocka mockb')
        self.assertListEqual(['Plugin mocka is now enabled', 'Plugin mockb is now enabled'], superadmin.message_history)

    def test_cmd_plugin_enable_mixed_multiple(self):
        mock_pluginA = Mock(spec=Plugin)
        mock_pluginA.isEnabled = Mock(return_value=False)
        when(self.console).getPlugin('mock').thenReturn(mock_pluginA)
        superadmin = FakeClient(self.console, name='superadmin', guid='superadminguid', groupBits=128)
        superadmin.connects('1')
        superadmin.clearMessageHistory()
        superadmin.says('!plugin enable mock fake')
        self.assertListEqual(['Plugin mock is now enabled', 'Plugin fake is not loaded'], superadmin.message_history)

    def test_cmd_plugin_disable_with_no_plugin_name(self):
        superadmin = FakeClient(self.console, name='superadmin', guid='superadminguid', groupBits=128)
        superadmin.connects('1')
        superadmin.clearMessageHistory()
        superadmin.says('!plugin disable')
        self.assertListEqual(['usage: !plugin disable <name/s>'], superadmin.message_history)

    def test_cmd_plugin_disable_protected(self):
        superadmin = FakeClient(self.console, name='superadmin', guid='superadminguid', groupBits=128)
        superadmin.connects('1')
        superadmin.clearMessageHistory()
        superadmin.says('!plugin disable admin')
        self.assertListEqual(['Plugin admin is protected'], superadmin.message_history)

    def test_cmd_plugin_disable_with_invalid_plugin_name(self):
        superadmin = FakeClient(self.console, name='superadmin', guid='superadminguid', groupBits=128)
        superadmin.connects('1')
        superadmin.clearMessageHistory()
        superadmin.says('!plugin disable fake')
        self.assertListEqual(['Plugin fake is not loaded'], superadmin.message_history)

    def test_cmd_plugin_disable_with_already_disable_plugin(self):
        mock_plugin = Mock(spec=Plugin)
        mock_plugin.isEnabled = Mock(return_value=False)
        when(self.console).getPlugin('mock').thenReturn(mock_plugin)
        superadmin = FakeClient(self.console, name='superadmin', guid='superadminguid', groupBits=128)
        superadmin.connects('1')
        superadmin.clearMessageHistory()
        superadmin.says('!plugin disable mock')
        self.assertListEqual(['Plugin mock is already disabled'], superadmin.message_history)

    def test_cmd_plugin_disable_succeed(self):
        mock_plugin = Mock(spec=Plugin)
        mock_plugin.isEnabled = Mock(return_value=True)
        when(self.console).getPlugin('mock').thenReturn(mock_plugin)
        superadmin = FakeClient(self.console, name='superadmin', guid='superadminguid', groupBits=128)
        superadmin.connects('1')
        superadmin.clearMessageHistory()
        superadmin.says('!plugin disable mock')
        self.assertListEqual(['Plugin mock is now disabled'], superadmin.message_history)

    def test_cmd_plugin_disable_succeed_multiple(self):
        mock_pluginA = Mock(spec=Plugin)
        mock_pluginA.isEnabled = Mock(return_value=True)
        when(self.console).getPlugin('mocka').thenReturn(mock_pluginA)
        mock_pluginB = Mock(spec=Plugin)
        mock_pluginB.isEnabled = Mock(return_value=True)
        when(self.console).getPlugin('mockb').thenReturn(mock_pluginB)
        superadmin = FakeClient(self.console, name='superadmin', guid='superadminguid', groupBits=128)
        superadmin.connects('1')
        superadmin.clearMessageHistory()
        superadmin.says('!plugin disable mocka mockb')
        self.assertListEqual(['Plugin mocka is now disabled', 'Plugin mockb is now disabled'], superadmin.message_history)

    def test_cmd_plugin_disable_mixed_multiple(self):
        mock_pluginA = Mock(spec=Plugin)
        mock_pluginA.isEnabled = Mock(return_value=True)
        when(self.console).getPlugin('mock').thenReturn(mock_pluginA)
        superadmin = FakeClient(self.console, name='superadmin', guid='superadminguid', groupBits=128)
        superadmin.connects('1')
        superadmin.clearMessageHistory()
        superadmin.says('!plugin disable mock fake')
        self.assertListEqual(['Plugin mock is now disabled', 'Plugin fake is not loaded'], superadmin.message_history)

    def test_cmd_plugin_load_with_no_plugin_name(self):
        superadmin = FakeClient(self.console, name='superadmin', guid='superadminguid', groupBits=128)
        superadmin.connects('1')
        superadmin.clearMessageHistory()
        superadmin.says('!plugin load')
        self.assertListEqual(['usage: !plugin load <name/s>'], superadmin.message_history)

    def test_cmd_plugin_load_protected(self):
        superadmin = FakeClient(self.console, name='superadmin', guid='superadminguid', groupBits=128)
        superadmin.connects('1')
        superadmin.clearMessageHistory()
        superadmin.says('!plugin load admin')
        self.assertListEqual(['Plugin admin is protected'], superadmin.message_history)

    def test_cmd_plugin_load_with_already_loaded_plugin(self):
        mock_plugin = Mock(spec=Plugin)
        when(self.console).getPlugin('mock').thenReturn(mock_plugin)
        superadmin = FakeClient(self.console, name='superadmin', guid='superadminguid', groupBits=128)
        superadmin.connects('1')
        superadmin.clearMessageHistory()
        superadmin.says('!plugin load mock')
        self.assertListEqual(['Plugin mock is already loaded'], superadmin.message_history)

    def test_cmd_plugin_load_with_invalid_plugin_name(self):
        superadmin = FakeClient(self.console, name='superadmin', guid='superadminguid', groupBits=128)
        superadmin.connects('1')
        superadmin.clearMessageHistory()
        superadmin.says('!plugin load fake')
        self.assertListEqual(['Missing fake plugin python module', 'Please put the plugin module in @b3/extplugins/'], superadmin.message_history)

    def test_cmd_plugin_unload_with_no_plugin_name(self):
        superadmin = FakeClient(self.console, name='superadmin', guid='superadminguid', groupBits=128)
        superadmin.connects('1')
        superadmin.clearMessageHistory()
        superadmin.says('!plugin unload')
        self.assertListEqual(['usage: !plugin unload <name/s>'], superadmin.message_history)

    def test_cmd_plugin_unload_protected(self):
        superadmin = FakeClient(self.console, name='superadmin', guid='superadminguid', groupBits=128)
        superadmin.connects('1')
        superadmin.clearMessageHistory()
        superadmin.says('!plugin unload admin')
        self.assertListEqual(['Plugin admin is protected'], superadmin.message_history)

    def test_cmd_plugin_unload_with_invalid_plugin_name(self):
        superadmin = FakeClient(self.console, name='superadmin', guid='superadminguid', groupBits=128)
        superadmin.connects('1')
        superadmin.clearMessageHistory()
        superadmin.says('!plugin unload fake')
        self.assertListEqual(['Plugin fake is not loaded'], superadmin.message_history)

    def test_cmd_plugin_unload_with_enabled_plugin(self):
        mock_plugin = Mock(spec=Plugin)
        mock_plugin.isEnabled = Mock(return_value=True)
        when(self.console).getPlugin('mock').thenReturn(mock_plugin)
        superadmin = FakeClient(self.console, name='superadmin', guid='superadminguid', groupBits=128)
        superadmin.connects('1')
        superadmin.clearMessageHistory()
        superadmin.says('!plugin unload mock')
        self.assertListEqual(['Plugin mock is currently enabled: disable it first'], superadmin.message_history)

    def test_cmd_plugin_unload_successful(self):
        mock_plugin = Mock(spec=Plugin)
        mock_plugin.console = self.console
        mock_plugin.isEnabled = Mock(return_value=False)
        when(self.console).getPlugin('mock').thenReturn(mock_plugin)
        self.console._plugins['mock'] = mock_plugin
        mock_func = Mock()
        mock_func.__name__ = 'cmd_mockfunc'
        self.adminPlugin._commands['mockcommand'] = Command(plugin=mock_plugin, cmd='mockcommand', level=100, func=mock_func)
        mock_plugin.onSay = Mock()
        mock_plugin.registerEvent('EVT_CLIENT_SAY', mock_plugin.onSay)
        mock_plugin.mockCronjob = Mock()
        mock_plugin.mockCrontab = b3.cron.PluginCronTab(mock_plugin, mock_plugin.mockCronjob, minute='*', second='*/60')
        self.console.cron.add(mock_plugin.mockCrontab)
        self.assertIn(id(mock_plugin.mockCrontab), self.console.cron._tabs)
        superadmin = FakeClient(self.console, name='superadmin', guid='superadminguid', groupBits=128)
        superadmin.connects('1')
        superadmin.clearMessageHistory()
        superadmin.says('!plugin unload mock')
        self.assertNotIn('mockcommand', self.adminPlugin._commands)
        self.assertIn(self.console.getEventID('EVT_CLIENT_SAY'), self.console._handlers)
        self.assertNotIn(mock_plugin, self.console._handlers[self.console.getEventID('EVT_CLIENT_SAY')])
        self.assertNotIn(id(mock_plugin.mockCrontab), self.console.cron._tabs)
        self.assertListEqual(['Plugin mock has been unloaded'], superadmin.message_history)

    def test_cmd_plugin_info_with_no_plugin_name(self):
        superadmin = FakeClient(self.console, name='superadmin', guid='superadminguid', groupBits=128)
        superadmin.connects('1')
        superadmin.clearMessageHistory()
        superadmin.says('!plugin info')
        self.assertListEqual(['usage: !plugin info <name/s>'], superadmin.message_history)

    def test_cmd_plugin_info_with_valid_plugin_name(self):
        mock_module = Mock()
        mock_module.__setattr__('__author__', 'Mocker')
        mock_module.__setattr__('__version__', '1.1')
        when(self.console).pluginImport('mock').thenReturn(mock_module)
        superadmin = FakeClient(self.console, name='superadmin', guid='superadminguid', groupBits=128)
        superadmin.connects('1')
        superadmin.clearMessageHistory()
        superadmin.says('!plugin info mock')
        self.assertListEqual(['You are running plugin mock v1.1 by Mocker'], superadmin.message_history)

    def test_cmd_plugin_info_with_valid_plugin_name_and_website_escape(self):
        mock_module = Mock()
        mock_module.__setattr__('__author__', 'Mocker - www.mocker.com')
        mock_module.__setattr__('__version__', '1.1')
        when(self.console).pluginImport('mock').thenReturn(mock_module)
        superadmin = FakeClient(self.console, name='superadmin', guid='superadminguid', groupBits=128)
        superadmin.connects('1')
        superadmin.clearMessageHistory()
        superadmin.says('!plugin info mock')
        self.assertListEqual(['You are running plugin mock v1.1 by Mocker'], superadmin.message_history)

    def test_cmd_plugin_info_with_valid_plugin_name_and_email_escape(self):
        mock_module = Mock()
        mock_module.__setattr__('__author__', 'Mocker - info@mocker.co.uk')
        mock_module.__setattr__('__version__', '1.1')
        when(self.console).pluginImport('mock').thenReturn(mock_module)
        superadmin = FakeClient(self.console, name='superadmin', guid='superadminguid', groupBits=128)
        superadmin.connects('1')
        superadmin.clearMessageHistory()
        superadmin.says('!plugin info mock')
        self.assertListEqual(['You are running plugin mock v1.1 by Mocker'], superadmin.message_history)