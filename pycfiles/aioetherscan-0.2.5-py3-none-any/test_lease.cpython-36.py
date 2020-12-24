# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/test/test_lease.py
# Compiled at: 2018-05-26 21:48:07
# Size of source mod 2**32: 2377 bytes
import unittest, asyncio, functools
from aioetcd3.client import client
from aioetcd3.help import range_all

def asynctest(f):

    @functools.wraps(f)
    def _f(self):
        asyncio.get_event_loop().run_until_complete(f(self))

    return _f


class LeaseTest(unittest.TestCase):

    def setUp(self):
        endpoints = '127.0.0.1:2379'
        self.client = client(endpoint=endpoints)
        self.tearDown()

    @asynctest
    async def test_lease_1(self):
        lease = await self.client.grant_lease(ttl=5)
        self.assertEqual(lease.ttl, 5)
        await asyncio.sleep(1)
        lease, keys = await self.client.get_lease_info(lease)
        self.assertLessEqual(lease.ttl, 4)
        self.assertEqual(len(keys), 0)
        lease = await self.client.refresh_lease(lease)
        self.assertEqual(lease.ttl, 5)
        await self.client.revoke_lease(lease)
        lease, keys = await self.client.get_lease_info(lease)
        self.assertIsNone(lease)
        self.assertEqual(len(keys), 0)

    @asynctest
    async def test_lease_2(self):
        lease = await self.client.grant_lease(ttl=5)
        self.assertEqual(lease.ttl, 5)
        await asyncio.sleep(1)
        lease, keys = await lease.info()
        self.assertLessEqual(lease.ttl, 4)
        self.assertEqual(len(keys), 0)
        lease = await lease.refresh()
        self.assertEqual(lease.ttl, 5)
        await lease.revoke()
        lease, keys = await lease.info()
        self.assertIsNone(lease)
        self.assertEqual(len(keys), 0)
        lease = None
        async with self.client.grant_lease_scope(ttl=5) as l:
            lease = l
            await asyncio.sleep(1)
        lease, keys = await lease.info()
        self.assertIsNone(lease)
        self.assertEqual(len(keys), 0)

    @asynctest
    async def test_lease_3(self):
        lease = await self.client.grant_lease(ttl=5)
        self.assertEqual(lease.ttl, 5)
        await self.client.put('/testlease', 'testlease', lease=lease)
        await asyncio.sleep(6)
        lease, keys = await lease.info()
        self.assertIsNone(lease, None)
        self.assertEqual(len(keys), 0)
        value, meta = await self.client.get('/testlease')
        self.assertIsNone(value)
        self.assertIsNone(meta)

    @asynctest
    async def tearDown(self):
        await self.client.delete(range_all())