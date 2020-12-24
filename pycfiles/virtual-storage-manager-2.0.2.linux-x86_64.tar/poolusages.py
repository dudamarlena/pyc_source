# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/vsm/api/views/poolusages.py
# Compiled at: 2016-06-13 14:11:03
from vsm.api import common
import logging
LOG = logging.getLogger(__name__)

class ViewBuilder(common.ViewBuilder):
    _collection_name = 'poolusages'

    def basic(self, poolusage):
        if not poolusage.get('id', ''):
            poolusage['id'] = ''
            return poolusage
        return {'poolusage': {'id': poolusage.get('id', 0), 
                         'pool_id': poolusage.get('pool_id', ''), 
                         'vsmapp_id': poolusage.get('vsmapp_id', ''), 
                         'cinder_volume_host': poolusage.get('cinder_volume_host', ''), 
                         'as_glance_store_pool': poolusage.get('as_glance_store_pool', ''), 
                         'attach_status': poolusage.get('attach_status', ''), 
                         'attach_at': poolusage.get('attach_at', '')}}

    def index(self, poolusages):
        """Show a list of poolusages without many details."""
        return self._list_view(self.basic, poolusages)

    def _list_view(self, func, poolusages):
        """Provide a view for a list of poolusages."""
        node_list = [ func(poolusage)['poolusage'] for poolusage in poolusages ]
        nodes_dict = dict(poolusages=node_list)
        return nodes_dict