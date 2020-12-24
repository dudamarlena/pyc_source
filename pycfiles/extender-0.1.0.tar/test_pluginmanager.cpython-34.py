# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/messense/Projects/extender/tests/test_pluginmanager.py
# Compiled at: 2014-06-08 07:05:41
# Size of source mod 2**32: 1932 bytes
import nose
from nose.tools import raises
from extender import PluginManager, Plugin

def test_plugins_install():
    plugins = PluginManager()
    plugins.install('extender.plugins')
    msg = plugins.first('test_func1', 'test')
    assert msg == 'test'


def test_plugin_get():
    plugins = PluginManager()
    plugins.install('extender.plugins')
    assert plugins.get('plugin1') is not None


@raises(KeyError)
def test_plugin_get_with_nonexists_slug():
    plugins = PluginManager()
    plugins.install('extender.plugins')
    plugins.get('test-plugin')


def test_plugins_enable():
    plugins = PluginManager()
    plugins.install('extender.plugins')
    len1 = len(plugins)
    len2 = sum(1 for i in plugins.all(include_disabled=False))
    assert len1 == 3
    assert len2 == 2


def test_plugins_call():
    plugins = PluginManager()
    plugins.install('extender.plugins')
    result = plugins.call('test_func2', 2, 1)
    assert 'a + b = 3' in result
    assert 'a - b = 1' in result
    assert 'a * b = 2' not in result


def test_plugins_apply():
    plugins = PluginManager()
    plugins.install('extender.plugins')
    value = plugins.apply('test_func3', 'test')
    assert value == 'Plugin1 Plugin2 test'


class TestPlugin(Plugin):
    __test__ = False
    title = 'TestPlugin'
    slug = 'testplugin'
    description = 'My awesome plugin!'
    version = '0.0.1'
    priority = 2
    author = 'Your Name'
    author_url = 'https://github.com/yourname/pluginname'

    def test(self):
        return 'test'


def test_plugin_register():
    plugins = PluginManager()
    plugins.register(TestPlugin)
    assert plugins.first('test') == 'test'


def test_plugin_unregister():
    plugins = PluginManager()
    plugins.install('extender.plugins')
    assert len(plugins) == 3
    plugins.unregister('plugin3')
    assert len(plugins) == 2


if __name__ == '__main__':
    nose.runmodule()