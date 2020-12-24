# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/wafw00f/manager.py
# Compiled at: 2020-02-20 22:34:09
# Size of source mod 2**32: 718 bytes
"""
Copyright (C) 2020, WAFW00F Developers.
See the LICENSE file for copying permission.
"""
import os
from functools import partial
from pluginbase import PluginBase

def load_plugins():
    here = os.path.abspath(os.path.dirname(__file__))
    get_path = partial(os.path.join, here)
    plugin_dir = get_path('plugins')
    plugin_base = PluginBase(package='wafw00f.plugins',
      searchpath=[plugin_dir])
    plugin_source = plugin_base.make_plugin_source(searchpath=[
     plugin_dir],
      persist=True)
    plugin_dict = {}
    for plugin_name in plugin_source.list_plugins():
        plugin_dict[plugin_name] = plugin_source.load_plugin(plugin_name)

    return plugin_dict