# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/vsmclient/v1/placement_groups.py
# Compiled at: 2016-06-13 14:11:03
"""
Placement Groups interface.
"""
import urllib
from vsmclient import base

class PlacementGroup(base.Resource):
    """A placement group aggregates objects within a pool."""

    def __repr__(self):
        try:
            return '<PlacementGroup: %s>' % self.id
        except AttributeError:
            return '<PG: summary>'


class PlacementGroupsManager(base.ManagerWithFind):
    """
    Manage :class:`PlacementGroup` resources.
    """
    resource_class = PlacementGroup

    def get(self, placement_group_id):
        """
        Get a placement_group.

        :param placement_group_id: The ID of the placement_group.
        :rtype: :class:`PlacementGroup`
        """
        return self._get('/placement_groups/%s' % placement_group_id, 'placement_group')

    def list(self, detailed=False, search_opts=None, paginate_opts=None):
        """
        Get a list of all placement_groups.

        :rtype: list of :class:`PlacementGroup`
        """
        if search_opts is None:
            search_opts = {}
        if paginate_opts is None:
            paginate_opts = {}
        qparams = {}
        for opt, val in search_opts.iteritems():
            if val:
                qparams[opt] = val

        for opt, val in paginate_opts.iteritems():
            if val:
                qparams[opt] = val

        query_string = '?%s' % urllib.urlencode(qparams) if qparams else ''
        detail = ''
        if detailed:
            detail = '/detail'
        ret = self._list('/placement_groups%s%s' % (detail, query_string), 'placement_groups')
        return ret

    def summary(self):
        """
        summary
        """
        url = '/placement_groups/summary'
        return self._get(url, 'placement_group-summary')

    def _action(self, action, placement_group, info=None, **kwargs):
        """
        Perform a placement_group "action."
        """
        body = {action: info}
        self.run_hooks('modify_body_for_action', body, **kwargs)
        url = '/placement_groups/%s/action' % base.getid(placement_group)
        return self.api.client.post(url, body=body)