# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/sutekh/gui/ConfigFile.py
# Compiled at: 2019-12-11 16:37:54
"""Configuration handling for the Sutekh GUI."""
import pkg_resources
from sutekh.base.gui.BaseConfigFile import BaseConfigFile
from sutekh.base.gui.MessageBus import MessageBus, CONFIG_MSG

class ConfigFile(BaseConfigFile):
    """Application overrides for the ConfigFile

       Provides application overrides and the default setup.
       """
    DEFAULT_FILTERS = {'Default Filter Template': '(Clan in $var0) or (Discipline in $var1) or (CardType in $var2) or (CardFunction in $var3)', 
       'Clan': 'Clan in $var0', 
       'Discipline': 'Discipline in $var0', 
       'Card Type': 'CardType in $var0', 
       'Card Text': 'CardText in $var0', 
       'Card Name': 'CardName in $var0', 
       'Card Set Name': 'CardSetName in $var0', 
       'Physical Expansion': 'PhysicalExpansion in $var0'}

    def _get_app_configspec_file(self):
        """Get the application specific config file"""
        fConfigSpec = pkg_resources.resource_stream(__name__, 'configspec.ini')
        return fConfigSpec

    def get_show_errata_markers(self):
        """Query the 'show errata markers' option."""
        return self._oConfig['main']['show errata markers']

    def set_show_errata_markers(self, bShowErrata):
        """Set the 'show errata markers' option."""
        self._oConfig['main']['show errata markers'] = bShowErrata
        MessageBus.publish(CONFIG_MSG, 'show_errata_markers')

    def sanitize(self):
        """Called after validation to clean up a valid config.

           Currently clean-up consists of adding some open panes if none
           are listed.
           """
        if not self._oConfig['open_frames']:
            self.add_frame(1, 'physical_card', 'Full Card List', False, False, -1, None)
            self.add_frame(2, 'Card Text', 'Card Text', False, False, -1, None)
            self.add_frame(3, 'Card Set List', 'Card Set List', False, False, -1, None)
            self.add_frame(4, 'physical_card_set', 'My Collection', False, False, -1, None)
        if 'last cardlist update' in self._oConfig['main']:
            self._oConfig['main'].pop('last cardlist update')
        return