# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-i386/egg/typhoonae/xmpp/tests/test_xmpp.py
# Compiled at: 2010-12-12 04:36:57
"""Unit tests for the XMPP service."""
import BaseHTTPServer, SimpleHTTPServer, google.appengine.api.apiproxy_stub_map, google.appengine.api.urlfetch_stub, google.appengine.api, cgi, httplib, os, threading, typhoonae.xmpp.xmpp_http_dispatch, typhoonae.xmpp.xmpp_service_stub, unittest, xmpp

class XmppServiceTestCase(unittest.TestCase):
    """Testing the XMPP service API proxy stub."""

    def setUp(self):
        """Register TyphoonAE's XMPP service API proxy stub."""
        google.appengine.api.apiproxy_stub_map.apiproxy = google.appengine.api.apiproxy_stub_map.APIProxyStubMap()
        google.appengine.api.apiproxy_stub_map.apiproxy.RegisterStub('xmpp', typhoonae.xmpp.xmpp_service_stub.XmppServiceStub())
        os.environ['APPLICATION_ID'] = 'testapp'

    def test_stub(self):
        """Tests whether the stub is correctly registered."""
        stub = google.appengine.api.apiproxy_stub_map.apiproxy.GetStub('xmpp')
        self.assertEqual(typhoonae.xmpp.xmpp_service_stub.XmppServiceStub, stub.__class__)

    def testGetPresence(self):
        """Tests getting presence for a JID."""
        self.assertTrue(google.appengine.api.xmpp.get_presence('you@net', 'me@net'))

    def testSendMessage(self):
        """Sends a message."""
        self.assertRaises(xmpp.HostUnknown, google.appengine.api.xmpp.send_message, [
         'foo@bar'], 'Hello, World!')

    def testSendInvite(self):
        """Sends an invite."""
        self.assertRaises(xmpp.HostUnknown, google.appengine.api.xmpp.send_invite, [
         'foo@bar'], 'Hello, World!')


class StoppableHttpRequestHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):
    """HTTP request handler with QUIT stopping the server."""

    def do_POST(self):
        length = int(self.headers.getheader('content-length'))
        qs = self.rfile.read(length)
        params = cgi.parse_qs(qs, keep_blank_values=1)
        self.server.buffer.append(params)
        self.send_response(200)
        self.end_headers()

    def do_QUIT(self):
        """Sends 200 OK response, and sets server.stop to True."""
        self.send_response(200)
        self.end_headers()
        self.server.stop = True

    def log_request(self, *args):
        """Suppress any log messages for testing."""
        pass


class StoppableHttpServer(BaseHTTPServer.HTTPServer):
    """HTTP server that reacts to self.stop flag."""
    buffer = []

    def serve_forever(self):
        """Handles one request at a time until stopped."""
        self.stop = False
        while not self.stop:
            self.handle_request()


def stop_server(port):
    """Send QUIT request to HTTP server running on localhost:<port>."""
    conn = httplib.HTTPConnection('localhost:%d' % port)
    conn.request('QUIT', '/')
    conn.getresponse()
    conn.close()


class MockMessage(object):
    """A fake message class."""

    def getBody(self):
        return 'foo'

    def getFrom(self):
        return 'test@nowhere.net'

    def getTo(self):
        return 'recipient@nowhere.net'


class XmppHttpDispatcherTestCase(unittest.TestCase):
    """Testing the XMPP/HTTP dispatcher."""

    def testDispatcher(self):
        """Makes a call to our dispatcher."""
        server = StoppableHttpServer(('localhost', 9876), StoppableHttpRequestHandler)
        server_thread = threading.Thread(target=server.serve_forever)
        server_thread.setDaemon(True)
        server_thread.start()
        dispatcher = typhoonae.xmpp.xmpp_http_dispatch.Dispatcher('localhost:9876')
        message = MockMessage()
        dispatcher(None, message)
        assert 'test@nowhere.net' in str(server.buffer)
        typhoonae.xmpp.xmpp_http_dispatch.post_multipart('http://localhost:9876', [
         ('body', 'Some body contents.')])
        stop_server(9876)
        return

    def testPostMultipart(self):
        """Tries to post multipart form data."""
        typhoonae.xmpp.xmpp_http_dispatch.post_multipart('http://localhost:8765', [
         ('body', 'Some body contents.')])

    def testLoop(self):
        """Tests the main loop."""

        class MockConnection(object):
            _counter = 0

            @classmethod
            def Process(cls, i):
                if cls._counter > 0:
                    raise KeyboardInterrupt
                cls._counter += 1

        typhoonae.xmpp.xmpp_http_dispatch.loop(MockConnection())