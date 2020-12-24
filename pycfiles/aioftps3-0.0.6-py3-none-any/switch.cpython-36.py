# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /mnt/c/Users/luc_t_000/projects/freepybox/aiofreepybox/api/switch.py
# Compiled at: 2018-12-03 18:01:41
# Size of source mod 2**32: 794 bytes


class Switch:

    def __init__(self, access):
        self._access = access

    async def get_status(self):
        """
        Get Switch status
        """
        return await self._access.get('switch/status/')

    async def get_port_conf(self, port_id):
        """
        Get port_id Port configuration
        """
        return await self._access.get('switch/port/{0}'.format(port_id))

    async def set_port_conf(self, port_id, conf):
        """
        Update port_id Port configuration with conf dictionary
        """
        await self._access.put('switch/port/{0}'.format(port_id), conf)

    async def get_port_stats(self, port_id):
        """
        Get port_id Port stats
        """
        return await self._access.get('switch/port/{0}/{1}'.format(port_id, 'stats'))