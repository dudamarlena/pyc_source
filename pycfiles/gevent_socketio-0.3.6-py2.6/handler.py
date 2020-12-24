# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/socketio/handler.py
# Compiled at: 2014-02-03 00:13:04
import sys, re, gevent, urlparse
from gevent.pywsgi import WSGIHandler
from socketio import transports

class SocketIOHandler(WSGIHandler):
    RE_REQUEST_URL = re.compile('\n        ^/(?P<resource>.+?)\n         /1\n         /(?P<transport_id>[^/]+)\n         /(?P<sessid>[^/]+)/?$\n         ', re.X)
    RE_HANDSHAKE_URL = re.compile('^/(?P<resource>.+?)/1/$', re.X)
    RE_DISCONNECT_URL = re.compile('\n        ^/(?P<resource>.+?)\n         /(?P<protocol_version>[^/]+)\n         //(?P<sessid>[^/]+)/?$\n         ', re.X)
    handler_types = {'websocket': transports.WebsocketTransport, 
       'flashsocket': transports.FlashSocketTransport, 
       'htmlfile': transports.HTMLFileTransport, 
       'xhr-multipart': transports.XHRMultipartTransport, 
       'xhr-polling': transports.XHRPollingTransport, 
       'jsonp-polling': transports.JSONPolling}

    def __init__(self, config, *args, **kwargs):
        """Create a new SocketIOHandler.

        :param config: dict Configuration for timeouts and intervals
          that will go down to the other components, transports, etc..

        """
        self.socketio_connection = False
        self.allowed_paths = None
        self.config = config
        super(SocketIOHandler, self).__init__(*args, **kwargs)
        self.transports = self.handler_types.keys()
        if self.server.transports:
            self.transports = self.server.transports
            if not set(self.transports).issubset(set(self.handler_types)):
                raise ValueError('transports should be elements of: %s' % self.handler_types.keys())
        return

    def _do_handshake(self, tokens):
        if tokens['resource'] != self.server.resource:
            self.log_error('socket.io URL mismatch')
        else:
            socket = self.server.get_socket()
            data = '%s:%s:%s:%s' % (socket.sessid,
             self.config['heartbeat_timeout'] or '',
             self.config['close_timeout'] or '',
             (',').join(self.transports))
            self.write_smart(data)

    def write_jsonp_result(self, data, wrapper='0'):
        self.start_response('200 OK', [
         ('Content-Type', 'application/javascript')])
        self.result = [
         'io.j[%s]("%s");' % (wrapper, data)]

    def write_plain_result(self, data):
        self.start_response('200 OK', [
         (
          'Access-Control-Allow-Origin', self.environ.get('HTTP_ORIGIN', '*')),
         ('Access-Control-Allow-Credentials', 'true'),
         ('Access-Control-Allow-Methods', 'POST, GET, OPTIONS'),
         ('Access-Control-Max-Age', 3600),
         ('Content-Type', 'text/plain')])
        self.result = [
         data]

    def write_smart(self, data):
        args = urlparse.parse_qs(self.environ.get('QUERY_STRING'))
        if 'jsonp' in args:
            self.write_jsonp_result(data, args['jsonp'][0])
        else:
            self.write_plain_result(data)
        self.process_result()

    def handle_one_response(self):
        """This function deals with *ONE INCOMING REQUEST* from the web.

        It will wire and exchange message to the queues for long-polling
        methods, otherwise, will stay alive for websockets.

        """
        path = self.environ.get('PATH_INFO')
        if not path.lstrip('/').startswith(self.server.resource + '/'):
            return super(SocketIOHandler, self).handle_one_response()
        else:
            self.status = None
            self.headers_sent = False
            self.result = None
            self.response_length = 0
            self.response_use_chunked = False
            request_method = self.environ.get('REQUEST_METHOD')
            request_tokens = self.RE_REQUEST_URL.match(path)
            handshake_tokens = self.RE_HANDSHAKE_URL.match(path)
            disconnect_tokens = self.RE_DISCONNECT_URL.match(path)
            if handshake_tokens:
                return self._do_handshake(handshake_tokens.groupdict())
            if disconnect_tokens:
                tokens = disconnect_tokens.groupdict()
            elif request_tokens:
                tokens = request_tokens.groupdict()
            else:
                return super(SocketIOHandler, self).handle_one_response()
            sessid = tokens['sessid']
            socket = self.server.get_socket(sessid)
            if not socket:
                self.handle_bad_request()
                return []
            if self.environ['QUERY_STRING'].startswith('disconnect'):
                socket.disconnect()
                self.handle_disconnect_request()
                return []
            transport = self.handler_types.get(tokens['transport_id'])
            old_class = None
            if issubclass(transport, (transports.WebsocketTransport,
             transports.FlashSocketTransport)):
                old_class = self.__class__
                self.__class__ = self.server.ws_handler_class
                self.prevent_wsgi_call = True
                self.handle_one_response()
            self.environ['socketio'] = socket
            self.transport = transport(self, self.config)
            self.transport.do_exchange(socket, request_method)
            if not socket.connection_established:
                socket.connection_established = True
                socket.state = socket.STATE_CONNECTED
                socket._spawn_heartbeat()
                socket._spawn_watcher()
                try:
                    if socket.wsgi_app_greenlet is None:
                        start_response = lambda status, headers, exc=None: None
                        socket.wsgi_app_greenlet = gevent.spawn(self.application, self.environ, start_response)
                except:
                    self.handle_error(*sys.exc_info())

            if tokens['transport_id'] in ('flashsocket', 'websocket'):
                gevent.joinall(socket.jobs)
            if old_class:
                self.__class__ = old_class
            if hasattr(self, 'websocket') and self.websocket:
                if hasattr(self.websocket, 'environ'):
                    del self.websocket.environ
                del self.websocket
            if self.environ:
                del self.environ
            return

    def handle_bad_request(self):
        self.close_connection = True
        self.start_response('400 Bad Request', [
         ('Content-Type', 'text/plain'),
         ('Connection', 'close'),
         ('Content-Length', 0)])

    def handle_disconnect_request(self):
        self.close_connection = True
        self.start_response('200 OK', [
         ('Content-Type', 'text/plain'),
         ('Connection', 'close'),
         ('Content-Length', 0)])