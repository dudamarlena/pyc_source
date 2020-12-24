# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/fraoustin/Téléchargements/ocglances/tmp/ocglances/plugins/glances_batpercent.py
# Compiled at: 2017-02-11 10:25:25
"""Battery plugin."""
from ocglances.logger import logger
from ocglances.plugins.glances_plugin import GlancesPlugin
try:
    import batinfo
except ImportError:
    logger.debug('Batinfo library not found. Glances cannot grab battery info.')

class Plugin(GlancesPlugin):
    """Glances battery capacity plugin.

    stats is a list
    """

    def __init__(self, args=None):
        """Init the plugin."""
        super(Plugin, self).__init__(args=args)
        self.glancesgrabbat = GlancesGrabBat()
        self.display_curse = False
        self.reset()

    def reset(self):
        """Reset/init the stats."""
        self.stats = []

    @GlancesPlugin._check_decorator
    @GlancesPlugin._log_result_decorator
    def update(self):
        """Update battery capacity stats using the input method."""
        self.reset()
        if self.input_method == 'local':
            self.glancesgrabbat.update()
            self.stats = self.glancesgrabbat.get()
        elif self.input_method == 'snmp':
            pass
        return self.stats


class GlancesGrabBat(object):
    """Get batteries stats using the batinfo library."""

    def __init__(self):
        """Init batteries stats."""
        try:
            self.bat = batinfo.batteries()
            self.initok = True
            self.bat_list = []
            self.update()
        except Exception as e:
            self.initok = False
            logger.debug('Cannot init GlancesGrabBat class (%s)' % e)

    def update(self):
        """Update the stats."""
        if self.initok:
            self.bat.update()
            self.bat_list = [
             {'label': 'Battery', 
                'value': self.battery_percent, 
                'unit': '%'}]
        else:
            self.bat_list = []

    def get(self):
        """Get the stats."""
        return self.bat_list

    @property
    def battery_percent(self):
        """Get batteries capacity percent."""
        if not self.initok or not self.bat.stat:
            return []
        bsum = 0
        for b in self.bat.stat:
            try:
                bsum += int(b.capacity)
            except ValueError:
                return []

        return int(bsum / len(self.bat.stat))