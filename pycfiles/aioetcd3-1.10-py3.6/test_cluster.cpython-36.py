# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/test/test_cluster.py
# Compiled at: 2018-05-26 21:48:07
# Size of source mod 2**32: 942 bytes
import unittest, asyncio, functools
from aioetcd3.client import client
from aioetcd3.help import range_all

def asynctest(f):

    @functools.wraps(f)
    def _f(self):
        asyncio.get_event_loop().run_until_complete(f(self))

    return _f


class ClusterTest(unittest.TestCase):

    def setUp(self):
        endpoints = '127.0.0.1:2379'
        self.client = client(endpoint=endpoints)

    @asynctest
    async def test_member(self):
        members = await self.client.member_list()
        self.assertTrue(members)
        m = members[0]
        healthy, unhealthy = await self.client.member_healthy([m.clientURLs])
        self.assertTrue(healthy)
        self.assertFalse(unhealthy)
        healthy, unhealthy = await self.client.member_healthy()
        self.assertTrue(healthy)
        self.assertFalse(unhealthy)