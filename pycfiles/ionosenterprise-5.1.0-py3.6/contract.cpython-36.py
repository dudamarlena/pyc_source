# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ionosenterprise/requests/contract.py
# Compiled at: 2019-10-08 04:15:23
# Size of source mod 2**32: 302 bytes


class contract:

    def list_contracts(self, depth=1):
        """
        Retrieves information about the resource limits
        for a particular contract and the current resource usage.

        """
        response = self._perform_request('/contracts?depth=' + str(depth))
        return response