# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/vsm/api/views/servers.py
# Compiled at: 2016-06-13 14:11:03
from vsm.api import common
import logging
LOG = logging.getLogger(__name__)

class ViewBuilder(common.ViewBuilder):
    _collection_name = 'servers'

    def basic(self, server):
        if not server['type']:
            server['type'] = ''
        return {'server': {'id': server['id'], 
                      'host': server['host'], 
                      'primary_public_ip': server['primary_public_ip'], 
                      'secondary_public_ip': server['secondary_public_ip'], 
                      'cluster_ip': server['cluster_ip'], 
                      'raw_ip': '192.168.1.3,192.168.2.3,192.168.3.3', 
                      'zone_id': server['zone_id'], 
                      'ceph_ver': server['ceph_ver'], 
                      'service_id': server['service_id'], 
                      'osds': server['data_drives_number'], 
                      'type': server['type'], 
                      'status': server['status']}}

    def index(self, servers):
        """Show a list of servers without many details."""
        return self._list_view(self.basic, servers)

    def _list_view(self, func, servers):
        """Provide a view for a list of servers."""
        server_list = [ func(server)['server'] for server in servers ]
        servers_dict = dict(servers=server_list)
        return servers_dict