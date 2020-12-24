# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/fraoustin/Téléchargements/ocglances/tmp/ocglances/plugins/glances_quicklook.py
# Compiled at: 2017-02-11 10:25:25
"""Quicklook plugin."""
from ocglances.cpu_percent import cpu_percent
from ocglances.outputs.glances_bars import Bar
from ocglances.plugins.glances_plugin import GlancesPlugin
import ocglances.psutil as psutil
cpuinfo_tag = False
try:
    from cpuinfo import cpuinfo
except ImportError:
    pass
else:
    cpuinfo_tag = True

class Plugin(GlancesPlugin):
    """Glances quicklook plugin.

    'stats' is a dictionary.
    """

    def __init__(self, args=None):
        """Init the quicklook plugin."""
        super(Plugin, self).__init__(args=args)
        self.display_curse = True
        self.reset()

    def reset(self):
        """Reset/init the stats."""
        self.stats = {}

    @GlancesPlugin._check_decorator
    @GlancesPlugin._log_result_decorator
    def update(self):
        """Update quicklook stats using the input method."""
        self.reset()
        if self.input_method == 'local':
            self.stats['cpu'] = cpu_percent.get()
            self.stats['percpu'] = cpu_percent.get(percpu=True)
            self.stats['mem'] = psutil.virtual_memory().percent
            self.stats['swap'] = psutil.swap_memory().percent
        elif self.input_method == 'snmp':
            pass
        if cpuinfo_tag:
            cpu_info = cpuinfo.get_cpu_info()
            if cpu_info is not None:
                self.stats['cpu_name'] = cpu_info['brand']
                self.stats['cpu_hz_current'] = cpu_info['hz_actual_raw'][0]
                self.stats['cpu_hz'] = cpu_info['hz_advertised_raw'][0]
        return self.stats

    def update_views(self):
        """Update stats views."""
        super(Plugin, self).update_views()
        for key in ['cpu', 'mem', 'swap']:
            if key in self.stats:
                self.views[key]['decoration'] = self.get_alert(self.stats[key], header=key)

    def msg_curse(self, args=None, max_width=10):
        """Return the list to display in the UI."""
        ret = []
        if not self.stats or self.is_disable():
            return ret
        bar = Bar(max_width)
        if 'cpu_name' in self.stats and 'cpu_hz_current' in self.stats and 'cpu_hz' in self.stats:
            msg_name = ('{} - ').format(self.stats['cpu_name'])
            msg_freq = ('{:.2f}/{:.2f}GHz').format(self._hz_to_ghz(self.stats['cpu_hz_current']), self._hz_to_ghz(self.stats['cpu_hz']))
            if len(msg_name + msg_freq) - 6 <= max_width:
                ret.append(self.curse_add_line(msg_name))
            ret.append(self.curse_add_line(msg_freq))
            ret.append(self.curse_new_line())
        for key in ['cpu', 'mem', 'swap']:
            if key == 'cpu' and args.percpu:
                for cpu in self.stats['percpu']:
                    bar.percent = cpu['total']
                    if cpu[cpu['key']] < 10:
                        msg = ('{:3}{} ').format(key.upper(), cpu['cpu_number'])
                    else:
                        msg = ('{:4} ').format(cpu['cpu_number'])
                    ret.extend(self._msg_create_line(msg, bar, key))

            else:
                bar.percent = self.stats[key]
                msg = ('{:4} ').format(key.upper())
                ret.extend(self._msg_create_line(msg, bar, key))

        return ret

    def _msg_create_line(self, msg, bar, key):
        """Create a new line to the Quickview"""
        ret = []
        ret.append(self.curse_add_line(msg))
        ret.append(self.curse_add_line(bar.pre_char, decoration='BOLD'))
        ret.append(self.curse_add_line(str(bar), self.get_views(key=key, option='decoration')))
        ret.append(self.curse_add_line(bar.post_char, decoration='BOLD'))
        ret.append(self.curse_add_line('  '))
        ret.append(self.curse_new_line())
        return ret

    def _hz_to_ghz(self, hz):
        """Convert Hz to Ghz"""
        return hz / 1000000000.0