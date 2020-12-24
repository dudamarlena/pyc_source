# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/fraoustin/Téléchargements/ocglances/tmp/ocglances/plugins/glances_cpu.py
# Compiled at: 2017-02-11 10:25:25
"""CPU plugin."""
from ocglances.timer import getTimeSinceLastUpdate
from ocglances.compat import iterkeys
from ocglances.cpu_percent import cpu_percent
from ocglances.globals import LINUX
from ocglances.plugins.glances_core import Plugin as CorePlugin
from ocglances.plugins.glances_plugin import GlancesPlugin
import ocglances.psutil as psutil
snmp_oid = {'default': {'user': '1.3.6.1.4.1.2021.11.9.0', 'system': '1.3.6.1.4.1.2021.11.10.0', 
               'idle': '1.3.6.1.4.1.2021.11.11.0'}, 
   'windows': {'percent': '1.3.6.1.2.1.25.3.3.1.2'}, 'esxi': {'percent': '1.3.6.1.2.1.25.3.3.1.2'}, 'netapp': {'system': '1.3.6.1.4.1.789.1.2.1.3.0', 'idle': '1.3.6.1.4.1.789.1.2.1.5.0', 
              'nb_log_core': '1.3.6.1.4.1.789.1.2.1.6.0'}}
items_history_list = [
 {'name': 'user', 'description': 'User CPU usage', 
    'color': '#00FF00', 
    'y_unit': '%'},
 {'name': 'system', 'description': 'System CPU usage', 
    'color': '#FF0000', 
    'y_unit': '%'}]

class Plugin(GlancesPlugin):
    """Glances CPU plugin.

    'stats' is a dictionary that contains the system-wide CPU utilization as a
    percentage.
    """

    def __init__(self, args=None):
        """Init the CPU plugin."""
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
        """Update CPU stats using the input method."""
        self.reset()
        if self.input_method == 'local':
            self.update_local()
        elif self.input_method == 'snmp':
            self.update_snmp()
        return self.stats

    def update_local(self):
        """Update CPU stats using PSUtil."""
        self.stats['total'] = cpu_percent.get()
        cpu_times_percent = psutil.cpu_times_percent(interval=0.0)
        for stat in ['user', 'system', 'idle', 'nice', 'iowait',
         'irq', 'softirq', 'steal', 'guest', 'guest_nice']:
            if hasattr(cpu_times_percent, stat):
                self.stats[stat] = getattr(cpu_times_percent, stat)

        try:
            cpu_stats = psutil.cpu_stats()
        except AttributeError:
            pass

        time_since_update = getTimeSinceLastUpdate('cpu')
        if not hasattr(self, 'cpu_stats_old'):
            self.cpu_stats_old = cpu_stats
        else:
            for stat in cpu_stats._fields:
                if getattr(cpu_stats, stat) is not None:
                    self.stats[stat] = getattr(cpu_stats, stat) - getattr(self.cpu_stats_old, stat)

            self.stats['time_since_update'] = time_since_update
            self.stats['cpucore'] = self.nb_log_core
            self.cpu_stats_old = cpu_stats
        return

    def update_snmp(self):
        """Update CPU stats using SNMP."""
        if self.short_system_name in ('windows', 'esxi'):
            try:
                cpu_stats = self.get_stats_snmp(snmp_oid=snmp_oid[self.short_system_name], bulk=True)
            except KeyError:
                self.reset()

            self.stats['nb_log_core'] = 0
            self.stats['idle'] = 0
            for c in cpu_stats:
                if c.startswith('percent'):
                    self.stats['idle'] += float(cpu_stats['percent.3'])
                    self.stats['nb_log_core'] += 1

            if self.stats['nb_log_core'] > 0:
                self.stats['idle'] = self.stats['idle'] / self.stats['nb_log_core']
            self.stats['idle'] = 100 - self.stats['idle']
            self.stats['total'] = 100 - self.stats['idle']
        else:
            try:
                self.stats = self.get_stats_snmp(snmp_oid=snmp_oid[self.short_system_name])
            except KeyError:
                self.stats = self.get_stats_snmp(snmp_oid=snmp_oid['default'])

            if self.stats['idle'] == '':
                self.reset()
                return self.stats
            for key in iterkeys(self.stats):
                self.stats[key] = float(self.stats[key])

            self.stats['total'] = 100 - self.stats['idle']

    def update_views(self):
        """Update stats views."""
        super(Plugin, self).update_views()
        for key in ['user', 'system', 'iowait']:
            if key in self.stats:
                self.views[key]['decoration'] = self.get_alert_log(self.stats[key], header=key)

        for key in ['steal', 'total']:
            if key in self.stats:
                self.views[key]['decoration'] = self.get_alert(self.stats[key], header=key)

        for key in ['ctx_switches']:
            if key in self.stats:
                self.views[key]['decoration'] = self.get_alert(self.stats[key], maximum=100 * self.stats['cpucore'], header=key)

        for key in ['nice', 'irq', 'iowait', 'steal', 'ctx_switches', 'interrupts', 'soft_interrupts', 'syscalls']:
            if key in self.stats:
                self.views[key]['optional'] = True

    def msg_curse(self, args=None):
        """Return the list to display in the UI."""
        ret = []
        if not self.stats or self.is_disable():
            return ret
        idle_tag = 'user' not in self.stats
        msg = ('{:8}').format('CPU')
        ret.append(self.curse_add_line(msg, 'TITLE'))
        msg = ('{:>5}%').format(self.stats['total'])
        if idle_tag:
            ret.append(self.curse_add_line(msg, self.get_views(key='total', option='decoration')))
        else:
            ret.append(self.curse_add_line(msg))
        if 'nice' in self.stats:
            msg = ('  {:8}').format('nice:')
            ret.append(self.curse_add_line(msg, optional=self.get_views(key='nice', option='optional')))
            msg = ('{:>5}%').format(self.stats['nice'])
            ret.append(self.curse_add_line(msg, optional=self.get_views(key='nice', option='optional')))
        if 'ctx_switches' in self.stats:
            msg = ('  {:8}').format('ctx_sw:')
            ret.append(self.curse_add_line(msg, optional=self.get_views(key='ctx_switches', option='optional')))
            msg = ('{:>5}').format(int(self.stats['ctx_switches'] // self.stats['time_since_update']))
            ret.append(self.curse_add_line(msg, self.get_views(key='ctx_switches', option='decoration'), optional=self.get_views(key='ctx_switches', option='optional')))
        ret.append(self.curse_new_line())
        if 'user' in self.stats:
            msg = ('{:8}').format('user:')
            ret.append(self.curse_add_line(msg))
            msg = ('{:>5}%').format(self.stats['user'])
            ret.append(self.curse_add_line(msg, self.get_views(key='user', option='decoration')))
        elif 'idle' in self.stats:
            msg = ('{:8}').format('idle:')
            ret.append(self.curse_add_line(msg))
            msg = ('{:>5}%').format(self.stats['idle'])
            ret.append(self.curse_add_line(msg))
        if 'irq' in self.stats:
            msg = ('  {:8}').format('irq:')
            ret.append(self.curse_add_line(msg, optional=self.get_views(key='irq', option='optional')))
            msg = ('{:>5}%').format(self.stats['irq'])
            ret.append(self.curse_add_line(msg, optional=self.get_views(key='irq', option='optional')))
        if 'interrupts' in self.stats:
            msg = ('  {:8}').format('inter:')
            ret.append(self.curse_add_line(msg, optional=self.get_views(key='interrupts', option='optional')))
            msg = ('{:>5}').format(int(self.stats['interrupts'] // self.stats['time_since_update']))
            ret.append(self.curse_add_line(msg, optional=self.get_views(key='interrupts', option='optional')))
        ret.append(self.curse_new_line())
        if 'system' in self.stats and not idle_tag:
            msg = ('{:8}').format('system:')
            ret.append(self.curse_add_line(msg))
            msg = ('{:>5}%').format(self.stats['system'])
            ret.append(self.curse_add_line(msg, self.get_views(key='system', option='decoration')))
        else:
            msg = ('{:8}').format('core:')
            ret.append(self.curse_add_line(msg))
            msg = ('{:>6}').format(self.stats['nb_log_core'])
            ret.append(self.curse_add_line(msg))
        if 'iowait' in self.stats:
            msg = ('  {:8}').format('iowait:')
            ret.append(self.curse_add_line(msg, optional=self.get_views(key='iowait', option='optional')))
            msg = ('{:>5}%').format(self.stats['iowait'])
            ret.append(self.curse_add_line(msg, self.get_views(key='iowait', option='decoration'), optional=self.get_views(key='iowait', option='optional')))
        if 'soft_interrupts' in self.stats:
            msg = ('  {:8}').format('sw_int:')
            ret.append(self.curse_add_line(msg, optional=self.get_views(key='soft_interrupts', option='optional')))
            msg = ('{:>5}').format(int(self.stats['soft_interrupts'] // self.stats['time_since_update']))
            ret.append(self.curse_add_line(msg, optional=self.get_views(key='soft_interrupts', option='optional')))
        ret.append(self.curse_new_line())
        if 'idle' in self.stats and not idle_tag:
            msg = ('{:8}').format('idle:')
            ret.append(self.curse_add_line(msg))
            msg = ('{:>5}%').format(self.stats['idle'])
            ret.append(self.curse_add_line(msg))
        if 'steal' in self.stats:
            msg = ('  {:8}').format('steal:')
            ret.append(self.curse_add_line(msg, optional=self.get_views(key='steal', option='optional')))
            msg = ('{:>5}%').format(self.stats['steal'])
            ret.append(self.curse_add_line(msg, self.get_views(key='steal', option='decoration'), optional=self.get_views(key='steal', option='optional')))
        if 'syscalls' in self.stats and not LINUX:
            msg = ('  {:8}').format('syscal:')
            ret.append(self.curse_add_line(msg, optional=self.get_views(key='syscalls', option='optional')))
            msg = ('{:>5}').format(int(self.stats['syscalls'] // self.stats['time_since_update']))
            ret.append(self.curse_add_line(msg, optional=self.get_views(key='syscalls', option='optional')))
        return ret