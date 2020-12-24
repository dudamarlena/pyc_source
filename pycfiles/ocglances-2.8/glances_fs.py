# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/fraoustin/Téléchargements/ocglances/tmp/ocglances/plugins/glances_fs.py
# Compiled at: 2017-02-11 10:25:25
"""File system plugin."""
import operator
from ocglances.plugins.glances_plugin import GlancesPlugin
import ocglances.psutil as psutil
snmp_oid = {'default': {'mnt_point': '1.3.6.1.4.1.2021.9.1.2', 'device_name': '1.3.6.1.4.1.2021.9.1.3', 
               'size': '1.3.6.1.4.1.2021.9.1.6', 
               'used': '1.3.6.1.4.1.2021.9.1.8', 
               'percent': '1.3.6.1.4.1.2021.9.1.9'}, 
   'windows': {'mnt_point': '1.3.6.1.2.1.25.2.3.1.3', 'alloc_unit': '1.3.6.1.2.1.25.2.3.1.4', 
               'size': '1.3.6.1.2.1.25.2.3.1.5', 
               'used': '1.3.6.1.2.1.25.2.3.1.6'}, 
   'netapp': {'mnt_point': '1.3.6.1.4.1.789.1.5.4.1.2', 'device_name': '1.3.6.1.4.1.789.1.5.4.1.10', 
              'size': '1.3.6.1.4.1.789.1.5.4.1.3', 
              'used': '1.3.6.1.4.1.789.1.5.4.1.4', 
              'percent': '1.3.6.1.4.1.789.1.5.4.1.6'}}
snmp_oid['esxi'] = snmp_oid['windows']
items_history_list = [
 {'name': 'percent', 'description': 'File system usage in percent', 
    'color': '#00FF00'}]

class Plugin(GlancesPlugin):
    """Glances file system plugin.

    stats is a list
    """

    def __init__(self, args=None):
        """Init the plugin."""
        super(Plugin, self).__init__(args=args, items_history_list=items_history_list)
        self.display_curse = True
        self.reset()

    def get_key(self):
        """Return the key of the list."""
        return 'mnt_point'

    def reset(self):
        """Reset/init the stats."""
        self.stats = []

    @GlancesPlugin._check_decorator
    @GlancesPlugin._log_result_decorator
    def update(self):
        """Update the FS stats using the input method."""
        self.reset()
        if self.input_method == 'local':
            try:
                fs_stat = psutil.disk_partitions(all=False)
            except UnicodeDecodeError:
                return self.stats

            for fstype in self.get_conf_value('allow'):
                try:
                    fs_stat += [ f for f in psutil.disk_partitions(all=True) if f.fstype.find(fstype) >= 0 ]
                except UnicodeDecodeError:
                    return self.stats

            for fs in fs_stat:
                if self.is_hide(fs.mountpoint):
                    continue
                try:
                    fs_usage = psutil.disk_usage(fs.mountpoint)
                except OSError:
                    continue

                fs_current = {'device_name': fs.device, 'fs_type': fs.fstype, 
                   'mnt_point': fs.mountpoint, 
                   'size': fs_usage.total, 
                   'used': fs_usage.used, 
                   'free': fs_usage.free, 
                   'percent': fs_usage.percent, 
                   'key': self.get_key()}
                self.stats.append(fs_current)

        elif self.input_method == 'snmp':
            try:
                fs_stat = self.get_stats_snmp(snmp_oid=snmp_oid[self.short_system_name], bulk=True)
            except KeyError:
                fs_stat = self.get_stats_snmp(snmp_oid=snmp_oid['default'], bulk=True)

            if self.short_system_name in ('windows', 'esxi'):
                for fs in fs_stat:
                    if fs == 'Virtual Memory' or fs == 'Physical Memory' or fs == 'Real Memory':
                        continue
                    size = int(fs_stat[fs]['size']) * int(fs_stat[fs]['alloc_unit'])
                    used = int(fs_stat[fs]['used']) * int(fs_stat[fs]['alloc_unit'])
                    percent = float(used * 100 / size)
                    fs_current = {'device_name': '', 
                       'mnt_point': fs.partition(' ')[0], 
                       'size': size, 
                       'used': used, 
                       'percent': percent, 
                       'key': self.get_key()}
                    self.stats.append(fs_current)

            else:
                for fs in fs_stat:
                    fs_current = {'device_name': fs_stat[fs]['device_name'], 
                       'mnt_point': fs, 
                       'size': int(fs_stat[fs]['size']) * 1024, 
                       'used': int(fs_stat[fs]['used']) * 1024, 
                       'percent': float(fs_stat[fs]['percent']), 
                       'key': self.get_key()}
                    self.stats.append(fs_current)

        return self.stats

    def update_views(self):
        """Update stats views."""
        super(Plugin, self).update_views()
        for i in self.stats:
            self.views[i[self.get_key()]]['used']['decoration'] = self.get_alert(i['used'], maximum=i['size'], header=i['mnt_point'])

    def msg_curse(self, args=None, max_width=None):
        """Return the dict to display in the curse interface."""
        ret = []
        if not self.stats or self.is_disable():
            return ret
        if max_width is not None and max_width >= 23:
            fsname_max_width = max_width - 14
        else:
            fsname_max_width = 9
        msg = ('{:{width}}').format('FILE SYS', width=fsname_max_width)
        ret.append(self.curse_add_line(msg, 'TITLE'))
        if args.fs_free_space:
            msg = ('{:>7}').format('Free')
        else:
            msg = ('{:>7}').format('Used')
        ret.append(self.curse_add_line(msg))
        msg = ('{:>7}').format('Total')
        ret.append(self.curse_add_line(msg))
        for i in sorted(self.stats, key=operator.itemgetter(self.get_key())):
            ret.append(self.curse_new_line())
            if i['device_name'] == '' or i['device_name'] == 'none':
                mnt_point = i['mnt_point'][-fsname_max_width + 1:]
            elif len(i['mnt_point']) + len(i['device_name'].split('/')[(-1)]) <= fsname_max_width - 3:
                mnt_point = i['mnt_point'] + ' (' + i['device_name'].split('/')[(-1)] + ')'
            elif len(i['mnt_point']) > fsname_max_width:
                mnt_point = '_' + i['mnt_point'][-fsname_max_width + 1:]
            else:
                mnt_point = i['mnt_point']
            msg = ('{:{width}}').format(mnt_point, width=fsname_max_width)
            ret.append(self.curse_add_line(msg))
            if args.fs_free_space:
                msg = ('{:>7}').format(self.auto_unit(i['free']))
            else:
                msg = ('{:>7}').format(self.auto_unit(i['used']))
            ret.append(self.curse_add_line(msg, self.get_views(item=i[self.get_key()], key='used', option='decoration')))
            msg = ('{:>7}').format(self.auto_unit(i['size']))
            ret.append(self.curse_add_line(msg))

        return ret