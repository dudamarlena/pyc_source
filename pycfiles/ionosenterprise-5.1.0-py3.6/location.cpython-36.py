# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ionosenterprise/requests/location.py
# Compiled at: 2019-10-08 04:15:23
# Size of source mod 2**32: 582 bytes


class location:

    def get_location(self, location_id, depth=0):
        """
        Retrieves a single location by ID.

        :param      location_id: The unique ID of the location.
        :type       location_id: ``str``

        """
        response = self._perform_request('/locations/%s?depth=%s' % (location_id, depth))
        return response

    def list_locations(self, depth=0):
        """
        Retrieves a list of locations available in the account.

        """
        response = self._perform_request('/locations?depth=%s' % depth)
        return response