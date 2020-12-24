# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-i386/egg/typhoonae/channel/tests/test_channel.py
# Compiled at: 2010-12-12 04:36:57
"""Unit tests for the Channel API and TyphoonAE's service stub."""
from google.appengine.api import apiproxy_stub_map
from google.appengine.api import channel
from google.appengine.runtime import apiproxy_errors
from typhoonae.channel import channel_service_stub
import BaseHTTPServer, SimpleHTTPServer, cgi, httplib, os, threading, unittest

class StoppableHttpRequestHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):
    """HTTP request handler with QUIT stopping the server."""

    def do_POST(self):
        length = int(self.headers.getheader('content-length'))
        qs = self.rfile.read(length)
        params = cgi.parse_qs(qs, keep_blank_values=1)
        self.server.buf.append(params)

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
    buf = []

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


class ChannelTestCase(unittest.TestCase):
    """Testing the Channel API."""

    def setUp(self):
        """Register TyphoonAE's Channel API proxy stub."""
        os.environ['SERVER_SOFTWARE'] = 'Development'
        apiproxy_stub_map.apiproxy = apiproxy_stub_map.APIProxyStubMap()
        apiproxy_stub_map.apiproxy.RegisterStub('channel', channel_service_stub.ChannelServiceStub('localhost:9876'))

    def test_stub(self):
        """Tests whether the stub is correctly registered."""
        stub = apiproxy_stub_map.apiproxy.GetStub('channel')
        self.assertEqual(channel_service_stub.ChannelServiceStub, stub.__class__)

    def test_create_channel(self):
        """Creates a channel."""
        self.assertEqual('testchannel', channel.create_channel('testchannel'))
        self.assertRaises(channel.InvalidChannelClientIdError, channel.create_channel, '')

    def test_send_message(self):
        """Sends a channel message."""
        server = StoppableHttpServer(('localhost', 9876), StoppableHttpRequestHandler)
        server_thread = threading.Thread(target=server.serve_forever)
        server_thread.setDaemon(True)
        server_thread.start()
        channel.send_message('testchannel', 'Hello, World!')
        self.assertRaises(channel.InvalidMessageError, channel.send_message, 'testchannel', '')
        stop_server(9876)
        buf = server.buf
        self.assertEqual("[{'Hello, World!': ['']}]", str(buf))