# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-build-ed191__6/protobuf/google/protobuf/internal/service_reflection_test.py
# Compiled at: 2020-01-10 16:25:26
# Size of source mod 2**32: 5412 bytes
"""Tests for google.protobuf.internal.service_reflection."""
__author__ = 'petar@google.com (Petar Petrov)'
try:
    import unittest2 as unittest
except ImportError:
    import unittest

from google.protobuf import unittest_pb2
from google.protobuf import service_reflection
from google.protobuf import service

class FooUnitTest(unittest.TestCase):

    def testService(self):

        class MockRpcChannel(service.RpcChannel):

            def CallMethod(self, method, controller, request, response, callback):
                self.method = method
                self.controller = controller
                self.request = request
                callback(response)

        class MockRpcController(service.RpcController):

            def SetFailed(self, msg):
                self.failure_message = msg

        self.callback_response = None

        class MyService(unittest_pb2.TestService):
            pass

        self.callback_response = None

        def MyCallback(response):
            self.callback_response = response

        rpc_controller = MockRpcController()
        channel = MockRpcChannel()
        srvc = MyService()
        srvc.Foo(rpc_controller, unittest_pb2.FooRequest(), MyCallback)
        self.assertEqual('Method Foo not implemented.', rpc_controller.failure_message)
        self.assertEqual(None, self.callback_response)
        rpc_controller.failure_message = None
        service_descriptor = unittest_pb2.TestService.GetDescriptor()
        srvc.CallMethod(service_descriptor.methods[1], rpc_controller, unittest_pb2.BarRequest(), MyCallback)
        self.assertTrue(srvc.GetRequestClass(service_descriptor.methods[1]) is unittest_pb2.BarRequest)
        self.assertTrue(srvc.GetResponseClass(service_descriptor.methods[1]) is unittest_pb2.BarResponse)
        self.assertEqual('Method Bar not implemented.', rpc_controller.failure_message)
        self.assertEqual(None, self.callback_response)

        class MyServiceImpl(unittest_pb2.TestService):

            def Foo(self, rpc_controller, request, done):
                self.foo_called = True

            def Bar(self, rpc_controller, request, done):
                self.bar_called = True

        srvc = MyServiceImpl()
        rpc_controller.failure_message = None
        srvc.Foo(rpc_controller, unittest_pb2.FooRequest(), MyCallback)
        self.assertEqual(None, rpc_controller.failure_message)
        self.assertEqual(True, srvc.foo_called)
        rpc_controller.failure_message = None
        srvc.CallMethod(service_descriptor.methods[1], rpc_controller, unittest_pb2.BarRequest(), MyCallback)
        self.assertEqual(None, rpc_controller.failure_message)
        self.assertEqual(True, srvc.bar_called)

    def testServiceStub(self):

        class MockRpcChannel(service.RpcChannel):

            def CallMethod(self, method, controller, request, response_class, callback):
                self.method = method
                self.controller = controller
                self.request = request
                callback(response_class())

        self.callback_response = None

        def MyCallback(response):
            self.callback_response = response

        channel = MockRpcChannel()
        stub = unittest_pb2.TestService_Stub(channel)
        rpc_controller = 'controller'
        request = 'request'
        self.assertEqual(unittest_pb2.TestService_Stub.GetDescriptor(), stub.GetDescriptor())
        stub.Foo(rpc_controller, request, MyCallback)
        self.assertIsInstance(self.callback_response, unittest_pb2.FooResponse)
        self.assertEqual(request, channel.request)
        self.assertEqual(rpc_controller, channel.controller)
        self.assertEqual(stub.GetDescriptor().methods[0], channel.method)


if __name__ == '__main__':
    unittest.main()