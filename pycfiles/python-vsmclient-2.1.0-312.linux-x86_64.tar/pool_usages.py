# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/vsmclient/v1/pool_usages.py
# Compiled at: 2016-06-13 14:11:03
"""
Storage Pool Usage Interface.
"""
from vsmclient import base
import urllib

class PoolUsage(base.Resource):
    """"""

    def __repr__(self):
        return '<Pool Usage: %s>' % self.id

    def update(self, **kwargs):
        """update attach_status and time"""
        self.manager.update(self, **kwargs)

    def delete(self):
        """Delete this usage."""
        self.manager.delete(self)


class PoolUsageManager(base.ManagerWithFind):
    """
    Manage :class:`PoolUsage` resources.
    """
    resource_class = PoolUsage

    def create(self, pools=None):
        """
        Create pool usages.
        Param: a list of pool id and cinder_volume_host.
        """
        if not isinstance(pools, list):
            pool_list = list()
            pool_list.append(pools)
        else:
            pool_list = pools
        body = {'poolusages': pool_list}
        return self._create('/poolusages', body, 'poolusages')

    def list(self, detailed=False, search_opts=None):
        """
        Get a list of all pool usages.
        :rtype: list of :class:`PoolUsage`
        """
        if search_opts is None:
            search_opts = {}
        qparams = {}
        for opt, val in search_opts.iteritems():
            if val:
                qparams[opt] = val

        query_string = '?%s' % urllib.urlencode(qparams) if qparams else ''
        detail = ''
        if detailed:
            detail = '/detail'
        ret = self._list('/poolusages%s%s' % (detail, query_string), 'poolusages')
        return ret

    def delete(self, poolusage):
        """
        Delete an pool usage.

        :param poolusage: The :class:`PoolUsage` to delete.
        """
        self._delete('/poolusages/%s' % base.getid(poolusage))

    def update(self, poolusage, **kargs):
        """
        Update the attach_status and time for a set of pool usages.

        """
        if not kargs:
            return
        body = {'poolusages': kargs}
        self._update('/poolusages/%s' % base.getid(poolusage), body)