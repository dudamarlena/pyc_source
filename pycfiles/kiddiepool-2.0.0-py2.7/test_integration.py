# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/tests/test_integration.py
# Compiled at: 2018-03-12 19:01:14
import os, time
from kazoo.testing import harness
from unittest import skipIf
import kiddiepool

@skipIf(not os.getenv('ZOOKEEPER_PATH'), 'ZOOKEEPER_PATH is not defined; skipping integration tests')
class BasicPoolBehavior(harness.KazooTestHarness):
    SERVICE_PATH = '/services/herpderp/0.1'
    FAKE_HOST = '127.0.254.1:12345'

    def setUp(self):
        self.setup_zookeeper()
        self.client.ensure_path(self.SERVICE_PATH)
        self.pool = kiddiepool.TidePool(self.client, self.SERVICE_PATH)

    def tearDown(self):
        self.teardown_zookeeper()

    def test_pool_mutation(self):
        assert len(self.pool.candidate_pool) == 0
        self.client.create(('{0}/{1}').format(self.SERVICE_PATH, self.FAKE_HOST))
        time.sleep(0.5)
        assert len(self.pool.candidate_pool) == 1
        host, port = self.FAKE_HOST.split(':')
        host_tuple = (str(host), int(port))
        assert host_tuple in self.pool.candidate_pool