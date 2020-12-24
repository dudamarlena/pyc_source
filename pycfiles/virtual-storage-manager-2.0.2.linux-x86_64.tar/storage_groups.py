# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/vsm/api/views/storage_groups.py
# Compiled at: 2016-06-13 14:11:03
from vsm.api import common
import logging, time
LOG = logging.getLogger(__name__)

class ViewBuilder(common.ViewBuilder):
    _collection_name = 'storage_groups'

    def basic(self, request, storage_group):
        LOG.info('storage_groups api view %s ' % storage_group)
        _storage_group = {'storage_group': {'id': storage_group['id'], 
                             'name': storage_group['name'], 
                             'friendly_name': storage_group['friendly_name'].replace('_', ' '), 
                             'storage_class': storage_group['storage_class'], 
                             'attached_pools': storage_group['attached_pools'], 
                             'attached_osds': storage_group['attached_osds'], 
                             'capacity_total': storage_group['capacity_total'], 
                             'capacity_used': storage_group['capacity_used'], 
                             'capacity_avail': storage_group['capacity_avail'], 
                             'largest_node_capacity_used': storage_group['largest_node_capacity_used'], 
                             'status': storage_group['status'], 
                             'take_list': storage_group['take_list'], 
                             'rule_id': storage_group['rule_id'], 
                             'marker': storage_group['marker']}}
        try:
            _storage_group['storage_group']['updated_at'] = time.strftime('%Y-%m-%d %H:%M:%S', time.strptime(storage_group['updated_at'], '%Y-%m-%dT%H:%M:%S.000000'))
        except:
            _storage_group['storage_group']['updated_at'] = ''

        return _storage_group

    def index(self, request, storage_groups):
        """Show a list of storage_groups without many details."""
        return self._list_view(self.basic, request, storage_groups)

    def _list_view(self, func, request, storage_groups):
        """Provide a view for a list of storage_groups."""
        storage_group_list = [ func(request, storage_group)['storage_group'] for storage_group in storage_groups ]
        storage_groups_dict = dict(storage_groups=storage_group_list)
        return storage_groups_dict