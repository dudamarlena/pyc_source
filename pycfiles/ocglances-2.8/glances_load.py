# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/fraoustin/Téléchargements/ocglances/tmp/ocglances/plugins/glances_load.py
# Compiled at: 2017-02-11 10:25:25
"""Load plugin."""
import os
from ocglances.compat import iteritems
from ocglances.plugins.glances_core import Plugin as CorePlugin
from ocglances.plugins.glances_plugin import GlancesPlugin
snmp_oid = {'min1': '1.3.6.1.4.1.2021.10.1.3.1', 'min5': '1.3.6.1.4.1.2021.10.1.3.2', 
   'min15': '1.3.6.1.4.1.2021.10.1.3.3'}
items_history_list = [
 {'name': 'min1', 'description': '1 minute load', 
    'color': '#0000FF'},
 {'name': 'min5', 'description': '5 minutes load', 
    'color': '#0000AA'},
 {'name': 'min15', 'description': '15 minutes load', 
    'color': '#000044'}]

class Plugin(GlancesPlugin):
    """Glances load plugin.

    stats is a dict
    """

    def __init__(self, args=None):
        """Init the plugin."""
        super(Plugin, self).__init__(args=args, items_history_list=items_history_list)
        self.display_curse = True
        self.reset()
        try:
            self.nb_log_core = CorePlugin(args=self.args).update()['log']
        except Exception:
            self.nb_log_core = 1

    def reset(self):
        """Reset/init the stats."""
        self.stats = {}

    @GlancesPlugin._check_decorator
    @GlancesPlugin._log_result_decorator
    def update(self):
        """Update load stats."""
        self.reset()
        if self.input_method == 'local':
            try:
                load = os.getloadavg()
            except (OSError, AttributeError):
                self.stats = {}
            else:
                self.stats = {'min1': load[0], 'min5': load[1], 
                   'min15': load[2], 
                   'cpucore': self.nb_log_core}

        elif self.input_method == 'snmp':
            self.stats = self.get_stats_snmp(snmp_oid=snmp_oid)
            if self.stats['min1'] == '':
                self.reset()
                return self.stats
            for k, v in iteritems(self.stats):
                self.stats[k] = float(v)

            self.stats['cpucore'] = self.nb_log_core
        return self.stats

    def update_views(self):
        """Update stats views."""
        super(Plugin, self).update_views()
        try:
            self.views['min15']['decoration'] = self.get_alert_log(self.stats['min15'], maximum=100 * self.stats['cpucore'])
            self.views['min5']['decoration'] = self.get_alert(self.stats['min5'], maximum=100 * self.stats['cpucore'])
        except KeyError:
            pass

    def msg_curse(self, args=None):
        """Return the dict to display in the curse interface."""
        ret = []
        if not self.stats or self.stats == {} or self.is_disable():
            return ret
        msg = ('{:8}').format('LOAD')
        ret.append(self.curse_add_line(msg, 'TITLE'))
        if 'cpucore' in self.stats and self.stats['cpucore'] > 0:
            msg = ('{}-core').format(int(self.stats['cpucore']))
            ret.append(self.curse_add_line(msg))
        ret.append(self.curse_new_line())
        msg = ('{:8}').format('1 min:')
        ret.append(self.curse_add_line(msg))
        msg = ('{:>6.2f}').format(self.stats['min1'])
        ret.append(self.curse_add_line(msg))
        ret.append(self.curse_new_line())
        msg = ('{:8}').format('5 min:')
        ret.append(self.curse_add_line(msg))
        msg = ('{:>6.2f}').format(self.stats['min5'])
        ret.append(self.curse_add_line(msg, self.get_views(key='min5', option='decoration')))
        ret.append(self.curse_new_line())
        msg = ('{:8}').format('15 min:')
        ret.append(self.curse_add_line(msg))
        msg = ('{:>6.2f}').format(self.stats['min15'])
        ret.append(self.curse_add_line(msg, self.get_views(key='min15', option='decoration')))
        return ret