# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/fraoustin/Téléchargements/ocglances/tmp/ocglances/plugins/glances_percpu.py
# Compiled at: 2017-02-11 10:25:25
"""Per-CPU plugin."""
from ocglances.cpu_percent import cpu_percent
from ocglances.plugins.glances_plugin import GlancesPlugin

class Plugin(GlancesPlugin):
    """Glances per-CPU plugin.

    'stats' is a list of dictionaries that contain the utilization percentages
    for each CPU.
    """

    def __init__(self, args=None):
        """Init the plugin."""
        super(Plugin, self).__init__(args=args)
        self.display_curse = True
        self.reset()

    def get_key(self):
        """Return the key of the list."""
        return 'cpu_number'

    def reset(self):
        """Reset/init the stats."""
        self.stats = []

    @GlancesPlugin._check_decorator
    @GlancesPlugin._log_result_decorator
    def update(self):
        """Update per-CPU stats using the input method."""
        self.reset()
        if self.input_method == 'local':
            self.stats = cpu_percent.get(percpu=True)
        return self.stats

    def msg_curse(self, args=None):
        """Return the dict to display in the curse interface."""
        ret = []
        if not self.stats:
            msg = 'PER CPU not available'
            ret.append(self.curse_add_line(msg, 'TITLE'))
            return ret
        msg = ('{:8}').format('PER CPU')
        ret.append(self.curse_add_line(msg, 'TITLE'))
        for cpu in self.stats:
            msg = ('{:>6}%').format(cpu['total'])
            ret.append(self.curse_add_line(msg))

        for stat in ['user', 'system', 'idle', 'iowait', 'steal']:
            if stat not in self.stats[0]:
                continue
            ret.append(self.curse_new_line())
            msg = ('{:8}').format(stat + ':')
            ret.append(self.curse_add_line(msg))
            for cpu in self.stats:
                msg = ('{:>6}%').format(cpu[stat])
                ret.append(self.curse_add_line(msg, self.get_alert(cpu[stat], header=stat)))

        return ret