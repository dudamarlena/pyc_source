# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /usr/local/Cellar/python/2.7.10_2/Frameworks/Python.framework/Versions/2.7/lib/python2.7/site-packages/geventwebsocket/handler.py
# Compiled at: 2015-11-13 17:02:49
import base64, hashlib, six, warnings
from gevent.pywsgi import WSGIHandler
from .websocket import WebSocket, Stream
from .logging import create_logger

class Client(object):

    def __init__(self, address, ws):
        self.address = address
        self.ws = ws


class WebSocketHandler(WSGIHandler):
    """
    Automatically upgrades the connection to a websocket.

    To prevent the WebSocketHandler to call the underlying WSGI application,
    but only setup the WebSocket negotiations, do:

      mywebsockethandler.prevent_wsgi_call = True

    before calling run_application().  This is useful if you want to do more
    things before calling the app, and want to off-load the WebSocket
    negotiations to this library.  Socket.IO needs this for example, to send
    the 'ack' before yielding the control to your WSGI app.
    """
    SUPPORTED_VERSIONS = ('13', '8', '7')
    GUID = '258EAFA5-E914-47DA-95CA-C5AB0DC85B11'

    def run_websocket(self):
        """
        Called when a websocket has been created successfully.
        """
        if getattr(self, 'prevent_wsgi_call', False):
            return
        else:
            if not hasattr(self.server, 'clients'):
                self.server.clients = {}
            try:
                self.server.clients[self.client_address] = Client(self.client_address, self.websocket)
                self.application(self.environ, lambda s, h, e=None: [])
            finally:
                del self.server.clients[self.client_address]
                if not self.websocket.closed:
                    self.websocket.close()
                self.environ.update({'wsgi.websocket': None})
                self.websocket = None

            return

    def run_application(self):
        if hasattr(self.server, 'pre_start_hook') and self.server.pre_start_hook:
            self.logger.debug('Calling pre-start hook')
            if self.server.pre_start_hook(self):
                return super(WebSocketHandler, self).run_application()
        self.logger.debug('Initializing WebSocket')
        self.result = self.upgrade_websocket()
        if hasattr(self, 'websocket'):
            if self.status and not self.headers_sent:
                self.write('')
            self.run_websocket()
        else:
            if self.status:
                if not self.result:
                    self.result = []
                self.process_result()
                return
            else:
                return super(WebSocketHandler, self).run_application()

    def upgrade_websocket(self):
        """
        Attempt to upgrade the current environ into a websocket enabled
        connection. If successful, the environ dict with be updated with two
        new entries, `wsgi.websocket` and `wsgi.websocket_version`.

        :returns: Whether the upgrade was successful.
        """
        self.logger.debug('Validating WebSocket request')
        if self.environ.get('REQUEST_METHOD', '') != 'GET':
            self.logger.debug('Can only upgrade connection if using GET method.')
            return
        else:
            upgrade = self.environ.get('HTTP_UPGRADE', '').lower()
            if upgrade == 'websocket':
                connection = self.environ.get('HTTP_CONNECTION', '').lower()
                if 'upgrade' not in connection:
                    self.logger.warning("Client didn't ask for a connection upgrade")
                    return
            else:
                return
            if self.request_version != 'HTTP/1.1':
                self.start_response('402 Bad Request', [])
                self.logger.warning('Bad server protocol in headers')
                return [
                 'Bad protocol version']
            if self.environ.get('HTTP_SEC_WEBSOCKET_VERSION'):
                return self.upgrade_connection()
            self.logger.warning('No protocol defined')
            self.start_response('426 Upgrade Required', [
             (
              'Sec-WebSocket-Version', (', ').join(self.SUPPORTED_VERSIONS))])
            return [
             'No Websocket protocol version defined']

    def upgrade_connection(self):
        """
        Validate and 'upgrade' the HTTP request to a WebSocket request.

        If an upgrade succeeded then then handler will have `start_response`
        with a status of `101`, the environ will also be updated with
        `wsgi.websocket` and `wsgi.websocket_version` keys.

        :param environ: The WSGI environ dict.
        :param start_response: The callable used to start the response.
        :param stream: File like object that will be read from/written to by
            the underlying WebSocket object, if created.
        :return: The WSGI response iterator is something went awry.
        """
        self.logger.debug('Attempting to upgrade connection')
        version = self.environ.get('HTTP_SEC_WEBSOCKET_VERSION')
        if version not in self.SUPPORTED_VERSIONS:
            msg = ('Unsupported WebSocket Version: {0}').format(version)
            self.logger.warning(msg)
            self.start_response('400 Bad Request', [
             (
              'Sec-WebSocket-Version', (', ').join(self.SUPPORTED_VERSIONS))])
            return [
             msg]
        else:
            key = self.environ.get('HTTP_SEC_WEBSOCKET_KEY', '').strip()
            if not key:
                msg = 'Sec-WebSocket-Key header is missing/empty'
                self.logger.warning(msg)
                self.start_response('400 Bad Request', [])
                return [
                 msg]
            try:
                key_len = len(base64.b64decode(key))
            except TypeError:
                msg = ('Invalid key: {0}').format(key)
                self.logger.warning(msg)
                self.start_response('400 Bad Request', [])
                return [
                 msg]

            if key_len != 16:
                msg = ('Invalid key: {0}').format(key)
                self.logger.warning(msg)
                self.start_response('400 Bad Request', [])
                return [
                 msg]
            requested_protocols = self.environ.get('HTTP_SEC_WEBSOCKET_PROTOCOL', '')
            protocol = None
            if hasattr(self.application, 'app_protocol'):
                allowed_protocol = self.application.app_protocol(self.environ['PATH_INFO'])
                if allowed_protocol and allowed_protocol in requested_protocols:
                    protocol = allowed_protocol
                    self.logger.debug(('Protocol allowed: {0}').format(protocol))
            self.websocket = WebSocket(self.environ, Stream(self), self)
            self.environ.update({'wsgi.websocket_version': version, 
               'wsgi.websocket': self.websocket})
            sec_accept = base64.b64encode(hashlib.sha1(six.b(key + self.GUID)).digest())
            if six.PY3:
                sec_accept = sec_accept.decode('utf-8')
            headers = [('Upgrade', 'websocket'),
             ('Connection', 'Upgrade'),
             (
              'Sec-WebSocket-Accept', sec_accept)]
            if protocol:
                headers.append(('Sec-WebSocket-Protocol', protocol))
            self.logger.debug('WebSocket request accepted, switching protocols')
            self.start_response('101 Switching Protocols', headers)
            return

    @property
    def logger(self):
        if not hasattr(self.server, 'logger'):
            self.server.logger = create_logger(__name__)
        return self.server.logger

    def log_request(self):
        if '101' not in self.status.decode('utf-8'):
            self.logger.info(self.format_request())

    @property
    def active_client(self):
        return self.server.clients[self.client_address]

    def start_response(self, status, headers, exc_info=None):
        """
        Called when the handler is ready to send a response back to the remote
        endpoint. A websocket connection may have not been created.
        """
        writer = super(WebSocketHandler, self).start_response(status, headers, exc_info=exc_info)
        self._prepare_response()
        return writer

    def _prepare_response(self):
        """
        Sets up the ``pywsgi.Handler`` to work with a websocket response.

        This is used by other projects that need to support WebSocket
        connections as part of a larger effort.
        """
        if not not self.headers_sent:
            raise AssertionError
            return self.environ.get('wsgi.websocket') or None
        self.provided_content_length = False
        self.response_use_chunked = False
        self.close_connection = True
        self.provided_date = True