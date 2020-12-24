# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/vsm/api/views/placement_groups.py
# Compiled at: 2016-06-13 14:11:03
from vsm.api import common
import logging
LOG = logging.getLogger(__name__)

class ViewBuilder(common.ViewBuilder):
    _collection_name = 'placement_groups'

    def basic(self, request, placement_group):
        LOG.info('placement_groups api view %s ' % placement_group)
        return {'placement_group': {'id': placement_group['id'], 
                               'pg_id': placement_group['pgid'], 
                               'state': placement_group['state'], 
                               'up': placement_group['up'], 
                               'acting': placement_group['acting']}}

    def _detail(self, request, placement_group):
        LOG.info('placement_groups api detail view %s ' % placement_group)
        return {'placement_group': {'id': placement_group['id'], 
                               'pg_id': placement_group['pgid'], 
                               'state': placement_group['state'], 
                               'up': placement_group['up'], 
                               'acting': placement_group['acting']}}

    def detail(self, request, placement_groups):
        return self._list_view(self._detail, request, placement_groups)

    def index(self, request, placement_groups):
        """Show a list of placement_groups without many details."""
        return self._list_view(self.basic, request, placement_groups)

    def _list_view(self, func, request, placement_groups):
        """Provide a view for a list of placement_groups."""
        placement_group_list = [ func(request, placement_group)['placement_group'] for placement_group in placement_groups ]
        placement_groups_dict = dict(placement_groups=placement_group_list)
        return placement_groups_dict