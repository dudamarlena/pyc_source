# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/fraoustin/Téléchargements/ocglances/tmp/ocglances/plugins/glances_memswap.py
# Compiled at: 2017-02-11 10:25:25
"""Swap memory plugin."""
from ocglances.compat import iterkeys
from ocglances.plugins.glances_plugin import GlancesPlugin
import ocglances.psutil as psutil
snmp_oid = {'default': {'total': '1.3.6.1.4.1.2021.4.3.0', 'free': '1.3.6.1.4.1.2021.4.4.0'}, 
   'windows': {'mnt_point': '1.3.6.1.2.1.25.2.3.1.3', 'alloc_unit': '1.3.6.1.2.1.25.2.3.1.4', 
               'size': '1.3.6.1.2.1.25.2.3.1.5', 
               'used': '1.3.6.1.2.1.25.2.3.1.6'}}
items_history_list = [
 {'name': 'percent', 'description': 'Swap memory usage', 
    'color': '#00FF00', 
    'y_unit': '%'}]

class Plugin(GlancesPlugin):
    """Glances swap memory plugin.

    stats is a dict
    """

    def __init__(self, args=None):
        """Init the plugin."""
        super(Plugin, self).__init__(args=args, items_history_list=items_history_list)
        self.display_curse = True
        self.reset()

    def reset(self):
        """Reset/init the stats."""
        self.stats = {}

    @GlancesPlugin._check_decorator
    @GlancesPlugin._log_result_decorator
    def update(self):
        """Update swap memory stats using the input method."""
        self.reset()
        if self.input_method == 'local':
            sm_stats = psutil.swap_memory()
            for swap in ['total', 'used', 'free', 'percent',
             'sin', 'sout']:
                if hasattr(sm_stats, swap):
                    self.stats[swap] = getattr(sm_stats, swap)

        elif self.input_method == 'snmp':
            if self.short_system_name == 'windows':
                try:
                    fs_stat = self.get_stats_snmp(snmp_oid=snmp_oid[self.short_system_name], bulk=True)
                except KeyError:
                    self.reset()

                for fs in fs_stat:
                    if fs == 'Virtual Memory':
                        self.stats['total'] = int(fs_stat[fs]['size']) * int(fs_stat[fs]['alloc_unit'])
                        self.stats['used'] = int(fs_stat[fs]['used']) * int(fs_stat[fs]['alloc_unit'])
                        self.stats['percent'] = float(self.stats['used'] * 100 / self.stats['total'])
                        self.stats['free'] = self.stats['total'] - self.stats['used']
                        break

            else:
                self.stats = self.get_stats_snmp(snmp_oid=snmp_oid['default'])
                if self.stats['total'] == '':
                    self.reset()
                    return self.stats
                for key in iterkeys(self.stats):
                    if self.stats[key] != '':
                        self.stats[key] = float(self.stats[key]) * 1024

                self.stats['used'] = self.stats['total'] - self.stats['free']
                self.stats['percent'] = float((self.stats['total'] - self.stats['free']) / self.stats['total'] * 100)
        return self.stats

    def update_views(self):
        """Update stats views."""
        super(Plugin, self).update_views()
        self.views['used']['decoration'] = self.get_alert_log(self.stats['used'], maximum=self.stats['total'])

    def msg_curse(self, args=None):
        """Return the dict to display in the curse interface."""
        ret = []
        if not self.stats or self.is_disable():
            return ret
        msg = ('{:7} ').format('SWAP')
        ret.append(self.curse_add_line(msg, 'TITLE'))
        msg = ('{:>6.1%}').format(self.stats['percent'] / 100)
        ret.append(self.curse_add_line(msg))
        ret.append(self.curse_new_line())
        msg = ('{:8}').format('total:')
        ret.append(self.curse_add_line(msg))
        msg = ('{:>6}').format(self.auto_unit(self.stats['total']))
        ret.append(self.curse_add_line(msg))
        ret.append(self.curse_new_line())
        msg = ('{:8}').format('used:')
        ret.append(self.curse_add_line(msg))
        msg = ('{:>6}').format(self.auto_unit(self.stats['used']))
        ret.append(self.curse_add_line(msg, self.get_views(key='used', option='decoration')))
        ret.append(self.curse_new_line())
        msg = ('{:8}').format('free:')
        ret.append(self.curse_add_line(msg))
        msg = ('{:>6}').format(self.auto_unit(self.stats['free']))
        ret.append(self.curse_add_line(msg))
        return ret