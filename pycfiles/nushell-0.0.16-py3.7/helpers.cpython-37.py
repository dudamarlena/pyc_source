# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/nushell/tests/helpers.py
# Compiled at: 2019-10-27 12:44:16
# Size of source mod 2**32: 2371 bytes


def assert_good_response(response):
    """ensure that a response is good, meaning jsonrpc 2.0 and method response
    """
    for key in ('jsonrpc', 'method', 'params'):
        assert key in response

    assert isinstance(response['params'], (dict, list))
    assert response['method'] == 'response'


def check_plugin_config(plugin, plugin_name, usage, is_filter):
    """a helper function to test a general plugin configuration
    """
    assert not plugin.argUsage
    assert not plugin.positional
    assert not plugin._positional
    assert not plugin.named
    assert '--help' not in plugin.get_help()
    plugin_config = plugin.get_config()
    assert 'help' in plugin.named
    for key in ('name', 'usage', 'positional', 'rest_positional', 'named', 'is_filter'):
        assert key in plugin_config

    assert plugin_config['is_filter'] == is_filter
    assert plugin_config['usage'] == usage
    assert plugin_config['name'] == plugin_name
    assert plugin.name == plugin_name
    assert plugin.usage == usage
    for contender in [usage, plugin_name, '--help', 'show this usage']:
        assert contender in plugin.get_help()


def check_remove_help(plugin, plugin_name, usage, is_filter):
    """similar checks, but remove the help parameters
    """
    plugin_config = plugin.get_config()
    assert 'help' not in plugin.named
    assert '--help' not in plugin.get_help()
    plugin.add_named_argument('greet', 'Switch', usage='say hello')
    assert 'greet' in plugin.argUsage
    assert 'greet' in plugin.named
    plugin.add_positional_argument('avatar', 'Optional', 'String')
    assert 'avatar' in plugin._positional
    assert plugin.positional