# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/vsm/api/views/devices.py
# Compiled at: 2016-06-13 14:11:03
from vsm.api import common
import logging
LOG = logging.getLogger(__name__)

class ViewBuilder(common.ViewBuilder):
    _collection_name = 'devices'

    def basic(self, request, device):
        return {'device': {'id': device['id'], 
                      'name': device['name'], 
                      'path': device['path'], 
                      'journal': device['journal'], 
                      'device_type': device['device_type'], 
                      'state': device['state'], 
                      'journal_state': device['journal_state'], 
                      'total_capacity_kb': device['total_capacity_kb'], 
                      'avail_capacity_kb': device['avail_capacity_kb'], 
                      'used_capacity_kb': device['used_capacity_kb']}}

    def index(self, request, devices):
        """Show a list of devices without many details."""
        return self._list_view(self.basic, request, devices)

    def _list_view(self, func, request, devices):
        """Provide a view for a list of devices."""
        device_list = [ func(request, device)['device'] for device in devices ]
        devices_dict = dict(devices=device_list)
        LOG.info('---devices_dict---%s' % devices_dict)
        return devices_dict