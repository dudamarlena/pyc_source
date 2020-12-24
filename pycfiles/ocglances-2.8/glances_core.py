# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/fraoustin/Téléchargements/ocglances/tmp/ocglances/plugins/glances_core.py
# Compiled at: 2017-02-11 10:25:25
"""CPU core plugin."""
from ocglances.plugins.glances_plugin import GlancesPlugin
import ocglances.psutil as psutil

class Plugin(GlancesPlugin):
    """Glances CPU core plugin.

    Get stats about CPU core number.

    stats is integer (number of core)
    """

    def __init__(self, args=None):
        """Init the plugin."""
        super(Plugin, self).__init__(args=args)
        self.display_curse = False
        self.reset()

    def reset(self):
        """Reset/init the stat using the input method."""
        self.stats = {}

    def update(self):
        """Update core stats.

        Stats is a dict (with both physical and log cpu number) instead of a integer.
        """
        self.reset()
        if self.input_method == 'local':
            try:
                self.stats['phys'] = psutil.cpu_count(logical=False)
                self.stats['log'] = psutil.cpu_count()
            except NameError:
                self.reset()

        elif self.input_method == 'snmp':
            pass
        return self.stats