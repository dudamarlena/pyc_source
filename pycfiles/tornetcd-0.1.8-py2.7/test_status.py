# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-intel/egg/tornetcd/tests/test_status.py
# Compiled at: 2016-03-30 00:12:10
import time
from .. import Client, EtcdResult, EtcdException
from tornado import ioloop, httpclient, gen, options
from . import BaseTestCase

class TestStatus(BaseTestCase):

    def testLeader(self):
        result = self.ioloop.run_sync(self.get_coroutine(self.client.leader))
        assert isinstance(result, dict)
        assert 'name' in result
        assert 'peerURIs' in result

    def testStats(self):
        result = self.ioloop.run_sync(self.get_coroutine(self.client.leader_stats))
        assert isinstance(result, dict)

    def testStoreStats(self):
        result = self.ioloop.run_sync(self.get_coroutine(self.client.store_stats))
        assert isinstance(result, dict)