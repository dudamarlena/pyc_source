# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/vsm/api/views/zones.py
# Compiled at: 2016-06-13 14:11:03
from vsm.api import common
import logging
LOG = logging.getLogger(__name__)

class ViewBuilder(common.ViewBuilder):
    _collection_name = 'zones'

    def basic(self, zone):
        return {'zone': {'id': zone['id'], 
                    'name': zone['name']}}

    def index(self, zones):
        """Show a list of servers without many details."""
        return self._list_view(self.basic, zones)

    def _list_view(self, func, zones):
        """Provide a view for a list of servers."""
        zone_list = [ func(zone)['zone'] for zone in zones ]
        zones_dict = dict(zones=zone_list)
        return zones_dict