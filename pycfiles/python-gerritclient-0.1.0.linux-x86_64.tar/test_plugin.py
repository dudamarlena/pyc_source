# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/machin/.virtualenvs/twine/lib/python2.7/site-packages/gerritclient/tests/unit/cli/test_plugin.py
# Compiled at: 2017-06-06 13:27:08
import mock, os
from gerritclient.tests.unit.cli import clibase
from gerritclient.tests.utils import fake_plugin

class TestPluginCommand(clibase.BaseCLITest):
    """Tests for gerrit plugin * commands."""

    def setUp(self):
        super(TestPluginCommand, self).setUp()
        self.m_client.get_all.return_value = fake_plugin.get_fake_plugins(10)
        get_fake_plugin = fake_plugin.get_fake_plugin(plugin_id='fake-plugin')
        self.m_client.get_by_id.return_value = get_fake_plugin

    def test_plugin_list_enabled(self):
        args = 'plugin list'
        self.exec_command(args)
        self.m_get_client.assert_called_once_with('plugin', mock.ANY)
        self.m_client.get_all.assert_called_once_with(detailed=False)

    def test_plugin_list_all(self):
        args = 'plugin list --all'
        self.exec_command(args)
        self.m_get_client.assert_called_once_with('plugin', mock.ANY)
        self.m_client.get_all.assert_called_once_with(detailed=True)

    def test_plugin_show(self):
        plugin_id = 'fake-plugin'
        args = ('plugin show {plugin_id}').format(plugin_id=plugin_id)
        self.exec_command(args)
        self.m_get_client.assert_called_once_with('plugin', mock.ANY)
        self.m_client.get_by_id.assert_called_once_with(plugin_id)

    def test_plugin_enable(self):
        plugin_id = 'fake-plugin'
        args = ('plugin enable {plugin_id}').format(plugin_id=plugin_id)
        self.exec_command(args)
        self.m_get_client.assert_called_once_with('plugin', mock.ANY)
        self.m_client.enable.assert_called_once_with(plugin_id)

    def test_plugin_disable(self):
        plugin_id = 'fake-plugin'
        args = ('plugin disable {plugin_id}').format(plugin_id=plugin_id)
        self.exec_command(args)
        self.m_get_client.assert_called_once_with('plugin', mock.ANY)
        self.m_client.disable.assert_called_once_with(plugin_id)

    @mock.patch('sys.stderr')
    def test_plugin_enable_fail(self, mocked_stderr):
        args = 'plugin enable'
        self.assertRaises(SystemExit, self.exec_command, args)
        self.assertIn('plugin enable: error:', mocked_stderr.write.call_args_list[(-1)][0][0])

    @mock.patch('sys.stderr')
    def test_plugin_disable_fail(self, mocked_stderr):
        args = 'plugin disable'
        self.assertRaises(SystemExit, self.exec_command, args)
        self.assertIn('plugin disable: error:', mocked_stderr.write.call_args_list[(-1)][0][0])

    def test_plugin_reload(self):
        plugin_id = 'fake-plugin'
        args = ('plugin reload {plugin_id}').format(plugin_id=plugin_id)
        self.exec_command(args)
        self.m_get_client.assert_called_once_with('plugin', mock.ANY)
        self.m_client.reload.assert_called_once_with(plugin_id)

    def test_plugin_install_from_url(self):
        plugin_id = 'fake-plugin.jar'
        url = 'http://url/path/to/plugin.jar'
        args = ('plugin install {plugin_id} --url {url}').format(plugin_id=plugin_id, url=url)
        self.m_client.install.return_value = fake_plugin.get_fake_plugin(plugin_id)
        self.exec_command(args)
        self.m_get_client.assert_called_once_with('plugin', mock.ANY)
        self.m_client.install.assert_called_once_with(plugin_id, source_type='url', value=url)

    @mock.patch('gerritclient.common.utils.file_exists', mock.Mock(return_value=True))
    def test_plugin_install_from_file(self):
        plugin_id = 'fake-plugin.jar'
        expected_path = '/tmp/fakes/fake-plugin.jar'
        data = os.urandom(12)
        self.m_client.install.return_value = fake_plugin.get_fake_plugin(plugin_id)
        args = ('plugin install {plugin_id} --file {file_path}').format(plugin_id=plugin_id, file_path=expected_path)
        m_open = mock.mock_open(read_data=data)
        with mock.patch('gerritclient.commands.plugin.open', m_open, create=True):
            self.exec_command(args)
        m_open.assert_called_once_with(expected_path, 'rb')
        self.m_get_client.assert_called_once_with('plugin', mock.ANY)
        self.m_client.install.assert_called_once_with(plugin_id, source_type='file', value=data)

    @mock.patch('sys.stderr')
    def test_plugin_install_w_wrong_identifier_fail(self, mocked_stderr):
        plugin_id = 'bad-plugin-identifier'
        url = 'http://url/path/to/plugin.jar'
        args = ('plugin install {plugin_id} --url {url}').format(plugin_id=plugin_id, url=url)
        self.assertRaises(ValueError, self.exec_command, args)
        self.assertIn('Plugin identifier must contain ".jar" prefix', mocked_stderr.write.call_args_list[0][0][0])