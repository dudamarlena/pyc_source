# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/updatorr/__init__.py
# Compiled at: 2013-04-10 09:49:36
from deluge.plugins.init import PluginInitBase
VERSION = (0, 1, 8)

class CorePlugin(PluginInitBase):

    def __init__(self, plugin_name):
        from core import Core as _plugin_cls
        self._plugin_cls = _plugin_cls
        super(CorePlugin, self).__init__(plugin_name)


class GtkUIPlugin(PluginInitBase):

    def __init__(self, plugin_name):
        from gtkui import GtkUI as _plugin_cls
        self._plugin_cls = _plugin_cls
        super(GtkUIPlugin, self).__init__(plugin_name)


class WebUIPlugin(PluginInitBase):

    def __init__(self, plugin_name):
        from webui import WebUI as _plugin_cls
        self._plugin_cls = _plugin_cls
        super(WebUIPlugin, self).__init__(plugin_name)