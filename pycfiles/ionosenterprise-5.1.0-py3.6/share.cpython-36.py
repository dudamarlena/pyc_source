# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ionosenterprise/requests/share.py
# Compiled at: 2019-10-08 04:15:23
# Size of source mod 2**32: 3070 bytes
import json

class share:

    def list_shares(self, group_id, depth=1):
        """
        Retrieves a list of all shares though a group.

        :param      group_id: The unique ID of the group.
        :type       group_id: ``str``

        :param      depth: The depth of the response data.
        :type       depth: ``int``

        """
        response = self._perform_request('/um/groups/%s/shares?depth=%s' % (group_id, str(depth)))
        return response

    def get_share(self, group_id, resource_id, depth=1):
        """
        Retrieves a specific resource share available to a group.

        :param      group_id: The unique ID of the group.
        :type       group_id: ``str``

        :param      resource_id: The unique ID of the resource.
        :type       resource_id: ``str``

        :param      depth: The depth of the response data.
        :type       depth: ``int``

        """
        response = self._perform_request('/um/groups/%s/shares/%s?depth=%s' % (
         group_id, resource_id, str(depth)))
        return response

    def add_share(self, group_id, resource_id, **kwargs):
        """
        Shares a resource through a group.

        :param      group_id: The unique ID of the group.
        :type       group_id: ``str``

        :param      resource_id: The unique ID of the resource.
        :type       resource_id: ``str``

        """
        properties = {}
        for attr, value in kwargs.items():
            properties[self._underscore_to_camelcase(attr)] = value

        data = {'properties': properties}
        response = self._perform_request(url=('/um/groups/%s/shares/%s' % (group_id, resource_id)),
          method='POST',
          data=(json.dumps(data)))
        return response

    def update_share(self, group_id, resource_id, **kwargs):
        """
        Updates the permissions of a group for a resource share.

        :param      group_id: The unique ID of the group.
        :type       group_id: ``str``

        :param      resource_id: The unique ID of the resource.
        :type       resource_id: ``str``

        """
        properties = {}
        for attr, value in kwargs.items():
            properties[self._underscore_to_camelcase(attr)] = value

        data = {'properties': properties}
        response = self._perform_request(url=('/um/groups/%s/shares/%s' % (group_id, resource_id)),
          method='PUT',
          data=(json.dumps(data)))
        return response

    def delete_share(self, group_id, resource_id):
        """
        Removes a resource share from a group.

        :param      group_id: The unique ID of the group.
        :type       group_id: ``str``

        :param      resource_id: The unique ID of the resource.
        :type       resource_id: ``str``

        """
        response = self._perform_request(url=('/um/groups/%s/shares/%s' % (group_id, resource_id)),
          method='DELETE')
        return response