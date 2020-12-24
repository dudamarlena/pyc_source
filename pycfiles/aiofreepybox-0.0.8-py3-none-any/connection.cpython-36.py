# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /mnt/c/Users/luc_t_000/projects/freepybox/aiofreepybox/api/connection.py
# Compiled at: 2018-12-03 18:01:41
# Size of source mod 2**32: 814 bytes


class Connection:

    def __init__(self, access):
        self._access = access

    async def get_status(self):
        """
        Get connection status:
        """
        return await self._access.get('connection/')

    async def get_config(self):
        """
        Get connection configuration:
        """
        return await self._access.get('connection/config/')

    async def set_config(self, conf):
        """
        Update connection configuration:
        """
        await self._access.put('connection/config/', conf)

    async def get_xdsl(self):
        """
        Get xdsl infos:
        """
        return await self._access.get('connection/xdsl/')

    async def get_ftth(self):
        """
        Get ftth infos:
        """
        return await self._access.get('connection/ftth/')