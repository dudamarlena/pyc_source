# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-intel/egg/tornetcd/tests/test_exception.py
# Compiled at: 2016-03-30 00:12:10
import time
from .. import Client, EtcdResult
from .. import exceptions as etcd_exc
from . import BaseTestCase

class TestTimeout(BaseTestCase):

    def get_etcdclient(self):
        return Client(host=self.hosts, httpclient=self.http, read_timeout=0.0001, ioloop=self.ioloop)

    def testAllTimeout(self):
        key = '/test5'
        fun = self.get_coroutine(self.client.get, key)
        try:
            result = self.ioloop.run_sync(fun)
        except Exception as ex:
            assert isinstance(ex, etcd_exc.EtcdConnectionFailed)


class TestAnyHostFaild(BaseTestCase):

    def get_hosts(self):
        return [
         '127.0.0.1:2370', '127.0.0.1:237', '127.0.0.1:212']

    def testTimeout(self):
        key = '/test5'
        fun = self.get_coroutine(self.client.get, key)
        for x in range(5):
            result = self.ioloop.run_sync(fun)
            assert isinstance(result, EtcdResult)