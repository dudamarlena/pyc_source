# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /mnt/c/Users/luc_t_000/projects/freepybox/aiofreepybox/api/nat.py
# Compiled at: 2019-03-10 17:26:53
# Size of source mod 2**32: 1881 bytes


class Nat:

    def __init__(self, access):
        self._access = access

    async def get_port_forwarding_list(self):
        """
        Get the list of port forwarding
        """
        return await self._access.get('fw/redir/')

    async def get_port_forwarding(self, redir_id):
        """
        Get a specific port forwarding
        """
        return await self._access.get('fw/redir/{0}'.format(redir_id))

    async def set_port_forwarding(self, redir_id, conf):
        """
        Update a port forwarding
        """
        return await self._access.put('fw/redir/{0}'.format(redir_id), conf)

    async def create_port_forwarding(self, conf):
        """
        Add a port forwarding
        """
        return await self._access.post('fw/redir/', conf)

    async def delete_port_forwarding(self, redir_id):
        """
        Delete a port forwarding
        """
        return await self._access.delete('fw/redir/{0}'.format(redir_id))

    async def get_incoming_port_list(self):
        """
        Get the list of incoming ports
        """
        return await self._access.get('fw/incoming/')

    async def get_incoming_port(self, inc_port_id):
        """
        Get a specific incoming port
        """
        return await self._access.get('fw/incoming/{}'.format(inc_port_id))

    async def set_incoming_port(self, inc_port_id, conf):
        """
        Update an incoming port
        """
        return await self._access.put('fw/incoming/{}'.format(inc_port_id), conf)

    async def get_dmz(self):
        """
        Get the current DMZ configuration
        """
        return await self._access.get('fw/dmz/')

    async def set_dmz(self, conf):
        """
        Update the current DMZ configuration
        """
        return await self._access.put('fw/dmz/', conf)