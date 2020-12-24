# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /mnt/c/Users/luc_t_000/projects/freepybox/aiofreepybox/api/call.py
# Compiled at: 2018-12-03 18:01:41
# Size of source mod 2**32: 237 bytes


class Call:

    def __init__(self, access):
        self._access = access

    async def get_call_list(self):
        """
        Returns the collection of all call entries
        """
        return await self._access.get('call/log/')