# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/vsmclient/v1/vsm_snapshots.py
# Compiled at: 2016-06-13 14:11:03
"""
Volume snapshot interface (1.1 extension).
"""
import urllib
from vsmclient import base

class Snapshot(base.Resource):
    """
    A Snapshot is a point-in-time snapshot of an openstack vsm.
    """

    def __repr__(self):
        return '<Snapshot: %s>' % self.id

    def delete(self):
        """
        Delete this snapshot.
        """
        self.manager.delete(self)

    def update(self, **kwargs):
        """
        Update the display_name or display_description for this snapshot.
        """
        self.manager.update(self, **kwargs)

    @property
    def progress(self):
        return self._info.get('os-extended-snapshot-attributes:progress')

    @property
    def project_id(self):
        return self._info.get('os-extended-snapshot-attributes:project_id')


class SnapshotManager(base.ManagerWithFind):
    """
    Manage :class:`Snapshot` resources.
    """
    resource_class = Snapshot

    def create(self, vsm_id, force=False, display_name=None, display_description=None):
        """
        Create a snapshot of the given vsm.

        :param vsm_id: The ID of the vsm to snapshot.
        :param force: If force is True, create a snapshot even if the vsm is
        attached to an instance. Default is False.
        :param display_name: Name of the snapshot
        :param display_description: Description of the snapshot
        :rtype: :class:`Snapshot`
        """
        body = {'snapshot': {'vsm_id': vsm_id, 'force': force, 
                        'display_name': display_name, 
                        'display_description': display_description}}
        return self._create('/snapshots', body, 'snapshot')

    def get(self, snapshot_id):
        """
        Get a snapshot.

        :param snapshot_id: The ID of the snapshot to get.
        :rtype: :class:`Snapshot`
        """
        return self._get('/snapshots/%s' % snapshot_id, 'snapshot')

    def list(self, detailed=True, search_opts=None):
        """
        Get a list of all snapshots.

        :rtype: list of :class:`Snapshot`
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
        return self._list('/snapshots%s%s' % (detail, query_string), 'snapshots')

    def delete(self, snapshot):
        """
        Delete a snapshot.

        :param snapshot: The :class:`Snapshot` to delete.
        """
        self._delete('/snapshots/%s' % base.getid(snapshot))

    def update(self, snapshot, **kwargs):
        """
        Update the display_name or display_description for a snapshot.

        :param snapshot: The :class:`Snapshot` to delete.
        """
        if not kwargs:
            return
        body = {'snapshot': kwargs}
        self._update('/snapshots/%s' % base.getid(snapshot), body)