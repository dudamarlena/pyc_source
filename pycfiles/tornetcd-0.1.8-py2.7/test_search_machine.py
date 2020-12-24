# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-intel/egg/tornetcd/tests/test_search_machine.py
# Compiled at: 2016-03-30 00:12:10
import time
from .. import Client, EtcdResult, EtcdException
from tornado import ioloop, httpclient, gen, options
from . import BaseTestCase

class TestMember(BaseTestCase):

    def testGetMember(self):
        result = self.ioloop.run_sync(self.get_coroutine(self.client.get_members))
        assert isinstance(result, dict)
        assert len(result.items())

    def testSearchMachine(self):
        fun = self.get_coroutine(self.client.search_machine)
        result = self.ioloop.run_sync(fun)
        assert True


class TestMachineException(BaseTestCase):

    def testSearchMachineException(self):
        fun = self.get_coroutine(self.client.search_machine)
        try:
            result = self.ioloop.run_sync(fun)
        except Exception as ex:
            assert isinstance(ex, EtcdException)

    def get_hosts(self):
        return ['127.0.0.1:2333', '127.0.0.1:2379', '127.0.0.1:2379']


class TestMachineExceptionDown1(BaseTestCase):

    def get_hosts(self):
        return [
         '127.0.0.1:2333', '127.0.0.1:2370', '127.0.0.1:2379']

    def testSuccess(self):
        fun = self.get_coroutine(self.client.search_machine)
        try:
            result = self.ioloop.run_sync(fun)
        except Exception as ex:
            assert isinstance(ex, EtcdException)
        else:
            assert True