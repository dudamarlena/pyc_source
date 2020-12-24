# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\dblapi\helpers.py
# Compiled at: 2018-03-18 13:07:26
# Size of source mod 2**32: 1358 bytes


async def update_vote_cache(client, **kwargs):
    r = await client.http.get((client.router.bot_votes), params={'onlyids':'true', 
     'days':kwargs.get('days', 31)})
    return r