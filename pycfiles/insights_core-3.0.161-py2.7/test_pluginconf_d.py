# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/parsers/tests/test_pluginconf_d.py
# Compiled at: 2019-05-16 13:41:33
from insights.parsers.pluginconf_d import PluginConfD, PluginConfDIni
from insights.tests import context_wrap
PLUGIN = '\n[main]\nenabled = 0\ngpgcheck = 1\ntimeout = 120\n\n# You can specify options per channel, e.g.:\n#\n#[rhel-i386-server-5]\n#enabled = 1\n#\n#[some-unsigned-custom-channel]\n#gpgcheck = 0\n\n[test]\ntest_multiline_config = http://example.com/repos/test/\n                        http://mirror_example.com/repos/test/\n'
PLUGINPATH = '/etc/yum/plugincon.d/rhnplugin.conf'

def test_pluginconf_d():
    plugin_info = PluginConfD(context_wrap(PLUGIN, path=PLUGINPATH))
    assert plugin_info.data['main'] == {'enabled': '0', 'gpgcheck': '1', 
       'timeout': '120'}
    assert plugin_info.file_path == '/etc/yum/plugincon.d/rhnplugin.conf'
    assert plugin_info.file_name == 'rhnplugin.conf'
    assert plugin_info.data['test'] == {'test_multiline_config': 'http://example.com/repos/test/,http://mirror_example.com/repos/test/'}
    assert sorted(plugin_info) == sorted(['main', 'test'])


def test_pluginconf_d_ini():
    plugin_info = PluginConfDIni(context_wrap(PLUGIN, path=PLUGINPATH))
    assert sorted(plugin_info.sections()) == sorted(['main', 'test'])
    assert 'main' in plugin_info
    assert plugin_info.get('main', 'gpgcheck') == '1'