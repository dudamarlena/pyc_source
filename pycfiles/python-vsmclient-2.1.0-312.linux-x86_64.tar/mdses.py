# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/vsmclient/v1/mdses.py
# Compiled at: 2016-06-13 14:11:03
"""
MDSes interface.
"""
import urllib
from vsmclient import base

class Mds(base.Resource):
    """A mds stores metadata on behalf of the Ceph Filesystem."""

    def __repr__(self):
        return '<MDS: %s>' % self.id

    def delete(self):
        """Delete this mds."""
        self.manager.delete(self)


class MdsesManager(base.ManagerWithFind):
    """
    Manage :class:`MDS` resources.
    """
    resource_class = Mds

    def get(self, mds_id):
        """
        Get a mds.

        :param mds_id: The ID of the mds.
        :rtype: :class:`MDS`
        """
        return self._get('/mdses/%s' % mds_id, 'mds')

    def list(self, detailed=False, search_opts=None):
        """
        Get a list of all mdses.

        :rtype: list of :class:`MDS`
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
        ret = self._list('/mdses%s%s' % (detail, query_string), 'mdses')
        return ret

    def restart(self, mds):
        self._action('restart', mds)

    def remove(self, mds):
        self._action('remove', mds)

    def delete(self, mds):
        self._delete('/mdses/%s' % base.getid(mds))

    def restore(self, mds):
        self._action('restore', mds)

    def summary(self):
        """
        summary
        """
        url = '/mdses/summary'
        return self._get(url, 'mds-summary')

    def _action(self, action, mds, info=None, **kwargs):
        """
        Perform a mds "action."
        """
        body = {action: info}
        self.run_hooks('modify_body_for_action', body, **kwargs)
        url = '/mdses/%s/action' % base.getid(mds)
        return self.api.client.post(url, body=body)