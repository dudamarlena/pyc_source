# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/fraoustin/Téléchargements/ocglances/tmp/ocglances/plugins/glances_wifi.py
# Compiled at: 2017-02-11 10:25:25
"""Wifi plugin."""
import operator
from ocglances.logger import logger
from ocglances.plugins.glances_plugin import GlancesPlugin
import ocglances.psutil as psutil
try:
    from wifi.scan import Cell
    from wifi.exceptions import InterfaceError
except ImportError:
    logger.debug('Wifi library not found. Glances cannot grab Wifi info.')
    wifi_tag = False
else:
    wifi_tag = True

class Plugin(GlancesPlugin):
    """Glances Wifi plugin.
    Get stats of the current Wifi hotspots.
    """

    def __init__(self, args=None):
        """Init the plugin."""
        super(Plugin, self).__init__(args=args)
        self.display_curse = True
        self.reset()

    def get_key(self):
        """Return the key of the list.

        :returns: string -- SSID is the dict key
        """
        return 'ssid'

    def reset(self):
        """Reset/init the stats to an empty list.

        :returns: None
        """
        self.stats = []

    @GlancesPlugin._check_decorator
    @GlancesPlugin._log_result_decorator
    def update(self):
        """Update Wifi stats using the input method.

        Stats is a list of dict (one dict per hotspot)

        :returns: list -- Stats is a list of dict (hotspot)
        """
        self.reset()
        if not wifi_tag:
            return self.stats
        else:
            if self.input_method == 'local':
                try:
                    netiocounters = psutil.net_io_counters(pernic=True)
                except UnicodeDecodeError:
                    return self.stats

                for net in netiocounters:
                    if self.is_hide(net):
                        continue
                    try:
                        wifi_cells = Cell.all(net)
                    except InterfaceError:
                        pass
                    except Exception as e:
                        logger.debug(('WIFI plugin: Can not grab cellule stats ({})').format(e))

                    for wifi_cell in wifi_cells:
                        hotspot = {'key': self.get_key(), 
                           'ssid': wifi_cell.ssid, 
                           'signal': wifi_cell.signal, 
                           'quality': wifi_cell.quality, 
                           'encrypted': wifi_cell.encrypted, 
                           'encryption_type': wifi_cell.encryption_type if wifi_cell.encrypted else None}
                        self.stats.append(hotspot)

            elif self.input_method == 'snmp':
                pass
            return self.stats

    def get_alert(self, value):
        """Overwrite the default get_alert method.
        Alert is on signal quality where lower is better...

        :returns: string -- Signal alert
        """
        ret = 'OK'
        try:
            if value <= self.get_limit('critical', stat_name=self.plugin_name):
                ret = 'CRITICAL'
            elif value <= self.get_limit('warning', stat_name=self.plugin_name):
                ret = 'WARNING'
            elif value <= self.get_limit('careful', stat_name=self.plugin_name):
                ret = 'CAREFUL'
        except KeyError:
            ret = 'DEFAULT'

        return ret

    def update_views(self):
        """Update stats views."""
        super(Plugin, self).update_views()
        for i in self.stats:
            self.views[i[self.get_key()]]['signal']['decoration'] = self.get_alert(i['signal'])
            self.views[i[self.get_key()]]['quality']['decoration'] = self.views[i[self.get_key()]]['signal']['decoration']

    def msg_curse(self, args=None, max_width=None):
        """Return the dict to display in the curse interface."""
        ret = []
        if not self.stats or args.disable_wifi or not wifi_tag:
            return ret
        if max_width is not None and max_width >= 23:
            ifname_max_width = max_width - 5
        else:
            ifname_max_width = 16
        msg = ('{:{width}}').format('WIFI', width=ifname_max_width)
        ret.append(self.curse_add_line(msg, 'TITLE'))
        msg = ('{:>7}').format('dBm')
        ret.append(self.curse_add_line(msg))
        for i in sorted(self.stats, key=operator.itemgetter(self.get_key())):
            if i['ssid'] == '':
                continue
            ret.append(self.curse_new_line())
            hotspotname = i['ssid']
            if i['encrypted']:
                hotspotname += (' {}').format(i['encryption_type'])
            if len(hotspotname) > ifname_max_width:
                hotspotname = '_' + hotspotname[-ifname_max_width + 1:]
            msg = ('{:{width}}').format(hotspotname, width=ifname_max_width)
            ret.append(self.curse_add_line(msg))
            msg = ('{:>7}').format(i['signal'], width=ifname_max_width)
            ret.append(self.curse_add_line(msg, self.get_views(item=i[self.get_key()], key='signal', option='decoration')))

        return ret