# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/sk/seckiss/rfw/rfw/sslserver.py
# Compiled at: 2014-03-26 05:27:41
import socket, os, base64, logging
from SocketServer import BaseServer, BaseRequestHandler
from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler
from SimpleHTTPServer import SimpleHTTPRequestHandler
import ssl
log = logging.getLogger(('lib.{}').format(__name__))
log.addHandler(logging.NullHandler())

class PlainServer(HTTPServer):

    def __init__(self, server_address, HandlerClass):
        BaseServer.__init__(self, server_address, HandlerClass)
        self.socket = socket.socket(self.address_family, self.socket_type)
        self.server_bind()
        self.server_activate()


class SSLServer(HTTPServer):

    def __init__(self, server_address, HandlerClass, certfile, keyfile):
        if not os.path.isfile(certfile):
            raise IOError(('SSLServer could not locate certfile {}').format(certfile))
        if not os.path.isfile(keyfile):
            raise IOError(('SSLServer could not locate keyfile {}').format(keyfile))
        BaseServer.__init__(self, server_address, HandlerClass)
        self.socket = ssl.SSLSocket(socket.socket(self.address_family, self.socket_type), keyfile=keyfile, certfile=certfile)
        self.server_bind()
        self.server_activate()


class CommonRequestHandler(BaseHTTPRequestHandler):

    def log_message(self, format, *args):
        log.info('%s - - [%s] %s' % (
         self.client_address[0],
         self.log_date_time_string(),
         format % args))

    def http_resp(self, code, content):
        content = str(content)
        self.send_response(code)
        self.send_header('Content-Length', len(content) + 2)
        self.end_headers()
        self.wfile.write(content + '\r\n')


class BasicAuthRequestHandler(CommonRequestHandler):
    """HTTP request handler with Basic Authentication. It automatically sends back HTTP response code 401 if no valid Autorization header present in the request."""

    def creds_check(self, user, password):
        return False

    def parse_auth(self, header):
        """Parse rfc2617 HTTP authentication header string (basic) and return (user,pass) tuple or None"""
        try:
            method, data = header.split(None, 1)
            if method.lower() == 'basic':
                user, pwd = base64.b64decode(data).split(':', 1)
                return (
                 user, pwd)
        except (KeyError, ValueError):
            return

        return

    def auth_basic(realm, text):
        """Callback decorator to require HTTP basic authentication"""

        def decorator(func):

            def wrapper(this, *a, **ka):
                parse_result = func(this, *a, **ka)
                if not parse_result:
                    return False
                creds = this.parse_auth(this.headers.get('Authorization', ''))
                if not creds or not this.creds_check(*creds):
                    if creds:
                        ip = this.client_address[0]
                        log.warn(('Authentication attempt with wrong credentials from {}').format(ip))
                    this.send_response(401)
                    this.send_header('WWW-Authenticate', ('Basic realm="{}"').format(realm))
                    this.send_header('Connection', 'close')
                    this.end_headers()
                    return False
                return True

            return wrapper

        return decorator

    @auth_basic(realm='private', text='Access denied')
    def parse_request(self):
        return BaseHTTPRequestHandler.parse_request(self)