# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/fraoustin/Téléchargements/ocglances/tmp/ocglances/plugins/glances_uptime.py
# Compiled at: 2017-02-11 10:25:25
"""Uptime plugin."""
from datetime import datetime, timedelta
from ocglances.plugins.glances_plugin import GlancesPlugin
import ocglances.psutil as psutil
snmp_oid = {'_uptime': '1.3.6.1.2.1.1.3.0'}

class Plugin(GlancesPlugin):
    """Glances uptime plugin.

    stats is date (string)
    """

    def __init__(self, args=None):
        """Init the plugin."""
        super(Plugin, self).__init__(args=args)
        self.display_curse = True
        self.align = 'right'
        self.uptime = datetime.now() - datetime.fromtimestamp(psutil.boot_time())
        self.reset()

    def reset(self):
        """Reset/init the stats."""
        self.stats = {}

    def get_export(self):
        """Overwrite the default export method.

        Export uptime in seconds.
        """
        return {'seconds': self.uptime.seconds}

    @GlancesPlugin._check_decorator
    @GlancesPlugin._log_result_decorator
    def update(self):
        """Update uptime stat using the input method."""
        self.reset()
        if self.input_method == 'local':
            self.uptime = datetime.now() - datetime.fromtimestamp(psutil.boot_time())
            self.stats = str(self.uptime).split('.')[0]
        elif self.input_method == 'snmp':
            uptime = self.get_stats_snmp(snmp_oid=snmp_oid)['_uptime']
            try:
                self.stats = str(timedelta(seconds=int(uptime) / 100))
            except Exception:
                pass

        return self.stats

    def msg_curse(self, args=None):
        """Return the string to display in the curse interface."""
        return [
         self.curse_add_line(('Uptime: {}').format(self.stats))]