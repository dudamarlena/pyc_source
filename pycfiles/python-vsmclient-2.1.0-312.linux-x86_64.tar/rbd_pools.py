# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/vsmclient/v1/rbd_pools.py
# Compiled at: 2016-06-13 14:11:03
"""
RBDPools interface.
"""
import urllib
from vsmclient import base

class RBDPool(base.Resource):
    """A rbd_pool is an extra block level storage to the OpenStack instances."""

    def __repr__(self):
        return '<RBDPool: %s>' % self.id


class RBDPoolsManager(base.ManagerWithFind):
    """
    Manage :class:`RBDPool` resources.
    """
    resource_class = RBDPool

    def get(self, rbd_pool_id):
        """
        Get a rbd_pool.

        :param rbd_pool_id: The ID of the rbd_pool.
        :rtype: :class:`RBDPool`
        """
        return self._get('/rbd_pools/%s' % rbd_pool_id, 'rbd_pool')

    def list(self, detailed=False, search_opts=None, paginate_opts=None):
        """
        Get a list of all rbd_pools.

        :rtype: list of :class:`RBDPool`
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
        ret = self._list('/rbd_pools%s%s' % (detail, query_string), 'rbd_pools')
        return ret

    def summary(self):
        """
        summary
        """
        url = '/rbd_pools/summary'
        return self._get(url, 'rbd-summary')

    def _action(self, action, rbd_pool, info=None, **kwargs):
        """
        Perform a rbd_pool "action."
        """
        body = {action: info}
        self.run_hooks('modify_body_for_action', body, **kwargs)
        url = '/rbd_pools/%s/action' % base.getid(rbd_pool)
        return self.api.client.post(url, body=body)