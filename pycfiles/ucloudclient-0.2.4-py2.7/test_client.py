# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-x86_64/egg/ucloudclient/tests/test_client.py
# Compiled at: 2015-11-11 06:54:58
from testtools import TestCase
from ucloudclient import client

class ClientTest(TestCase):

    def test_client_get_reset_timings(self):
        cs = client.Client('base_url', 'public_key', 'private_key')
        self.assertEqual(0, len(cs.get_timing()))
        cs.client.time.append('somevalue')
        self.assertEqual(1, len(cs.get_timing()))
        self.assertEqual('somevalue', cs.get_timing()[0])
        cs.reset_timing()
        self.assertEqual(0, len(cs.get_timing()))