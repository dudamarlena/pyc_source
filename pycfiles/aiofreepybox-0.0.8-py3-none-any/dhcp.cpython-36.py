# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /mnt/c/Users/luc_t_000/projects/freepybox/aiofreepybox/api/dhcp.py
# Compiled at: 2018-12-03 18:01:41
# Size of source mod 2**32: 721 bytes


class Dhcp:

    def __init__(self, access):
        self._access = access

    async def get_config(self):
        """
        Get DHCP configuration
        """
        return await self._access.get('dhcp/config/')

    async def set_config(self, conf):
        """
        Update a config with new conf dictionary
        """
        self._access.put('dhcp/config/', conf)

    async def get_dynamic_dhcp_lease(self):
        """
        Get the list of DHCP dynamic leases
        """
        return await self._access.get('dhcp/dynamic_lease/')

    async def get_static_dhcp_lease(self):
        """
        Get the list of DHCP static leases
        """
        return await self._access.get('dhcp/static_lease/')