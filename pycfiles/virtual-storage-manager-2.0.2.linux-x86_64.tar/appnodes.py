# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/vsm/api/views/appnodes.py
# Compiled at: 2016-06-13 14:11:03
from vsm.api import common
import logging
LOG = logging.getLogger(__name__)

class ViewBuilder(common.ViewBuilder):
    _collection_name = 'appnodes'

    def basic(self, appnode):
        if not appnode.get('id', ''):
            appnode['id'] = ''
            return appnode
        return {'appnode': {'id': appnode.get('id', 0), 
                       'os_tenant_name': appnode.get('os_tenant_name', ''), 
                       'os_username': appnode.get('os_username', ''), 
                       'os_password': appnode.get('os_password', ''), 
                       'os_auth_url': appnode.get('os_auth_url', ''), 
                       'os_region_name': appnode.get('os_region_name', ''), 
                       'uuid': appnode.get('uuid', ''), 
                       'ssh_user': appnode.get('ssh_user', ''), 
                       'vsmapp_id': appnode.get('vsmapp_id', ''), 
                       'ssh_status': appnode.get('ssh_status', ''), 
                       'log_info': appnode.get('log_info', '')}}

    def index(self, appnodes):
        """Show a list of appnodes without many details."""
        return self._list_view(self.basic, appnodes)

    def _list_view(self, func, appnodes):
        """Provide a view for a list of appnodes."""
        node_list = [ func(appnode)['appnode'] for appnode in appnodes ]
        nodes_dict = dict(appnodes=node_list)
        return nodes_dict