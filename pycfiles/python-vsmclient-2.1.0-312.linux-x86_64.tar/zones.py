# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/vsmclient/v1/zones.py
# Compiled at: 2016-06-13 14:11:03
"""
Zone interface.
"""
import urllib
from vsmclient import base
import logging

class Zone(base.Resource):
    """"""

    def __repr__(self):
        return '<Zone: %s>' % self.id

    def delete(self):
        """Delete this zone."""
        self.manager.delete(self)

    def update(self, **kwargs):
        """"""
        self.manager.update(self, **kwargs)


class ZoneManager(base.ManagerWithFind):
    """
    Manage :class:`Zone` resources.
    """
    resource_class = Zone

    def create(self, body):
        """
        Create a zone.
        """
        return self._create('/zones', body, 'zone')

    def get(self, zone_id):
        """
        Get a zone.

        :param zone_id: The ID of the zone to delete.
        :rtype: :class:`Zone`
        """
        return self._get('/zones/%s' % zone_id, 'zone')

    def osd_locations_choices(self):
        """
        :rtype: :class:`Zone`
        """
        resp, body = self.api.client.get('/zones/osd_locations_choices')
        return body

    def get_zone_not_in_crush_list(self):
        """
        :rtype: :class:`Zone`
        """
        resp, body = self.api.client.get('/zones/get_zone_not_in_crush_list')
        return body

    def list(self, detailed=False, search_opts=None):
        """
        Get a list of all zones.

        :rtype: list of :class:`Zone`
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
        ret = self._list('/zones%s%s' % (detail, query_string), 'zones')
        return ret

    def delete(self, zone):
        """
        Delete a zone.

        :param zone: The :class:`Zone` to delete.
        """
        self._delete('/zones/%s' % base.getid(zone))

    def update(self, zone, **kwargs):
        """

        :param vsm: The :class:`Zone` to delete.
        """
        if not kwargs:
            return
        body = {'zone': kwargs}
        self._update('/zones/%s' % base.getid(zone), body)

    def _action(self, action, zone, info=None, **kwargs):
        """
        Perform a zone "action."
        """
        body = {action: info}
        self.run_hooks('modify_body_for_action', body, **kwargs)
        url = '/zones/%s/action' % base.getid(zone)
        return self.api.client.post(url, body=body)

    def add_zone_to_crushmap_and_db(self, body):
        url = '/zones/add_zone_to_crushmap_and_db'
        return self.api.client.post(url, body=body)