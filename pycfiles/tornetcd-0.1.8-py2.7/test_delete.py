# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-intel/egg/tornetcd/tests/test_delete.py
# Compiled at: 2016-03-30 00:12:10
import time
from .. import Client, EtcdResult
from tornado import ioloop, httpclient, gen, options
from . import BaseTestCase
from .. import exceptions as etcdexc

class TestDelete(BaseTestCase):

    def testPopDefault(self):
        key = '/test0123_%s' % time.time()
        value = 'tornado-etcd'
        fun = self.get_coroutine(self.client.write, key, value)
        result = self.ioloop.run_sync(fun)
        fun = self.get_coroutine(self.client.pop, key)
        result = self.ioloop.run_sync(fun)
        assert isinstance(result, EtcdResult)
        assert result.action == 'delete'
        assert result.value == None
        return

    def testNonKeyDefault(self):
        key = '/abc%s' % time.time()
        fun = self.get_coroutine(self.client.pop, key)
        try:
            result = self.ioloop.run_sync(fun)
        except Exception as ex:
            assert isinstance(ex, etcdexc.EtcdKeyNotFound)