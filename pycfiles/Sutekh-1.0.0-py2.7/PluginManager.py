# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/sutekh/gui/PluginManager.py
# Compiled at: 2019-12-11 16:37:54
"""Classes for managing and creating plugins for Sutekh."""
import sutekh.gui.plugins as plugins
from sutekh.base.gui.BasePluginManager import BasePluginManager, BasePlugin

class SutekhPlugin(BasePlugin):
    """Class for Sutekh plugins."""
    pass


class PluginManager(BasePluginManager):
    """Manages plugins for Sutekh."""
    cAppPlugin = SutekhPlugin
    sPluginDir = 'sutekh.gui.plugins'

    def load_plugins(self):
        """Load list of Plugin Classes from plugin dir."""
        self._do_load_plugins(plugins)