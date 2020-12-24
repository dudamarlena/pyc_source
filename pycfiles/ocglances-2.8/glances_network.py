# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/fraoustin/Téléchargements/ocglances/tmp/ocglances/plugins/glances_network.py
# Compiled at: 2017-02-11 10:25:25
"""Network plugin."""
import base64, operator
from ocglances.timer import getTimeSinceLastUpdate
from ocglances.plugins.glances_plugin import GlancesPlugin
import ocglances.psutil as psutil
snmp_oid = {'default': {'interface_name': '1.3.6.1.2.1.2.2.1.2', 'cumulative_rx': '1.3.6.1.2.1.2.2.1.10', 
               'cumulative_tx': '1.3.6.1.2.1.2.2.1.16'}}
items_history_list = [
 {'name': 'rx', 'description': 'Download rate per second', 
    'color': '#00FF00', 
    'y_unit': 'bit/s'},
 {'name': 'tx', 'description': 'Upload rate per second', 
    'color': '#FF0000', 
    'y_unit': 'bit/s'}]

class Plugin(GlancesPlugin):
    """Glances network plugin.

    stats is a list
    """

    def __init__(self, args=None):
        """Init the plugin."""
        super(Plugin, self).__init__(args=args, items_history_list=items_history_list)
        self.display_curse = True
        self.reset()

    def get_key(self):
        """Return the key of the list."""
        return 'interface_name'

    def reset(self):
        """Reset/init the stats."""
        self.stats = []

    @GlancesPlugin._check_decorator
    @GlancesPlugin._log_result_decorator
    def update(self):
        """Update network stats using the input method.

        Stats is a list of dict (one dict per interface)
        """
        self.reset()
        if self.input_method == 'local':
            try:
                netiocounters = psutil.net_io_counters(pernic=True)
            except UnicodeDecodeError:
                return self.stats

            netstatus = {}
            try:
                netstatus = psutil.net_if_stats()
            except AttributeError:
                pass

            if not hasattr(self, 'network_old'):
                try:
                    self.network_old = netiocounters
                except (IOError, UnboundLocalError):
                    pass

            else:
                time_since_update = getTimeSinceLastUpdate('net')
                network_new = netiocounters
                for net in network_new:
                    if self.is_hide(net):
                        continue
                    try:
                        cumulative_rx = network_new[net].bytes_recv
                        cumulative_tx = network_new[net].bytes_sent
                        cumulative_cx = cumulative_rx + cumulative_tx
                        rx = cumulative_rx - self.network_old[net].bytes_recv
                        tx = cumulative_tx - self.network_old[net].bytes_sent
                        cx = rx + tx
                        netstat = {'interface_name': net, 
                           'time_since_update': time_since_update, 
                           'cumulative_rx': cumulative_rx, 
                           'rx': rx, 
                           'cumulative_tx': cumulative_tx, 
                           'tx': tx, 
                           'cumulative_cx': cumulative_cx, 
                           'cx': cx}
                    except KeyError:
                        continue
                    else:
                        try:
                            netstat['is_up'] = netstatus[net].isup
                        except (KeyError, AttributeError):
                            pass

                        try:
                            netstat['speed'] = netstatus[net].speed * 1048576
                        except (KeyError, AttributeError):
                            pass

                        netstat['key'] = self.get_key()
                        self.stats.append(netstat)

                self.network_old = network_new
        elif self.input_method == 'snmp':
            try:
                netiocounters = self.get_stats_snmp(snmp_oid=snmp_oid[self.short_system_name], bulk=True)
            except KeyError:
                netiocounters = self.get_stats_snmp(snmp_oid=snmp_oid['default'], bulk=True)

            if not hasattr(self, 'network_old'):
                try:
                    self.network_old = netiocounters
                except (IOError, UnboundLocalError):
                    pass

            else:
                time_since_update = getTimeSinceLastUpdate('net')
                network_new = netiocounters
                for net in network_new:
                    if self.is_hide(net):
                        continue
                    try:
                        if self.short_system_name == 'windows':
                            try:
                                interface_name = str(base64.b16decode(net[2:-2].upper()))
                            except TypeError:
                                interface_name = net

                        else:
                            interface_name = net
                        cumulative_rx = float(network_new[net]['cumulative_rx'])
                        cumulative_tx = float(network_new[net]['cumulative_tx'])
                        cumulative_cx = cumulative_rx + cumulative_tx
                        rx = cumulative_rx - float(self.network_old[net]['cumulative_rx'])
                        tx = cumulative_tx - float(self.network_old[net]['cumulative_tx'])
                        cx = rx + tx
                        netstat = {'interface_name': interface_name, 
                           'time_since_update': time_since_update, 
                           'cumulative_rx': cumulative_rx, 
                           'rx': rx, 
                           'cumulative_tx': cumulative_tx, 
                           'tx': tx, 
                           'cumulative_cx': cumulative_cx, 
                           'cx': cx}
                    except KeyError:
                        continue
                    else:
                        netstat['key'] = self.get_key()
                        self.stats.append(netstat)

                self.network_old = network_new
        return self.stats

    def update_views(self):
        """Update stats views."""
        super(Plugin, self).update_views()
        for i in self.stats:
            ifrealname = i['interface_name'].split(':')[0]
            bps_rx = int(i['rx'] // i['time_since_update'] * 8)
            bps_tx = int(i['tx'] // i['time_since_update'] * 8)
            alert_rx = self.get_alert(bps_rx, header=ifrealname + '_rx')
            alert_tx = self.get_alert(bps_tx, header=ifrealname + '_tx')
            if alert_rx == 'DEFAULT' and 'speed' in i and i['speed'] != 0:
                alert_rx = self.get_alert(current=bps_rx, maximum=i['speed'], header='rx')
            if alert_tx == 'DEFAULT' and 'speed' in i and i['speed'] != 0:
                alert_tx = self.get_alert(current=bps_tx, maximum=i['speed'], header='tx')
            self.views[i[self.get_key()]]['rx']['decoration'] = alert_rx
            self.views[i[self.get_key()]]['tx']['decoration'] = alert_tx

    def msg_curse(self, args=None, max_width=None):
        """Return the dict to display in the curse interface."""
        ret = []
        if not self.stats or self.is_disable():
            return ret
        if max_width is not None and max_width >= 23:
            ifname_max_width = max_width - 14
        else:
            ifname_max_width = 9
        msg = ('{:{width}}').format('NETWORK', width=ifname_max_width)
        ret.append(self.curse_add_line(msg, 'TITLE'))
        if args.network_cumul:
            if args.network_sum:
                msg = ('{:>14}').format('Rx+Tx')
                ret.append(self.curse_add_line(msg))
            else:
                msg = ('{:>7}').format('Rx')
                ret.append(self.curse_add_line(msg))
                msg = ('{:>7}').format('Tx')
                ret.append(self.curse_add_line(msg))
        else:
            if args.network_sum:
                msg = ('{:>14}').format('Rx+Tx/s')
                ret.append(self.curse_add_line(msg))
            else:
                msg = ('{:>7}').format('Rx/s')
                ret.append(self.curse_add_line(msg))
                msg = ('{:>7}').format('Tx/s')
                ret.append(self.curse_add_line(msg))
            for i in sorted(self.stats, key=operator.itemgetter(self.get_key())):
                if 'is_up' in i and i['is_up'] is False:
                    continue
                ifrealname = i['interface_name'].split(':')[0]
                ifname = self.has_alias(i['interface_name'])
                if ifname is None:
                    ifname = ifrealname
                if len(ifname) > ifname_max_width:
                    ifname = '_' + ifname[-ifname_max_width + 1:]
                if args.byte:
                    to_bit = 1
                    unit = ''
                else:
                    to_bit = 8
                    unit = 'b'
                if args.network_cumul:
                    rx = self.auto_unit(int(i['cumulative_rx'] * to_bit)) + unit
                    tx = self.auto_unit(int(i['cumulative_tx'] * to_bit)) + unit
                    sx = self.auto_unit(int(i['cumulative_rx'] * to_bit) + int(i['cumulative_tx'] * to_bit)) + unit
                else:
                    rx = self.auto_unit(int(i['rx'] // i['time_since_update'] * to_bit)) + unit
                    tx = self.auto_unit(int(i['tx'] // i['time_since_update'] * to_bit)) + unit
                    sx = self.auto_unit(int(i['rx'] // i['time_since_update'] * to_bit) + int(i['tx'] // i['time_since_update'] * to_bit)) + unit
                ret.append(self.curse_new_line())
                msg = ('{:{width}}').format(ifname, width=ifname_max_width)
                ret.append(self.curse_add_line(msg))
                if args.network_sum:
                    msg = ('{:>14}').format(sx)
                    ret.append(self.curse_add_line(msg))
                else:
                    msg = ('{:>7}').format(rx)
                    ret.append(self.curse_add_line(msg, self.get_views(item=i[self.get_key()], key='rx', option='decoration')))
                    msg = ('{:>7}').format(tx)
                    ret.append(self.curse_add_line(msg, self.get_views(item=i[self.get_key()], key='tx', option='decoration')))

        return ret