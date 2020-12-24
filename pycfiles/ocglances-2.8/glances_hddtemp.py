# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/fraoustin/Téléchargements/ocglances/tmp/ocglances/plugins/glances_hddtemp.py
# Compiled at: 2017-02-11 10:25:25
"""HDD temperature plugin."""
import os, socket
from ocglances.compat import nativestr, range
from ocglances.logger import logger
from ocglances.plugins.glances_plugin import GlancesPlugin

class Plugin(GlancesPlugin):
    """Glances HDD temperature sensors plugin.

    stats is a list
    """

    def __init__(self, args=None):
        """Init the plugin."""
        super(Plugin, self).__init__(args=args)
        self.glancesgrabhddtemp = GlancesGrabHDDTemp(args=args)
        self.display_curse = False
        self.reset()

    def reset(self):
        """Reset/init the stats."""
        self.stats = []

    @GlancesPlugin._check_decorator
    @GlancesPlugin._log_result_decorator
    def update(self):
        """Update HDD stats using the input method."""
        self.reset()
        if self.input_method == 'local':
            self.stats = self.glancesgrabhddtemp.get()
        return self.stats


class GlancesGrabHDDTemp(object):
    """Get hddtemp stats using a socket connection."""

    def __init__(self, host='127.0.0.1', port=7634, args=None):
        """Init hddtemp stats."""
        self.args = args
        self.host = host
        self.port = port
        self.cache = ''
        self.reset()

    def reset(self):
        """Reset/init the stats."""
        self.hddtemp_list = []

    def __update__(self):
        """Update the stats."""
        self.reset()
        data = self.fetch()
        if data == '':
            return
        if len(data) < 14:
            data = self.cache if len(self.cache) > 0 else self.fetch()
        self.cache = data
        try:
            fields = data.split('|')
        except TypeError:
            fields = ''

        devices = (len(fields) - 1) // 5
        for item in range(devices):
            offset = item * 5
            hddtemp_current = {}
            device = os.path.basename(nativestr(fields[(offset + 1)]))
            temperature = fields[(offset + 3)]
            unit = nativestr(fields[(offset + 4)])
            hddtemp_current['label'] = device
            try:
                hddtemp_current['value'] = float(temperature)
            except ValueError:
                hddtemp_current['value'] = nativestr(temperature)

            hddtemp_current['unit'] = unit
            self.hddtemp_list.append(hddtemp_current)

    def fetch(self):
        """Fetch the data from hddtemp daemon."""
        try:
            try:
                sck = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sck.connect((self.host, self.port))
                data = sck.recv(4096)
            except socket.error as e:
                logger.debug(('Cannot connect to an HDDtemp server ({}:{} => {})').format(self.host, self.port, e))
                logger.debug('Disable the HDDtemp module. Use the --disable-hddtemp to hide the previous message.')
                if self.args is not None:
                    self.args.disable_hddtemp = True
                data = ''

        finally:
            sck.close()

        return data

    def get(self):
        """Get HDDs list."""
        self.__update__()
        return self.hddtemp_list