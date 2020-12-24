# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ionosenterprise/requests/ipblock.py
# Compiled at: 2019-10-08 04:15:23
# Size of source mod 2**32: 1456 bytes
import json

class ipblock:

    def get_ipblock(self, ipblock_id):
        """
        Retrieves a single IP block by ID.

        :param      ipblock_id: The unique ID of the IP block.
        :type       ipblock_id: ``str``

        """
        response = self._perform_request('/ipblocks/%s' % ipblock_id)
        return response

    def list_ipblocks(self, depth=1):
        """
        Retrieves a list of IP blocks available in the account.

        """
        response = self._perform_request('/ipblocks?depth=%s' % str(depth))
        return response

    def delete_ipblock(self, ipblock_id):
        """
        Removes a single IP block from your account.

        :param      ipblock_id: The unique ID of the IP block.
        :type       ipblock_id: ``str``

        """
        response = self._perform_request(url=('/ipblocks/' + ipblock_id),
          method='DELETE')
        return response

    def reserve_ipblock(self, ipblock):
        """
        Reserves an IP block within your account.

        """
        properties = {'name': ipblock.name}
        if ipblock.location:
            properties['location'] = ipblock.location
        if ipblock.size:
            properties['size'] = str(ipblock.size)
        raw = {'properties': properties}
        response = self._perform_request(url='/ipblocks',
          method='POST',
          data=(json.dumps(raw)))
        return response