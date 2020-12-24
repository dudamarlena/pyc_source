# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/vsmclient/v1/licenses.py
# Compiled at: 2016-06-13 14:11:03
import urllib
from vsmclient import base

class License(base.Resource):
    """"""

    def __repr__(self):
        return '<License: %s>' % self.id

    def delete(self):
        """Delete this vsm."""
        self.manager.delete(self)

    def update(self, **kwargs):
        """Update the display_name or display_description for this vsm."""
        self.manager.update(self, **kwargs)

    def force_delete(self):
        """Delete the specified vsm ignoring its current state.

        :param vsm: The UUID of the vsm to force-delete.
        """
        self.manager.force_delete(self)


class LicenseManager(base.ManagerWithFind):
    """"""
    resource_class = License

    def license_get(self):
        url = '/licenses/license_status_get'
        return self.api.client.get(url)

    def license_create(self, value):
        body = {'value': value}
        url = '/licenses/license_status_create'
        return self.api.client.post(url, body=body)

    def license_update(self, value):
        body = {'value': value}
        url = '/licenses/license_status_update'
        return self.api.client.post(url, body=body)