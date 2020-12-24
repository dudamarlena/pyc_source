# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ionosenterprise/requests/request.py
# Compiled at: 2019-10-08 04:15:23
# Size of source mod 2**32: 836 bytes


class request:

    def get_request(self, request_id, status=False):
        """
        Retrieves a single request by ID.

        :param      request_id: The unique ID of the request.
        :type       request_id: ``str``

        :param      status: Retreive the full status of the request.
        :type       status: ``bool``

        """
        if status:
            response = self._perform_request('/requests/' + request_id + '/status')
        else:
            response = self._perform_request('/requests/%s' % request_id)
        return response

    def list_requests(self, depth=1):
        """
        Retrieves a list of requests available in the account.

        """
        response = self._perform_request('/requests?depth=%s' % str(depth))
        return response