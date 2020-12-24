# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\supervisor\tests\test_xmlrpc.py
# Compiled at: 2015-07-18 10:13:57
import unittest
from supervisor.tests.base import DummySupervisor
from supervisor.tests.base import DummyRequest
from supervisor.tests.base import DummySupervisorRPCNamespace
from supervisor.compat import xmlrpclib
from supervisor.compat import httplib

class GetFaultDescriptionTests(unittest.TestCase):

    def test_returns_description_for_known_fault(self):
        from supervisor import xmlrpc
        desc = xmlrpc.getFaultDescription(xmlrpc.Faults.SHUTDOWN_STATE)
        self.assertEqual(desc, 'SHUTDOWN_STATE')

    def test_returns_unknown_for_unknown_fault(self):
        from supervisor import xmlrpc
        desc = xmlrpc.getFaultDescription(999999)
        self.assertEqual(desc, 'UNKNOWN')


class RPCErrorTests(unittest.TestCase):

    def _getTargetClass(self):
        from supervisor.xmlrpc import RPCError
        return RPCError

    def _makeOne(self, code, extra=None):
        return self._getTargetClass()(code, extra)

    def test_sets_text_with_fault_name_only(self):
        from supervisor import xmlrpc
        e = self._makeOne(xmlrpc.Faults.FAILED)
        self.assertEqual(e.text, 'FAILED')

    def test_sets_text_with_fault_name_and_extra(self):
        from supervisor import xmlrpc
        e = self._makeOne(xmlrpc.Faults.FAILED, 'oops')
        self.assertEqual(e.text, 'FAILED: oops')


class XMLRPCMarshallingTests(unittest.TestCase):

    def test_xmlrpc_marshal(self):
        from supervisor import xmlrpc
        data = xmlrpc.xmlrpc_marshal(1)
        self.assertEqual(data, xmlrpclib.dumps((1, ), methodresponse=True))
        fault = xmlrpclib.Fault(1, 'foo')
        data = xmlrpc.xmlrpc_marshal(fault)
        self.assertEqual(data, xmlrpclib.dumps(fault))


class XMLRPCHandlerTests(unittest.TestCase):

    def _getTargetClass(self):
        from supervisor.xmlrpc import supervisor_xmlrpc_handler
        return supervisor_xmlrpc_handler

    def _makeOne(self, supervisord, subinterfaces):
        return self._getTargetClass()(supervisord, subinterfaces)

    def test_ctor(self):
        supervisor = DummySupervisor()
        subinterfaces = [('supervisor', DummySupervisorRPCNamespace())]
        handler = self._makeOne(supervisor, subinterfaces)
        self.assertEqual(handler.supervisord, supervisor)
        from supervisor.xmlrpc import RootRPCInterface
        self.assertEqual(handler.rpcinterface.__class__, RootRPCInterface)

    def test_match(self):

        class DummyRequest2:

            def __init__(self, uri):
                self.uri = uri

        supervisor = DummySupervisor()
        subinterfaces = [('supervisor', DummySupervisorRPCNamespace())]
        handler = self._makeOne(supervisor, subinterfaces)
        self.assertEqual(handler.match(DummyRequest2('/RPC2')), True)
        self.assertEqual(handler.match(DummyRequest2('/nope')), False)

    def test_continue_request_nosuchmethod(self):
        supervisor = DummySupervisor()
        subinterfaces = [('supervisor', DummySupervisorRPCNamespace())]
        handler = self._makeOne(supervisor, subinterfaces)
        data = xmlrpclib.dumps(('a', 'b'), 'supervisor.noSuchMethod')
        request = DummyRequest('/what/ever', None, None, None)
        handler.continue_request(data, request)
        logdata = supervisor.options.logger.data
        self.assertEqual(len(logdata), 2)
        self.assertEqual(logdata[(-2)], 'XML-RPC method called: supervisor.noSuchMethod()')
        self.assertEqual(logdata[(-1)], 'XML-RPC method supervisor.noSuchMethod() returned fault: [1] UNKNOWN_METHOD')
        self.assertEqual(len(request.producers), 1)
        xml_response = request.producers[0]
        self.assertRaises(xmlrpclib.Fault, xmlrpclib.loads, xml_response)
        return

    def test_continue_request_methodsuccess(self):
        supervisor = DummySupervisor()
        subinterfaces = [('supervisor', DummySupervisorRPCNamespace())]
        handler = self._makeOne(supervisor, subinterfaces)
        data = xmlrpclib.dumps((), 'supervisor.getAPIVersion')
        request = DummyRequest('/what/ever', None, None, None)
        handler.continue_request(data, request)
        logdata = supervisor.options.logger.data
        self.assertEqual(len(logdata), 2)
        self.assertEqual(logdata[(-2)], 'XML-RPC method called: supervisor.getAPIVersion()')
        self.assertEqual(logdata[(-1)], 'XML-RPC method supervisor.getAPIVersion() returned successfully')
        self.assertEqual(len(request.producers), 1)
        xml_response = request.producers[0]
        response = xmlrpclib.loads(xml_response)
        from supervisor.rpcinterface import API_VERSION
        self.assertEqual(response[0][0], API_VERSION)
        self.assertEqual(request._done, True)
        self.assertEqual(request.headers['Content-Type'], 'text/xml')
        self.assertEqual(request.headers['Content-Length'], len(xml_response))
        return

    def test_continue_request_no_params_in_request(self):
        supervisor = DummySupervisor()
        subinterfaces = [('supervisor', DummySupervisorRPCNamespace())]
        handler = self._makeOne(supervisor, subinterfaces)
        data = '<?xml version="1.0" encoding="UTF-8"?><methodCall><methodName>supervisor.getAPIVersion</methodName></methodCall>'
        request = DummyRequest('/what/ever', None, None, None)
        handler.continue_request(data, request)
        logdata = supervisor.options.logger.data
        self.assertEqual(len(logdata), 2)
        self.assertEqual(logdata[(-2)], 'XML-RPC method called: supervisor.getAPIVersion()')
        self.assertEqual(logdata[(-1)], 'XML-RPC method supervisor.getAPIVersion() returned successfully')
        self.assertEqual(len(request.producers), 1)
        xml_response = request.producers[0]
        response = xmlrpclib.loads(xml_response)
        from supervisor.rpcinterface import API_VERSION
        self.assertEqual(response[0][0], API_VERSION)
        self.assertEqual(request._done, True)
        self.assertEqual(request.headers['Content-Type'], 'text/xml')
        self.assertEqual(request.headers['Content-Length'], len(xml_response))
        return

    def test_continue_request_400_if_method_name_is_empty(self):
        supervisor = DummySupervisor()
        subinterfaces = [('supervisor', DummySupervisorRPCNamespace())]
        handler = self._makeOne(supervisor, subinterfaces)
        data = '<?xml version="1.0" encoding="UTF-8"?><methodCall><methodName></methodName></methodCall>'
        request = DummyRequest('/what/ever', None, None, None)
        handler.continue_request(data, request)
        logdata = supervisor.options.logger.data
        self.assertEqual(len(logdata), 1)
        self.assertEqual(logdata[(-1)], 'XML-RPC request received with no method name')
        self.assertEqual(len(request.producers), 0)
        self.assertEqual(request._error, 400)
        return

    def test_continue_request_500(self):
        supervisor = DummySupervisor()
        subinterfaces = [('supervisor', DummySupervisorRPCNamespace())]
        handler = self._makeOne(supervisor, subinterfaces)
        data = xmlrpclib.dumps((), 'supervisor.raiseError')
        request = DummyRequest('/what/ever', None, None, None)
        handler.continue_request(data, request)
        logdata = supervisor.options.logger.data
        self.assertEqual(len(logdata), 2)
        self.assertEqual(logdata[(-2)], 'XML-RPC method called: supervisor.raiseError()')
        self.assertTrue(logdata[(-1)].startswith('Traceback'))
        self.assertTrue(logdata[(-1)].endswith('ValueError: error\n'))
        self.assertEqual(len(request.producers), 0)
        self.assertEqual(request._error, 500)
        return

    def test_continue_request_value_is_function(self):

        class DummyRPCNamespace(object):

            def foo(self):

                def inner(self):
                    return 1

                inner.delay = 0.05
                return inner

        supervisor = DummySupervisor()
        subinterfaces = [('supervisor', DummySupervisorRPCNamespace()),
         (
          'ns1', DummyRPCNamespace())]
        handler = self._makeOne(supervisor, subinterfaces)
        data = xmlrpclib.dumps((), 'ns1.foo')
        request = DummyRequest('/what/ever', None, None, None)
        handler.continue_request(data, request)
        logdata = supervisor.options.logger.data
        self.assertEqual(len(logdata), 2)
        self.assertEqual(logdata[(-2)], 'XML-RPC method called: ns1.foo()')
        self.assertEqual(logdata[(-1)], 'XML-RPC method ns1.foo() returned successfully')
        self.assertEqual(len(request.producers), 0)
        self.assertEqual(request._done, False)
        return

    def test_iterparse_loads_methodcall(self):
        s = '<?xml version="1.0"?>\n        <methodCall>\n        <methodName>examples.getStateName</methodName>\n        <params>\n        <param>\n        <value><i4>41</i4></value>\n        </param>\n        <param>\n        <value><string>foo</string></value>\n        </param>\n        <param>\n        <value><string></string></value>\n        </param>\n        <param>\n        <!-- xml-rpc spec allows strings without <string> tag -->\n        <value>bar</value>\n        </param>\n        <param>\n        <value></value>\n        </param>\n        <param>\n        <value><boolean>1</boolean></value>\n        </param>\n        <param>\n        <value><double>-12.214</double></value>\n        </param>\n        <param>\n        <value>\n        <dateTime.iso8601>19980717T14:08:55</dateTime.iso8601>\n        </value>\n        </param>\n        <param>\n        <value><base64>eW91IGNhbid0IHJlYWQgdGhpcyE=</base64></value>\n        </param>\n        <param>\n        <struct>\n        <member><name>j</name><value><i4>5</i4></value></member>\n        <member><name>k</name><value>abc</value></member>\n        </struct>\n        </param>\n        <param>\n        <array>\n          <data>\n            <value><i4>12</i4></value>\n            <value><string>abc</string></value>\n            <value>def</value>\n            <value><i4>34</i4></value>\n          </data>\n        </array>\n        </param>\n        <param>\n        <struct>\n          <member>\n            <name>k</name>\n            <value><array><data>\n              <value><i4>1</i4></value>\n              <struct></struct>\n            </data></array></value>\n          </member>\n        </struct>\n        </param>\n        </params>\n        </methodCall>\n        '
        supervisor = DummySupervisor()
        subinterfaces = [('supervisor', DummySupervisorRPCNamespace())]
        handler = self._makeOne(supervisor, subinterfaces)
        result = handler.loads(s)
        params, method = result
        import datetime
        self.assertEqual(method, 'examples.getStateName')
        self.assertEqual(params[0], 41)
        self.assertEqual(params[1], 'foo')
        self.assertEqual(params[2], '')
        self.assertEqual(params[3], 'bar')
        self.assertEqual(params[4], '')
        self.assertEqual(params[5], True)
        self.assertEqual(params[6], -12.214)
        self.assertEqual(params[7], datetime.datetime(1998, 7, 17, 14, 8, 55))
        self.assertEqual(params[8], "you can't read this!")
        self.assertEqual(params[9], {'j': 5, 'k': 'abc'})
        self.assertEqual(params[10], [12, 'abc', 'def', 34])
        self.assertEqual(params[11], {'k': [1, {}]})


class TraverseTests(unittest.TestCase):

    def test_underscore(self):
        from supervisor import xmlrpc
        self.assertRaises(xmlrpc.RPCError, xmlrpc.traverse, None, '_', None)
        return

    def test_notfound(self):
        from supervisor import xmlrpc
        self.assertRaises(xmlrpc.RPCError, xmlrpc.traverse, None, 'foo', None)
        return

    def test_badparams(self):
        from supervisor import xmlrpc
        self.assertRaises(xmlrpc.RPCError, xmlrpc.traverse, self, 'test_badparams', (1,
                                                                                     2,
                                                                                     3))

    def test_success(self):
        from supervisor import xmlrpc
        L = []

        class Dummy:

            def foo(self, a):
                L.append(a)

        dummy = Dummy()
        xmlrpc.traverse(dummy, 'foo', [1])
        self.assertEqual(L, [1])


class SupervisorTransportTests(unittest.TestCase):

    def _getTargetClass(self):
        from supervisor.xmlrpc import SupervisorTransport
        return SupervisorTransport

    def _makeOne(self, *arg, **kw):
        return self._getTargetClass()(*arg, **kw)

    def test_ctor_unix(self):
        from supervisor import xmlrpc
        transport = self._makeOne('user', 'pass', 'unix:///foo/bar')
        conn = transport._get_connection()
        self.assertTrue(isinstance(conn, xmlrpc.UnixStreamHTTPConnection))
        self.assertEqual(conn.host, 'localhost')
        self.assertEqual(conn.socketfile, '/foo/bar')

    def test_ctor_unknown(self):
        self.assertRaises(ValueError, self._makeOne, 'user', 'pass', 'unknown:///foo/bar')

    def test__get_connection_http_9001(self):
        transport = self._makeOne('user', 'pass', 'http://127.0.0.1:9001/')
        conn = transport._get_connection()
        self.assertTrue(isinstance(conn, httplib.HTTPConnection))
        self.assertEqual(conn.host, '127.0.0.1')
        self.assertEqual(conn.port, 9001)

    def test__get_connection_http_80(self):
        transport = self._makeOne('user', 'pass', 'http://127.0.0.1/')
        conn = transport._get_connection()
        self.assertTrue(isinstance(conn, httplib.HTTPConnection))
        self.assertEqual(conn.host, '127.0.0.1')
        self.assertEqual(conn.port, 80)

    def test_request_non_200_response(self):
        transport = self._makeOne('user', 'pass', 'http://127.0.0.1/')
        dummy_conn = DummyConnection(400, '')

        def getconn():
            return dummy_conn

        transport._get_connection = getconn
        self.assertRaises(xmlrpclib.ProtocolError, transport.request, 'localhost', '/', '')
        self.assertEqual(transport.connection, None)
        self.assertEqual(dummy_conn.closed, True)
        return

    def test_request_400_response(self):
        transport = self._makeOne('user', 'pass', 'http://127.0.0.1/')
        dummy_conn = DummyConnection(400, '')

        def getconn():
            return dummy_conn

        transport._get_connection = getconn
        self.assertRaises(xmlrpclib.ProtocolError, transport.request, 'localhost', '/', '')
        self.assertEqual(transport.connection, None)
        self.assertEqual(dummy_conn.closed, True)
        self.assertEqual(dummy_conn.requestargs[0], 'POST')
        self.assertEqual(dummy_conn.requestargs[1], '/')
        self.assertEqual(dummy_conn.requestargs[2], '')
        self.assertEqual(dummy_conn.requestargs[3]['Content-Length'], '0')
        self.assertEqual(dummy_conn.requestargs[3]['Content-Type'], 'text/xml')
        self.assertEqual(dummy_conn.requestargs[3]['Authorization'], 'Basic dXNlcjpwYXNz')
        self.assertEqual(dummy_conn.requestargs[3]['Accept'], 'text/xml')
        return

    def test_request_200_response(self):
        transport = self._makeOne('user', 'pass', 'http://127.0.0.1/')
        response = '<?xml version="1.0"?>\n        <methodResponse>\n        <params>\n        <param>\n        <value><string>South Dakota</string></value>\n        </param>\n        </params>\n        </methodResponse>'
        dummy_conn = DummyConnection(200, response)

        def getconn():
            return dummy_conn

        transport._get_connection = getconn
        result = transport.request('localhost', '/', '')
        self.assertEqual(transport.connection, dummy_conn)
        self.assertEqual(dummy_conn.closed, False)
        self.assertEqual(dummy_conn.requestargs[0], 'POST')
        self.assertEqual(dummy_conn.requestargs[1], '/')
        self.assertEqual(dummy_conn.requestargs[2], '')
        self.assertEqual(dummy_conn.requestargs[3]['Content-Length'], '0')
        self.assertEqual(dummy_conn.requestargs[3]['Content-Type'], 'text/xml')
        self.assertEqual(dummy_conn.requestargs[3]['Authorization'], 'Basic dXNlcjpwYXNz')
        self.assertEqual(dummy_conn.requestargs[3]['Accept'], 'text/xml')
        self.assertEqual(result, ('South Dakota', ))


class TestDeferredXMLRPCResponse(unittest.TestCase):

    def _getTargetClass(self):
        from supervisor.xmlrpc import DeferredXMLRPCResponse
        return DeferredXMLRPCResponse

    def _makeOne(self, request=None, callback=None):
        if request is None:
            request = DummyRequest(None, None, None, None, None)
        if callback is None:
            callback = Dummy()
            callback.delay = 1
        return self._getTargetClass()(request, callback)

    def test_ctor(self):
        callback = Dummy()
        callback.delay = 1
        inst = self._makeOne(request='request', callback=callback)
        self.assertEqual(inst.callback, callback)
        self.assertEqual(inst.delay, 1.0)
        self.assertEqual(inst.request, 'request')
        self.assertEqual(inst.finished, False)

    def test_more_finished(self):
        inst = self._makeOne()
        inst.finished = True
        result = inst.more()
        self.assertEqual(result, '')

    def test_more_callback_returns_not_done_yet(self):
        from supervisor.http import NOT_DONE_YET

        def callback():
            return NOT_DONE_YET

        callback.delay = 1
        inst = self._makeOne(callback=callback)
        self.assertEqual(inst.more(), NOT_DONE_YET)

    def test_more_callback_raises_RPCError(self):
        from supervisor.xmlrpc import RPCError, Faults

        def callback():
            raise RPCError(Faults.UNKNOWN_METHOD)

        callback.delay = 1
        inst = self._makeOne(callback=callback)
        self.assertEqual(inst.more(), None)
        self.assertEqual(len(inst.request.producers), 1)
        self.assertTrue('UNKNOWN_METHOD' in inst.request.producers[0])
        self.assertTrue(inst.finished)
        return

    def test_more_callback_returns_value(self):

        def callback():
            return 'abc'

        callback.delay = 1
        inst = self._makeOne(callback=callback)
        self.assertEqual(inst.more(), None)
        self.assertEqual(len(inst.request.producers), 1)
        self.assertTrue('abc' in inst.request.producers[0])
        self.assertTrue(inst.finished)
        return

    def test_more_callback_raises_unexpected_exception(self):

        def callback():
            raise ValueError('foo')

        callback.delay = 1
        inst = self._makeOne(callback=callback)
        self.assertEqual(inst.more(), None)
        self.assertEqual(inst.request._error, 500)
        self.assertTrue(inst.finished)
        logged = inst.request.channel.server.logger.logged
        self.assertEqual(len(logged), 1)
        src, msg = logged[0]
        self.assertEqual(src, 'XML-RPC response callback error')
        self.assertTrue('Traceback' in msg)
        return

    def test_getresponse_http_10_with_keepalive(self):
        inst = self._makeOne()
        inst.request.version = '1.0'
        inst.request.header.append('Connection: keep-alive')
        inst.getresponse('abc')
        self.assertEqual(len(inst.request.producers), 1)
        self.assertEqual(inst.request.headers['Connection'], 'Keep-Alive')

    def test_getresponse_http_10_no_keepalive(self):
        inst = self._makeOne()
        inst.request.version = '1.0'
        inst.getresponse('abc')
        self.assertEqual(len(inst.request.producers), 1)
        self.assertEqual(inst.request.headers['Connection'], 'close')

    def test_getresponse_http_11_without_close(self):
        inst = self._makeOne()
        inst.request.version = '1.1'
        inst.getresponse('abc')
        self.assertEqual(len(inst.request.producers), 1)
        self.assertTrue('Connection' not in inst.request.headers)

    def test_getresponse_http_11_with_close(self):
        inst = self._makeOne()
        inst.request.header.append('Connection: close')
        inst.request.version = '1.1'
        inst.getresponse('abc')
        self.assertEqual(len(inst.request.producers), 1)
        self.assertEqual(inst.request.headers['Connection'], 'close')

    def test_getresponse_http_unknown(self):
        inst = self._makeOne()
        inst.request.version = None
        inst.getresponse('abc')
        self.assertEqual(len(inst.request.producers), 1)
        self.assertEqual(inst.request.headers['Connection'], 'close')
        return


class TestSystemNamespaceRPCInterface(unittest.TestCase):

    def _makeOne(self, namespaces=()):
        from supervisor.xmlrpc import SystemNamespaceRPCInterface
        return SystemNamespaceRPCInterface(namespaces)

    def test_listMethods_gardenpath(self):
        inst = self._makeOne()
        result = inst.listMethods()
        self.assertEqual(result, [
         'system.listMethods',
         'system.methodHelp',
         'system.methodSignature',
         'system.multicall'])

    def test_listMethods_omits_underscore_attrs(self):

        class DummyNamespace(object):

            def foo(self):
                pass

            def _bar(self):
                pass

        ns1 = DummyNamespace()
        inst = self._makeOne([('ns1', ns1)])
        result = inst.listMethods()
        self.assertEqual(result, [
         'ns1.foo',
         'system.listMethods',
         'system.methodHelp',
         'system.methodSignature',
         'system.multicall'])

    def test_methodHelp_known_method(self):
        inst = self._makeOne()
        result = inst.methodHelp('system.listMethods')
        self.assertTrue('array' in result)

    def test_methodHelp_unknown_method(self):
        from supervisor.xmlrpc import RPCError
        inst = self._makeOne()
        self.assertRaises(RPCError, inst.methodHelp, 'wont.be.found')

    def test_methodSignature_known_method(self):
        inst = self._makeOne()
        result = inst.methodSignature('system.methodSignature')
        self.assertEqual(result, ['array', 'string'])

    def test_methodSignature_unknown_method(self):
        from supervisor.xmlrpc import RPCError
        inst = self._makeOne()
        self.assertRaises(RPCError, inst.methodSignature, 'wont.be.found')

    def test_methodSignature_with_bad_sig(self):
        from supervisor.xmlrpc import RPCError

        class DummyNamespace(object):

            def foo(self):
                """ @param string name The thing"""
                pass

        ns1 = DummyNamespace()
        inst = self._makeOne([('ns1', ns1)])
        self.assertRaises(RPCError, inst.methodSignature, 'ns1.foo')

    def test_multicall_recursion_forbidden(self):
        inst = self._makeOne()
        call = {'methodName': 'system.multicall'}
        multiproduce = inst.multicall([call])
        result = multiproduce()
        self.assertEqual(result, [{'faultCode': 2, 'faultString': 'INCORRECT_PARAMETERS'}])

    def test_multicall_other_exception(self):
        inst = self._makeOne()
        call = {}
        multiproduce = inst.multicall([call])
        result = multiproduce()
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['faultCode'], 1)

    def test_multicall_no_calls(self):
        inst = self._makeOne()
        multiproduce = inst.multicall([])
        result = multiproduce()
        self.assertEqual(result, [])

    def test_multicall_callback_raises_RPCError(self):
        from supervisor.xmlrpc import RPCError, Faults

        class DummyNamespace(object):

            def foo(self):
                """ @param string name The thing"""
                raise RPCError(Faults.UNKNOWN_METHOD)

        ns1 = DummyNamespace()
        inst = self._makeOne([('ns1', ns1)])
        multiproduce = inst.multicall([{'methodName': 'ns1.foo'}])
        result = multiproduce()
        self.assertEqual(result, [{'faultString': 'UNKNOWN_METHOD', 'faultCode': 1}])

    def test_multicall_callback_returns_function_returns_NOT_DONE_YET(self):
        from supervisor.http import NOT_DONE_YET

        class DummyNamespace(object):

            def __init__(self):
                self.results = [
                 NOT_DONE_YET, 1]

            def foo(self):
                """ @param string name The thing"""

                def inner():
                    return self.results.pop(0)

                return inner

        ns1 = DummyNamespace()
        inst = self._makeOne([('ns1', ns1)])
        multiproduce = inst.multicall([{'methodName': 'ns1.foo'}])
        result = multiproduce()
        self.assertEqual(result, NOT_DONE_YET)
        result = multiproduce()
        self.assertEqual(result, [
         1])

    def test_multicall_callback_returns_function_raises_RPCError(self):
        from supervisor.xmlrpc import Faults, RPCError

        class DummyNamespace(object):

            def foo(self):
                """ @param string name The thing"""

                def inner():
                    raise RPCError(Faults.UNKNOWN_METHOD)

                return inner

        ns1 = DummyNamespace()
        inst = self._makeOne([('ns1', ns1)])
        multiproduce = inst.multicall([{'methodName': 'ns1.foo'}])
        result = multiproduce()
        self.assertEqual(result, [{'faultString': 'UNKNOWN_METHOD', 'faultCode': 1}])


class Test_gettags(unittest.TestCase):

    def _callFUT(self, comment):
        from supervisor.xmlrpc import gettags
        return gettags(comment)

    def test_one_atpart(self):
        lines = '@foo'
        result = self._callFUT(lines)
        self.assertEqual(result, [
         (0, None, None, None, ''), (0, 'foo', '', '', '')])
        return

    def test_two_atparts(self):
        lines = '@foo array'
        result = self._callFUT(lines)
        self.assertEqual(result, [
         (0, None, None, None, ''), (0, 'foo', 'array', '', '')])
        return

    def test_three_atparts(self):
        lines = '@foo array name'
        result = self._callFUT(lines)
        self.assertEqual(result, [
         (0, None, None, None, ''), (0, 'foo', 'array', 'name', '')])
        return

    def test_four_atparts(self):
        lines = '@foo array name text'
        result = self._callFUT(lines)
        self.assertEqual(result, [
         (0, None, None, None, ''), (0, 'foo', 'array', 'name', 'text')])
        return


class DummyResponse:

    def __init__(self, status=200, body='', reason='reason'):
        self.status = status
        self.body = body
        self.reason = reason

    def read(self):
        return self.body


class Dummy(object):
    pass


class DummyConnection:
    closed = False

    def __init__(self, status=200, body='', reason='reason'):
        self.response = DummyResponse(status, body, reason)

    def getresponse(self):
        return self.response

    def request(self, *arg, **kw):
        self.requestargs = arg
        self.requestkw = kw

    def close(self):
        self.closed = True