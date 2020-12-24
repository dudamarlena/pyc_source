# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\tests\simulation\test_service.py
# Compiled at: 2016-04-19 08:28:52
# Size of source mod 2**32: 3066 bytes
from unittest import TestCase
from mock import MagicMock, PropertyMock
from tests.fakes import InMemoryDataStorage
from mad.ast.definitions import DefineOperation
from mad.ast.actions import Think
from mad.evaluation import Symbols
from mad.simulation.factory import Factory
from mad.simulation.requests import Request
from mad.simulation.tasks import TaskPool
from mad.simulation.throttling import ThrottlingPolicy

class ServiceTests(TestCase):

    def setUp(self):
        self.factory = Factory()
        self.storage = InMemoryDataStorage(None)

    def test_throttling_is_trigger(self):
        self.create_service(busy_worker=1, queue_length=10, accept_next=False, rejection_count=0)
        request = self.create_request()
        self.service.process(request)
        self.assertEquals(0, request.reply_success.call_count)
        self.assertEquals(1, request.reply_error.call_count)

    def create_report(self):
        report = MagicMock()
        report.__call__ = MagicMock()
        self.storage.report_for = MagicMock(return_value=report)
        return report

    def create_service(self, busy_worker, queue_length, accept_next, rejection_count):
        self.simulation = self.factory.create_simulation(self.storage)
        self.environment = self.simulation.environment.create_local_environment()
        self.create_throttling(rejection_count, accept_next)
        self.create_noop_operation()
        self.service = self.factory.create_service('ServiceUnderTest', self.environment)
        for i in range(busy_worker):
            self.service.workers.acquire_one()

    def create_throttling(self, rejection_count, do_reject):
        self.throttling = TailDrop()
        self.throttling._accepts.return_value = do_reject
        type(self.throttling).rejection_count = PropertyMock(return_value=rejection_count)
        self.environment.define(Symbols.QUEUE, self.throttling)

    def create_noop_operation(self):
        noop = self.factory.create_operation(self.environment, DefineOperation('NOOP', Think(5)))
        self.environment.define('NOOP', noop)

    def create_request(self):
        request = MagicMock(Request)
        request.identifier = 1
        request.operation = 'NOOP'
        return request