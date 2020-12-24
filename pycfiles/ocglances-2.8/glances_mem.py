# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/fraoustin/Téléchargements/ocglances/tmp/ocglances/plugins/glances_mem.py
# Compiled at: 2017-02-11 10:25:25
"""Virtual memory plugin."""
from ocglances.compat import iterkeys
from ocglances.plugins.glances_plugin import GlancesPlugin
import ocglances.psutil as psutil
snmp_oid = {'default': {'total': '1.3.6.1.4.1.2021.4.5.0', 'free': '1.3.6.1.4.1.2021.4.11.0', 
               'shared': '1.3.6.1.4.1.2021.4.13.0', 
               'buffers': '1.3.6.1.4.1.2021.4.14.0', 
               'cached': '1.3.6.1.4.1.2021.4.15.0'}, 
   'windows': {'mnt_point': '1.3.6.1.2.1.25.2.3.1.3', 'alloc_unit': '1.3.6.1.2.1.25.2.3.1.4', 
               'size': '1.3.6.1.2.1.25.2.3.1.5', 
               'used': '1.3.6.1.2.1.25.2.3.1.6'}, 
   'esxi': {'mnt_point': '1.3.6.1.2.1.25.2.3.1.3', 'alloc_unit': '1.3.6.1.2.1.25.2.3.1.4', 
            'size': '1.3.6.1.2.1.25.2.3.1.5', 
            'used': '1.3.6.1.2.1.25.2.3.1.6'}}
items_history_list = [
 {'name': 'percent', 'description': 'RAM memory usage', 
    'color': '#00FF00', 
    'y_unit': '%'}]

class Plugin(GlancesPlugin):
    """Glances' memory plugin.

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
        """Update RAM memory stats using the input method."""
        self.reset()
        if self.input_method == 'local':
            vm_stats = psutil.virtual_memory()
            self.reset()
            for mem in ['total', 'available', 'percent', 'used', 'free',
             'active', 'inactive', 'buffers', 'cached',
             'wired', 'shared']:
                if hasattr(vm_stats, mem):
                    self.stats[mem] = getattr(vm_stats, mem)

            self.stats['free'] = self.stats['available']
            if hasattr(self.stats, 'buffers'):
                self.stats['free'] += self.stats['buffers']
            if hasattr(self.stats, 'cached'):
                self.stats['free'] += self.stats['cached']
            self.stats['used'] = self.stats['total'] - self.stats['free']
        elif self.input_method == 'snmp':
            if self.short_system_name in ('windows', 'esxi'):
                try:
                    fs_stat = self.get_stats_snmp(snmp_oid=snmp_oid[self.short_system_name], bulk=True)
                except KeyError:
                    self.reset()

                for fs in fs_stat:
                    if fs in ('Physical Memory', 'Real Memory'):
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

                self.stats['free'] = self.stats['free'] - self.stats['total'] + (self.stats['buffers'] + self.stats['cached'])
                self.stats['used'] = self.stats['total'] - self.stats['free']
                self.stats['percent'] = float((self.stats['total'] - self.stats['free']) / self.stats['total'] * 100)
        return self.stats

    def update_views(self):
        """Update stats views."""
        super(Plugin, self).update_views()
        self.views['used']['decoration'] = self.get_alert_log(self.stats['used'], maximum=self.stats['total'])
        for key in ['active', 'inactive', 'buffers', 'cached']:
            if key in self.stats:
                self.views[key]['optional'] = True

    def msg_curse(self, args=None):
        """Return the dict to display in the curse interface."""
        ret = []
        if not self.stats or self.is_disable():
            return ret
        msg = ('{:5} ').format('MEM')
        ret.append(self.curse_add_line(msg, 'TITLE'))
        msg = ('{:>7.1%}').format(self.stats['percent'] / 100)
        ret.append(self.curse_add_line(msg))
        if 'active' in self.stats:
            msg = ('  {:9}').format('active:')
            ret.append(self.curse_add_line(msg, optional=self.get_views(key='active', option='optional')))
            msg = ('{:>7}').format(self.auto_unit(self.stats['active']))
            ret.append(self.curse_add_line(msg, optional=self.get_views(key='active', option='optional')))
        ret.append(self.curse_new_line())
        msg = ('{:6}').format('total:')
        ret.append(self.curse_add_line(msg))
        msg = ('{:>7}').format(self.auto_unit(self.stats['total']))
        ret.append(self.curse_add_line(msg))
        if 'inactive' in self.stats:
            msg = ('  {:9}').format('inactive:')
            ret.append(self.curse_add_line(msg, optional=self.get_views(key='inactive', option='optional')))
            msg = ('{:>7}').format(self.auto_unit(self.stats['inactive']))
            ret.append(self.curse_add_line(msg, optional=self.get_views(key='inactive', option='optional')))
        ret.append(self.curse_new_line())
        msg = ('{:6}').format('used:')
        ret.append(self.curse_add_line(msg))
        msg = ('{:>7}').format(self.auto_unit(self.stats['used']))
        ret.append(self.curse_add_line(msg, self.get_views(key='used', option='decoration')))
        if 'buffers' in self.stats:
            msg = ('  {:9}').format('buffers:')
            ret.append(self.curse_add_line(msg, optional=self.get_views(key='buffers', option='optional')))
            msg = ('{:>7}').format(self.auto_unit(self.stats['buffers']))
            ret.append(self.curse_add_line(msg, optional=self.get_views(key='buffers', option='optional')))
        ret.append(self.curse_new_line())
        msg = ('{:6}').format('free:')
        ret.append(self.curse_add_line(msg))
        msg = ('{:>7}').format(self.auto_unit(self.stats['free']))
        ret.append(self.curse_add_line(msg))
        if 'cached' in self.stats:
            msg = ('  {:9}').format('cached:')
            ret.append(self.curse_add_line(msg, optional=self.get_views(key='cached', option='optional')))
            msg = ('{:>7}').format(self.auto_unit(self.stats['cached']))
            ret.append(self.curse_add_line(msg, optional=self.get_views(key='cached', option='optional')))
        return ret