# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /root/droopescan/dscan/plugins/internal/base_plugin.py
# Compiled at: 2019-06-14 01:34:00
# Size of source mod 2**32: 963 bytes
from __future__ import print_function
from dscan.plugins.internal.base_plugin_internal import BasePluginInternal
import dscan

class BasePlugin(BasePluginInternal):
    __doc__ = '\n        For documentation regarding these variables, please see\n        example.py\n    '
    forbidden_url = None
    regular_file_url = None
    plugins_base_url = None
    plugins_file = None
    module_common_file = None
    themes_base_url = None
    themes_file = None
    versions_file = None
    interesting_urls = None
    can_enumerate_plugins = True
    can_enumerate_themes = True
    can_enumerate_interesting = True
    can_enumerate_version = True

    def __init__(self):
        super(BasePlugin, self).__init__()
        label = self._meta.label
        self.plugins_file = dscan.PWD + 'plugins/%s/plugins.txt' % label
        self.themes_file = dscan.PWD + 'plugins/%s/themes.txt' % label
        self.versions_file = dscan.PWD + 'plugins/%s/versions.xml' % label