# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/vsmclient/v1/appnodes.py
# Compiled at: 2016-06-13 14:11:03
"""
Appnodes interface.
"""
from vsmclient import base
import urllib

class AppNode(base.Resource):
    """An appnode connects to openstack cinder."""

    def __repr__(self):
        return '<App Node: %s>' % self.id

    def update(self, **kwargs):
        """update ssh_status and log_info"""
        self.manager.update(self, **kwargs)

    def delete(self):
        """Delete this appnode."""
        self.manager.delete(self)


class AppNodeManager(base.ManagerWithFind):
    """
    Manage :class:`AppNode` resources.
    """
    resource_class = AppNode

    def create(self, auth_openstack):
        """
        Create a list of  app nodes.
        """
        body = {'appnodes': auth_openstack}
        return self._create('/appnodes', body, 'appnodes')

    def get(self, appnode_id):
        """
        Get details of an appnode.
        """
        return self._get('/appnodes/%s' % appnode_id, 'appnode')

    def list(self, detailed=False, search_opts=None):
        """
        Get a list of all appnodes.
        :rtype: list of :class:`AppNode`
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
        ret = self._list('/appnodes%s%s' % (detail, query_string), 'appnodes')
        return ret

    def delete(self, appnode):
        """
        Delete an app node.

        :param appnode: The :class:`AppNode` to delete.
        """
        self._delete('/appnodes/%s' % base.getid(appnode))

    def update(self, appnode, appnode_info):
        """
        Update the ssh_status or log_info for an appnode.

        """
        if not appnode_info:
            return
        body = {'appnode': appnode_info}
        self._update('/appnodes/%s' % base.getid(appnode), body)