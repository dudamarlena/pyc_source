# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/nushell/tests/test_filter.py
# Compiled at: 2019-10-27 12:36:45
# Size of source mod 2**32: 3021 bytes
from nushell.filter import FilterPlugin
from .helpers import assert_good_response, check_plugin_config, check_remove_help
from .plugin_requests import config_request, filter_begin_request, filter_end_request, filter_string_request, filter_int_request, filter_custom_request
import os, pytest

def func(plugin, params):
    """func will be executed by the calling FilterPlugin when method is "filter"
       instead of printing responses, we return them to the caller for testing
    """
    return params


def test_filter_plugin(tmp_path):
    """test creation of a simple sink plugin
    """
    plugin_name = 'filter'
    usage = 'A dummy filter plugin to print to the terminal'
    plugin = FilterPlugin(name=plugin_name, usage=usage, logging=False)
    for attr in ('params', 'args'):
        assert not getattr(plugin, attr, None)

    response = plugin.test(func, config_request)
    assert_good_response(response)
    assert plugin.get_config() == response['params']['Ok']
    for attr in ('params', 'args'):
        assert getattr(plugin, attr) in [[], {}]

    response = plugin.test(func, filter_begin_request)
    assert_good_response(response)
    assert response['params'] == {'Ok': []}
    assert 'args' in plugin.params
    if not ('help' in plugin.args and '_positional' in plugin.args):
        raise AssertionError
    response = plugin.test(func, filter_string_request)
    assert plugin.get_string_primitive() == 'pancakes'
    for key in ('help', '_positional'):
        assert key in response

    response = plugin.test(func, filter_int_request)
    assert plugin.get_int_primitive() == 'imanumber'
    response = plugin.test(func, filter_custom_request)
    assert plugin.get_primitive('Any') == 'imathing'
    response = plugin.test(func, filter_end_request)


def test_filter_config(tmp_path):
    """test configure of a simple sink plugin
    """
    plugin_name = 'filter'
    usage = 'A dummy filter plugin to print to the terminal'
    plugin = FilterPlugin(name=plugin_name, usage=usage, logging=False)
    check_plugin_config(plugin, plugin_name, usage, is_filter=True)
    plugin = FilterPlugin(name=plugin_name, usage=usage, logging=False, add_help=False)
    check_remove_help(plugin, plugin_name, usage, is_filter=True)