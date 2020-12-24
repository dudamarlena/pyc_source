# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
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