# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/nushell/tests/test_sink.py
# Compiled at: 2019-10-27 12:34:35
# Size of source mod 2**32: 2517 bytes
from nushell.sink import SinkPlugin
from .helpers import assert_good_response, check_plugin_config, check_remove_help
from .plugin_requests import config_request, sink_named_request, sink_help_request
import os, pytest

def sink(plugin, params):
    """sink will be executed by the calling SinkPlugin when method is "sink"
       instead of just printing, we return params to test
    """
    return params


def test_sink_name(tmp_path):
    """ensure that a plugin's name is made all lowercase, with spaces removed
       note that the user is allowed to use special characters.
    """
    plugin_name = 'sink'
    usage = 'A dummy sink plugin to print to the terminal'
    plugin = SinkPlugin(name=plugin_name, usage=usage, logging=False)
    assert plugin._clean_name('a a a') == 'a-a-a'
    assert plugin._clean_name('SINK') == 'sink'


def test_sink_plugin(tmp_path):
    """test creation of a simple sink plugin
    """
    plugin_name = 'sink'
    usage = 'A dummy sink plugin to print to the terminal'
    plugin = SinkPlugin(name=plugin_name, usage=usage, logging=False)
    response = plugin.test(sink, config_request)
    assert_good_response(response)
    assert plugin.get_config() == response['params']['Ok']
    response = plugin.test(sink, sink_help_request)
    if not (plugin.name in response and plugin.usage in response):
        raise AssertionError
    response = plugin.test(sink, sink_named_request)
    for key in ('sink', '_positional', '_pipe'):
        assert key in response


def test_sink_config(tmp_path):
    """test configure of a simple sink plugin
    """
    plugin_name = 'sink'
    usage = 'A dummy sink plugin to print to the terminal'
    plugin = SinkPlugin(name=plugin_name, usage=usage, logging=False)
    check_plugin_config(plugin, plugin_name, usage, is_filter=False)
    plugin = SinkPlugin(name=plugin_name, usage=usage, logging=False, add_help=False)
    check_remove_help(plugin, plugin_name, usage, is_filter=False)