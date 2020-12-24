# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/vsm/api/views/clusters.py
# Compiled at: 2016-06-13 14:11:03
from vsm.api import common
import logging
LOG = logging.getLogger(__name__)

class ViewBuilder(common.ViewBuilder):
    _collection_name = 'clusters'

    def basic(self, cluster):
        return {'cluster': {'id': 1, 
                       'name': cluster['name'], 
                       'file_system': '', 
                       'journal_size': '', 
                       'size': '', 
                       'management_network': '', 
                       'ceph_public_network': '1', 
                       'cluster_network': '14', 
                       'primary_public_ip_netmask': '', 
                       'scecondary_public_ip_netmask': '', 
                       'cluster_ip_netmask': ''}}

    def index(self, clusters):
        """Show a list of servers without many details."""
        return self._list_view(self.basic, clusters)

    def _list_view(self, func, clusters):
        """Provide a view for a list of servers."""
        cluster_list = [ func(cluster)['cluster'] for cluster in clusters ]
        clusters_dict = dict(clusters=cluster_list)
        return clusters_dict