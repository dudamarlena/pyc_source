# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-i386/egg/typhoonae/websocket/server.py
# Compiled at: 2010-12-12 04:36:57
"""Web Socket server implementation which uses tornado."""
import base64, logging, mimetools, optparse, re, threading, tornado.httpserver, tornado.ioloop, tornado.web, tornado.websocket, typhoonae.websocket, urllib, urllib2, urlparse
DESCRIPTION = 'Web Socket Service.'
USAGE = 'usage: %prog [options]'
LOG_FORMAT = '%(levelname)-8s %(asctime)s %(filename)s:%(lineno)s] %(message)s'
WEB_SOCKETS = {}
HANDSHAKE = 1
MESSAGE = 2
HANDSHAKE_URI = '_ah/websocket/handshake'
MESSAGE_URI = '_ah/websocket/message'

def post_multipart(url, fields):
    """Posts multipart form data fields.

    Args:
        url: Post multipart form data to this URL.
        fields: A list of tuples of the form [(fieldname, value), ...].
    """
    (content_type, body) = encode_multipart_formdata(fields)
    body = body.encode('utf-8')
    headers = {'Content-Type': content_type, typhoonae.websocket.WEBSOCKET_HEADER: '', 
       'Content-Length': str(len(body))}
    req = urllib2.Request(url, body, headers)
    try:
        res = urllib2.urlopen(req)
    except urllib2.URLError, e:
        reason = getattr(e, 'reason', e)
        logging.error(reason)
        return

    return res.read()


def encode_multipart_formdata(fields):
    """Encodes multipart form data.

    Returns content type and body.
    """
    BOUNDARY = mimetools.choose_boundary()
    CRLF = '\r\n'
    buffer = []
    for (key, value) in fields:
        buffer.append('--%s' % BOUNDARY)
        buffer.append('Content-Disposition: form-data; name="%s"' % key)
        buffer.append('')
        buffer.append(value)

    buffer.append('--%s--' % BOUNDARY)
    buffer.append('')
    body = CRLF.join(buffer)
    content_type = 'multipart/form-data; boundary=%s' % BOUNDARY
    return (
     content_type, body)


class BroadcastHandler(tornado.web.RequestHandler):
    """The broadcaster."""

    def post(self):
        app_id = self.request.headers.get('X-TyphoonAE-AppId')
        for id in WEB_SOCKETS[app_id].keys():
            try:
                WEB_SOCKETS[app_id][id].write_message(self.request.body)
            except IOError:
                del WEB_SOCKETS[app_id][id]


class MessageHandler(tornado.web.RequestHandler):
    """Receives messages and passes them to web sockets."""

    def post(self):
        id = self.request.headers.get(typhoonae.websocket.WEBSOCKET_HEADER)
        app_id = self.request.headers.get('X-TyphoonAE-AppId')
        if id:
            try:
                WEB_SOCKETS[app_id][int(id)].write_message(self.request.body)
            except IOError:
                del WEB_SOCKETS[app_id][int(id)]


class Dispatcher(threading.Thread):
    """Dispatcher thread for non-blocking message delivery."""

    def __init__(self, address, socket, request_type, param_path, body=''):
        """Constructor.

        Args:
            address: The server address.
            socket: String which represents the socket id.
            request_type: The request type.
            param_path: Parameter path.
            body: The message body.
        """
        super(Dispatcher, self).__init__()
        self._address = address
        self._socket = socket
        self._type = request_type
        self._path = param_path
        self._body = body

    def run(self):
        """Post message."""
        if self._type == HANDSHAKE:
            url = 'http://%s:%s/%s/%s' % (
             self._address, PORT, HANDSHAKE_URI, self._path)
        elif self._type == MESSAGE:
            url = 'http://%s:%s/%s/%s' % (
             self._address, PORT, MESSAGE_URI, self._path)
        post_multipart(url, [('body', self._body), ('from', self._socket)])


class WebSocketHandler(tornado.websocket.WebSocketHandler):
    """Dispatcher for incoming web socket requests."""

    def __init__(self, *args, **kw):
        super(WebSocketHandler, self).__init__(*args, **kw)

    def open(self, param_path):
        sock_id = self.stream.socket.fileno()
        app_id = base64.b64decode(re.match('^/([a-zA-Z0-9=]+)/.*', self.request.uri).group(1))
        if app_id not in WEB_SOCKETS:
            WEB_SOCKETS[app_id] = {}
        WEB_SOCKETS[app_id][sock_id] = self
        address = urlparse.urlsplit(self.request.headers['Origin']).hostname
        dispatcher = Dispatcher(address, str(sock_id), HANDSHAKE, param_path)
        dispatcher.start()

    def on_message(self, message):
        param_path = re.match('^/[a-zA-Z0-9=]+/(.*)', self.request.uri).group(1)
        sock_id = self.stream.socket.fileno()
        address = urlparse.urlsplit(self.request.headers['Origin']).hostname
        dispatcher = Dispatcher(address, str(sock_id), MESSAGE, param_path, body=message)
        dispatcher.start()

    def on_close(self):
        pass


def main():
    """The main function."""
    global PORT
    op = optparse.OptionParser(description=DESCRIPTION, usage=USAGE)
    op.add_option('--internal_port', dest='internal_port', metavar='PORT', help='the application internal port', default=8770)
    (options, args) = op.parse_args()
    PORT = options.internal_port
    logging.basicConfig(format=LOG_FORMAT, level=logging.ERROR)
    application = tornado.web.Application([
     (
      '/broadcast', BroadcastHandler),
     (
      '/message', MessageHandler),
     (
      '/[a-zA-Z0-9=]+/(.*)', WebSocketHandler)])
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(8888)
    tornado.ioloop.IOLoop.instance().start()


if __name__ == '__main__':
    main()