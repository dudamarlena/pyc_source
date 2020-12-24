# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\tests\simulation\test_events.py
# Compiled at: 2016-04-27 04:44:18
# Size of source mod 2**32: 7115 bytes
from unittest import TestCase
from mock import MagicMock, call
from tests.fakes import InMemoryDataStorage
from mad.evaluation import Symbols
from mad.ast.commons import Sequence
from mad.ast.definitions import *
from mad.ast.actions import *
from mad.simulation.factory import Simulation
from mad.simulation.events import Listener, Dispatcher
from mad.simulation.throttling import ThrottlingWrapper, ThrottlingPolicyDecorator
from mad.simulation.requests import Request
FAKE_REQUEST = 'whatever'
FAKE_SERVICE = 'service'

class DispatcherTests(TestCase):

    def setUp(self):
        self.dispatcher = Dispatcher()

    def test_register_rejects_non_listener(self):
        with self.assertRaises(AssertionError):
            self.dispatcher.register('this is not a listener')

    def test_notifies_only_once_despite_multiple_registration(self):
        listener = self._fake_listener()
        self.dispatcher.register(listener)
        self.dispatcher.register(listener)
        self.dispatcher.arrival_of(FAKE_REQUEST)
        listener.arrival_of.assert_called_once_with(FAKE_REQUEST)

    def test_dispatch(self):
        invocations = [
         (
          'arrival_of', [FAKE_REQUEST]),
         (
          'rejection_of', [FAKE_REQUEST]),
         (
          'posting_of', [FAKE_SERVICE, FAKE_REQUEST]),
         (
          'success_of', [FAKE_REQUEST]),
         (
          'failure_of', [FAKE_REQUEST]),
         (
          'timeout_of', [FAKE_REQUEST]),
         (
          'storage_of', [FAKE_REQUEST]),
         (
          'selection_of', [FAKE_REQUEST]),
         (
          'resuming', [FAKE_REQUEST]),
         (
          'error_replied_to', [FAKE_REQUEST]),
         (
          'success_replied_to', [FAKE_REQUEST])]
        for method_name, parameters in invocations:
            self._do_test_dispatch_of(method_name, *parameters)

    def _do_test_dispatch_of(self, method_name, *parameters):
        listener = self._fake_listener()
        method = getattr(self.dispatcher, method_name)
        method(*parameters)
        delegate = getattr(listener, method_name)
        delegate.assert_called_once_with(*parameters)

    def _fake_listener(self):
        listener = MagicMock(Listener)
        self.dispatcher.register(listener)
        return listener


class ServiceMonitoring(TestCase):

    def setUp(self):
        self.simulation = Simulation(InMemoryDataStorage(None))

    def define(self, symbol, value):
        self.simulation.environment.define(symbol, value)
        return value

    def look_up(self, symbol):
        return self.simulation.environment.look_up(symbol)

    def evaluate(self, expression, continuation=lambda x: x):
        return self.simulation.evaluate(expression, continuation)

    def simulate_until(self, end):
        self.simulation.run_until(end)

    def test_notifies_rejection(self):
        db = self.evaluate(DefineService('DB', DefineOperation('Select', Think(5)))).value
        fake_task_pool = MagicMock(ThrottlingPolicyDecorator)
        fake_task_pool._accepts = MagicMock(return_value=False)
        db.tasks = ThrottlingWrapper(db.environment, task_pool=fake_task_pool)
        listener = MagicMock(Listener)
        db.environment.look_up(Symbols.LISTENER).register(listener)
        request1 = self.send_request('DB', 'Select')
        request2 = self.send_request('DB', 'Select')
        self.simulate_until(10)
        expected_calls = [
         call.arrival_of(request1),
         call.arrival_of(request2),
         call.rejection_of(request2),
         call.success_replied_to(request1)]
        self.assertEqual(expected_calls, listener.method_calls, listener.method_calls)

    def test_notifies_arrival_and_success(self):
        db = self.evaluate(DefineService('DB', DefineOperation('Select', Think(5)))).value
        listener = MagicMock(Listener)
        db.environment.look_up(Symbols.LISTENER).register(listener)
        request = self.send_request('DB', 'Select')
        self.simulate_until(10)
        expected_calls = [
         call.arrival_of(request),
         call.success_replied_to(request)]
        self.assertEqual(expected_calls, listener.method_calls, listener.method_calls)

    def test_notifies_arrival_and_failure(self):
        db = self.evaluate(DefineService('DB', DefineOperation('Select', Fail()))).value
        listener = MagicMock(Listener)
        db.environment.look_up(Symbols.LISTENER).register(listener)
        request = self.send_request('DB', 'Select')
        self.simulate_until(10)
        expected_calls = [
         call.arrival_of(request),
         call.error_replied_to(request)]
        self.assertEqual(expected_calls, listener.method_calls, listener.method_calls)

    def test_notifies_when_request_timeout(self):
        db = self.evaluate(DefineService('DB', DefineOperation('Select', Fail()))).value
        listener = MagicMock(Listener)
        db.environment.look_up(Symbols.LISTENER).register(listener)
        request = self.send_request('DB', 'Select')
        request.reply_error()
        self.simulate_until(40)
        expected_calls = [
         call.arrival_of(request),
         call.error_replied_to(request)]
        self.assertEqual(expected_calls, listener.method_calls, listener.method_calls)

    def send_request(self, service_name, operation_name, on_success=lambda : None, on_error=lambda : None):
        service = self.look_up(service_name)
        request = self.fake_request(operation_name, on_success=on_success, on_error=on_error)
        request.send_to(service)
        return request

    def fake_request(self, operation, on_success=lambda : None, on_error=lambda : None):
        return Request(self.fake_client(), 0, operation, 1, on_success=on_success, on_error=on_error)

    def fake_client(self):
        fake_client = MagicMock()
        fake_client.schedule = self.simulation.schedule
        return fake_client