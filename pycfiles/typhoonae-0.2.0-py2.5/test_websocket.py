# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-i386/egg/typhoonae/websocket/tests/test_websocket.py
# Compiled at: 2010-12-12 04:36:57
"""Unit tests for TyphoonAE's WebSocket API and service stub."""
import google.appengine.api.apiproxy_stub_map, google.appengine.api.urlfetch_stub, os, typhoonae.websocket, typhoonae.websocket.websocket_stub, unittest

class WebSocketTestCase(unittest.TestCase):
    """Testing the WebSocket API."""

    def setUp(self):
        """Register TyphoonAE's WebSocket API proxy stub."""
        os.environ.update({'SERVER_NAME': 'host', 
           'APPLICATION_ID': 'app'})
        google.appengine.api.apiproxy_stub_map.apiproxy = google.appengine.api.apiproxy_stub_map.APIProxyStubMap()
        google.appengine.api.apiproxy_stub_map.apiproxy.RegisterStub('websocket', typhoonae.websocket.websocket_stub.WebSocketServiceStub())
        google.appengine.api.apiproxy_stub_map.apiproxy.RegisterStub('urlfetch', google.appengine.api.urlfetch_stub.URLFetchServiceStub())

    def test_stub(self):
        """Tests whether the stub is correctly registered."""
        stub = google.appengine.api.apiproxy_stub_map.apiproxy.GetStub('websocket')
        self.assertEqual(typhoonae.websocket.websocket_stub.WebSocketServiceStub, stub.__class__)
        self.assertRaises(typhoonae.websocket.websocket_stub.ConfigurationError, stub._GetEnviron, 'unknown')

    def test_create_websocket_url(self):
        """Tries to obtain a valid Web Socket URL."""
        self.assertEqual('ws://host:8888/YXBw/', typhoonae.websocket.create_websocket_url())
        self.assertEqual('ws://host:8888/YXBw/foo', typhoonae.websocket.create_websocket_url('/foo'))

    def test_message(self):
        """Simply cretes a Web Socket message instance."""
        message = typhoonae.websocket.Message({'from': 0, 'body': 'Message body'})
        self.assertEqual(0, message.socket)
        self.assertEqual('Message body', message.body)

    def test_send_message(self):
        """Sends a message to a Web Socket."""
        typhoonae.websocket.send_message('1', 'My first message.')
        self.assertRaises(typhoonae.websocket.BadArgumentError, typhoonae.websocket.send_message, 1, 'My second message.')
        self.assertRaises(typhoonae.websocket.BadArgumentError, typhoonae.websocket.send_message, [None], 'My second message.')
        return

    def test_broadcast_message(self):
        """Sends a broadcast message request to the Web Socket service."""
        typhoonae.websocket.broadcast_message('My broadcast message.')