# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/webapi/__init__.py
# Compiled at: 2019-09-28 01:15:14
# Size of source mod 2**32: 887 bytes
VERSION = (0, 4, 0)
try:
    from deluge.plugins.init import PluginInitBase

    class CorePlugin(PluginInitBase):

        def __init__(self, plugin_name):
            from .core import Core as _plugin_cls
            self._plugin_cls = _plugin_cls
            super(CorePlugin, self).__init__(plugin_name)


    class Gtk3UIPlugin(PluginInitBase):

        def __init__(self, plugin_name):
            from .gtk3ui import Gtk3UI as _plugin_cls
            self._plugin_cls = _plugin_cls
            super(Gtk3UIPlugin, self).__init__(plugin_name)


    class WebUIPlugin(PluginInitBase):

        def __init__(self, plugin_name):
            from .webui import WebUI as _plugin_cls
            self._plugin_cls = _plugin_cls
            super(WebUIPlugin, self).__init__(plugin_name)


except ImportError:
    pass