# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-i386/egg/typhoonae/websocket/websocket_stub.py
# Compiled at: 2010-12-12 04:36:57
"""TyphoonAE's WebSocket service stub."""
from typhoonae import websocket
from typhoonae.websocket import websocket_service_pb2
import base64, google.appengine.api.apiproxy_stub, httplib, logging, os, re
__all__ = [
 'Error',
 'ConfigurationError',
 'WebSocketServiceStub']

class Error(Exception):
    """Base websocket error type."""
    pass


class ConfigurationError(Error):
    """Raised when environment is not correctly configured."""
    pass


class WebSocketServiceStub(google.appengine.api.apiproxy_stub.APIProxyStub):
    """TyphoonAE's WebSocket service stub."""

    def __init__(self, service_name='websocket', port=8888):
        """Constructor.

        Args:
            service_name: Service name expected for all calls.
            port: Port number of the Web Socket service.
        """
        super(WebSocketServiceStub, self).__init__(service_name)
        self._port = port

    def _GetAddress(self):
        """Returns service address."""
        return '%s:%s' % (self._GetEnviron('SERVER_NAME'), self._port)

    @staticmethod
    def _GetEnviron(name):
        """Helper method ensures environment configured as expected.

        Args:
            name: Name of environment variable to get.

        Returns:
            Environment variable associated with name.

        Raises:
            ConfigurationError if required environment variable is not found.
        """
        try:
            return os.environ[name]
        except KeyError:
            raise ConfigurationError('%s is not set in environment.' % name)

    def _Dynamic_CreateWebSocketURL(self, request, response):
        """Implementation of WebSocketService::create_websocket_url().

        Args:
            request: A fully initialized CreateWebSocketURLRequest instance.
            response: A CreateWebSocketURLResponse instance.
        """
        url_parts = dict(protocol='ws', host=self._GetEnviron('SERVER_NAME'), port=self._port, app_key=base64.b64encode(self._GetEnviron('APPLICATION_ID')), success_path=re.sub('^/', '', request.success_path))
        response.url = websocket.WEBSOCKET_HANDLER_URL % url_parts

    def _SendMessage(self, body, socket, broadcast=False):
        """Sends a Web Socket message.

        Args:
            body: The message body.
            socket: A socket.
            broadcast: This flag determines whether a message should be sent to
                all active sockets but the sender.
        """
        path = 'message'
        if broadcast:
            path = 'broadcast'
        conn = httplib.HTTPConnection(self._GetAddress())
        headers = {websocket.WEBSOCKET_HEADER: str(socket), 'X-TyphoonAE-AppId': self._GetEnviron('APPLICATION_ID'), 
           'Content-Type': 'text/plain'}
        try:
            try:
                conn.request('POST', '/' + path, body.encode('utf-8'), headers)
            except:
                status = websocket_service_pb2.WebSocketMessageResponse.OTHER_ERROR

        finally:
            conn.close()

        status = websocket_service_pb2.WebSocketMessageResponse.NO_ERROR
        return status

    def _Dynamic_SendMessage(self, request, response):
        """Implementation of WebSocketService::send_message().

        Args:
            request: A WebSocketMessageRequest instance.
            response: A WebSocketMessageResponse instance.
        """
        status = self._SendMessage(request.message.body, request.message.socket)
        response.status.code = status

    def _Dynamic_BroadcastMessage(self, request, response):
        """Implementation of WebSocketService::broadcast_message().

        Args:
            request: A WebSocketMessageRequest instance.
            response: A WebSocketMessageResponse instance.
        """
        status = self._SendMessage(request.message.body, None, broadcast=True)
        response.status.code = status
        return