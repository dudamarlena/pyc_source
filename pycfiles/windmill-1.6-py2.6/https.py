# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-universal/egg/windmill/server/https.py
# Compiled at: 2011-01-13 01:48:00
"""
    This module provides an SSL-enabled HTTP server, WindmillChooserApplication
    and WindmillProxyApplication that are drop-in replacements for the standard
    non-ssl-enabled ones.
"""
import time, socket, select, urllib, SocketServer
from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler
from StringIO import StringIO
from proxy import WindmillProxyApplication
from httplib import HTTPConnection, HTTPException
import traceback, sys, windmill
if not sys.version.startswith('2.4'):
    from urlparse import urlparse, urlunparse
else:
    from windmill.tools.urlparse_25 import urlparse, urlunparse
import logging
logger = logging.getLogger(__name__)
try:
    import ssl
    _ssl_wrap_socket = ssl.wrap_socket
    _socket_create_connection = socket.create_connection
except (AttributeError, ImportError):
    if windmill.has_ssl:
        from OpenSSL import SSL
    from httplib import FakeSocket

    class BetterFakeSocket(FakeSocket):
        """ A FakeSocket that implements sendall and
            handles exceptions better
        """

        class _closedsocket:

            def __nonzero__(self):
                return False

            def __getattr__(self, name):
                if name == '__nonzero__':
                    return self.__nonzero__
                raise HTTPException(9, 'Bad file descriptor')

        def __init__(self, sock, ssl):
            FakeSocket.__init__(self, sock, ssl)
            self.ok = True

        def sendall(self, data):
            if self.ok:
                try:
                    self._ssl.sendall(data)
                except SSL.SysCallError, err:
                    self.ok = False
                    print err

        def recv(self, len=1024, flags=0):
            if self.ok:
                try:
                    result = self._ssl.read(len)
                except SSL.SysCallError, err:
                    self.ok = False
                    print err

                return result


    def _ssl_verify_peer(conection, certificate, errnum, depth, ok):
        return True


    def _ssl_wrap_socket(sock, certfile=None, server_side=False, ca_certs=None, do_handshake_on_connect=True, suppress_ragged_eofs=True):
        ctx = SSL.Context(SSL.SSLv23_METHOD)
        if certfile is not None:
            ctx.use_privatekey_file(certfile)
            try:
                ctx.use_certificate_file(certfile)
            except:
                pass
            else:
                ctx.load_verify_locations(certfile)
        ctx.set_verify(SSL.VERIFY_NONE, _ssl_verify_peer)
        ssl_sock = SSL.Connection(ctx, sock)
        if server_side:
            ssl_sock.set_accept_state()
        else:
            ssl_sock.set_connect_state()
        return BetterFakeSocket(sock, ssl_sock)


    def _socket_create_connection(address, timeout=None):
        if timeout is None:
            timeout = socket.getdefaulttimeout()
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        oldtimeout = socket.getdefaulttimeout()
        socket.setdefaulttimeout(timeout)
        sock.connect(address)
        socket.setdefaulttimeout(oldtimeout)
        return sock


class WindmillHTTPRequestHandler(SocketServer.ThreadingMixIn, BaseHTTPRequestHandler):

    def __init__(self, request, client_address, server):
        self.headers_set = []
        self.headers_sent = []
        self.header_buffer = ''
        BaseHTTPRequestHandler.__init__(self, request, client_address, server)

    def _sock_connect_to(self, netloc, soc):
        """Parse netloc string and establish connection on socket."""
        host_port = netloc.split(':', 1)
        if len(host_port) == 1:
            host_port.append(80)
        try:
            soc.connect(host_port)
        except socket.error, msg:
            self.send_error(404, msg)
            return False

        return True

    def do_CONNECT(self):
        """ Handle CONNECT commands.  Just set up SSL and restart. """
        request = None
        try:
            try:
                self.log_request(200)
                self.wfile.write(self.protocol_version + ' 200 Connection established\r\n')
                self.wfile.write('Proxy-agent: %s\r\n' % self.version_string())
                self.wfile.write('\r\n')
                if not windmill.has_ssl:
                    return
                request = self.connection
                connstream = _ssl_wrap_socket(self.connection, server_side=True, certfile=self.server.cert_creator[self.path].certfile)
                self.request = connstream
                self.base_path = 'https://' + self.path
                if self.base_path.endswith(':443'):
                    self.base_path = self.base_path[:-4]
                self.connection = self.request
                self.rfile = socket._fileobject(self.connection, 'rb', self.rbufsize)
                self.wfile = socket._fileobject(self.connection, 'wb', self.wbufsize)
                try:
                    self.handle()
                    self.finish()
                finally:
                    sys.exc_traceback = None

            except socket.error, err:
                logger.debug('%s while serving (%s) %s' % (err,
                 self.command, self.path))

        finally:
            if request is not None:
                request.close()

        return

    def handle_ALL(self):
        namespaces = self.server.namespaces
        proxy = self.server.proxy
        found = None
        path = self.path.split('?', 1)[0]
        for key in namespaces:
            if path.find('/' + key + '/') is not -1:
                found = key
                environ = self.get_environ()
                result = namespaces[found](environ, self.start_response)
                break
        else:
            found = None
            environ = self.get_environ()
            result = proxy(environ, self.start_response)

        try:
            for out in result:
                self.write(out)

        except socket.error, err:
            logger.debug('%s while serving (%s) %s' % (err, self.command, self.path))

        self.wfile.flush()
        self.connection.close()
        return

    do_GET = handle_ALL
    do_POST = handle_ALL
    do_PUT = handle_ALL
    do_DELETE = handle_ALL

    def start_response(self, status, headers, exc_info=None):
        if exc_info:
            try:
                if self.headers_sent:
                    raise exc_info[0], exc_info[1], exc_info[2]
            finally:
                exc_info = None

        elif self.headers_set:
            raise AssertionError('Headers already set!')
        self.headers_set[:] = [status, headers]
        (status, response_headers) = self.headers_sent[:] = self.headers_set
        (code, message) = status.split(' ', 1)
        self.send_response(int(code), message)
        self.send_headers(response_headers)
        return self.write

    def send_headers(self, response_headers):
        for header in response_headers:
            self.send_header(header[0], header[1])

        try:
            self.wfile.write(self.header_buffer + '\r\n')
        except socket.error, e:
            if len(e.args) is 2 and e.args[0] is 32:
                logger.debug('Client severed connection prematurely.')
            else:
                raise e

    def send_header(self, keyword, value):
        """Send a MIME header."""
        if self.request_version != 'HTTP/0.9':
            self.header_buffer += '%s: %s\r\n' % (keyword, value)
        if keyword.lower() == 'connection':
            if value.lower() == 'close':
                self.close_connection = 1
            elif value.lower() == 'keep-alive':
                self.close_connection = 0

    def send_response(self, code, message=None):
        """Send the response header and log the response code.
            Also send two standard headers with the server software
            version and the current date.
            """
        self.log_request(code)
        if message is None:
            if code in self.responses:
                message = self.responses[code][0]
            else:
                message = ''
        if self.request_version != 'HTTP/0.9':
            self.header_buffer += '%s %d %s\r\n' % (self.protocol_version, code, message)
        return

    def write(self, data):
        if not self.headers_set:
            raise AssertionError('write() before start_response()')
        self.wfile.write(data)

    def get_environ(self):
        """ Put together a wsgi environment """
        if hasattr(self, 'base_path'):
            self.path = self.base_path + self.path
        env = self.server.base_environ.copy()
        env['SERVER_PROTOCOL'] = self.request_version
        env['REQUEST_METHOD'] = self.command
        if '?' in self.path:
            (path, query) = self.path.split('?', 1)
        else:
            path, query = self.path, ''
        env['PATH_INFO'] = urllib.unquote(path)
        env['QUERY_STRING'] = query
        host = self.address_string()
        if host != self.client_address[0]:
            env['REMOTE_HOST'] = host
        env['REMOTE_ADDR'] = self.client_address[0]
        if self.headers.typeheader is not None:
            env['CONTENT_TYPE'] = self.headers.typeheader
        length = self.headers.getheader('content-length')
        if length:
            env['CONTENT_LENGTH'] = length
        for header in self.headers.headers:
            (key, value) = header.split(':', 1)
            key = key.replace('-', '_').upper()
            value = value.strip()
            if key in env:
                continue
            if 'HTTP_' + key in env:
                env[('HTTP_' + key)] += ',' + value
            else:
                env['HTTP_' + key] = value

        env['wsgi.url_scheme'] = urlparse(self.path).scheme
        clen = self.headers.getheader('content-length')
        if clen is not None and int(clen) > 0:
            i = self.rfile.read(int(clen))
            env['wsgi.input'] = StringIO(i)
        else:
            env['wsgi.input'] = self.rfile
        self.reconstruct_url(env)
        return env

    def reconstruct_url(self, environ):
        """ This can be done much faster and in a tidier way."""
        url = environ['wsgi.url_scheme'] + '://'
        if environ.get('HTTP_HOST'):
            url += environ['HTTP_HOST']
        else:
            url += environ['SERVER_NAME']
            if environ['wsgi.url_scheme'] == 'https':
                if environ['SERVER_PORT'] != '443':
                    url += ':' + environ['SERVER_PORT']
            elif environ['SERVER_PORT'] != '80':
                url += ':' + environ['SERVER_PORT']
        url += environ.get('SCRIPT_NAME', '')
        if '://' in self.path:
            url = self.path
        else:
            url += self.path
        environ['reconstructed_url'] = url
        return url

    def log_message(self, format, *args):
        logger.debug(format % args)


class WindmillHTTPServer(SocketServer.ThreadingMixIn, HTTPServer):

    def __init__(self, address, handler, cert_creator, apps, proxy):
        self.cert_creator = cert_creator
        self.namespaces = dict([ (arg.ns, arg) for arg in apps ])
        self.proxy = proxy
        HTTPServer.__init__(self, address, handler)
        self.setup_environ()
        self.threads = []

    daemon_threads = True

    def setup_environ(self):
        env = self.base_environ = {}
        env['SERVER_NAME'] = self.server_name
        env['GATEWAY_INTERFACE'] = 'CGI/1.1'
        env['SERVER_PORT'] = self.server_port
        env['REMOTE_HOST'] = ''
        env['CONTENT_LENGTH'] = ''
        env['SCRIPT_NAME'] = ''

    ready = False

    def start(self):
        WindmillHTTPServer.ready = True
        while self.ready:
            self.handle_request()

        self.server_close()

    def server_close(self):
        try:
            self.socket.shutdown(socket.SHUT_RDWR)
            self.socket.close()
        except socket.error, e:
            if len(e.args) is 2 and e.args[0] is 57:
                logger.debug("Server was killed, socket didn't shutdown perfectly.")
            else:
                raise e

    def add_namespace(self, name, application):
        """Add an application to a specific url namespace in windmill"""
        self.namespaces[name] = application

    def stop(self):
        self.xmlrpc_methods_instance.stop_runserver()
        WindmillHTTPServer.ready = False
        while True:
            try:
                socket.setdefaulttimeout(0.5)
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.connect(self.server_address)
                s.send('\n')
            except socket.error:
                break

        for t in [ t for t in self.threads if t.isAlive() ]:
            t.terminate()

    def process_request(self, request, client_address):
        """Start a new thread to process the request."""
        import thread2
        t = thread2.Thread(target=self.process_request_thread, args=(
         request, client_address))
        if self.daemon_threads:
            t.setDaemon(1)
        t.start()
        self.threads.append(t)

    def handle_error(self, request, client_address):
        try:
            args = sys.exec_info()
        except:
            return

        print '-' * 40
        print 'Exception happened during processing of request from',
        print client_address
        try:
            traceback.print_exception(*args)
        except TypeError:
            print 'Traceback cannot be printed, probably do to a thread safety issue.'

        print '-' * 40


class WindmillConnection(HTTPConnection):
    """ Decide on the run if we should do HTTP or HTTPS """

    def __init__(self, scheme, host, port=None, strict=None):
        self.scheme = scheme
        if scheme == 'https':
            self.default_port = 443
        HTTPConnection.__init__(self, host, port, strict)
        self.key_file = None
        self.cert_file = None
        if not hasattr(self, 'timeout'):
            self.timeout = None
        return

    def connect(self):
        """Connect to a host on a given (SSL) port."""
        if self.scheme == 'http':
            HTTPConnection.connect(self)
            return
        sock = _socket_create_connection((self.host, self.port), self.timeout)
        self.sock = _ssl_wrap_socket(sock, self.key_file, self.cert_file)


class WindmillHTTPSProxyApplication(WindmillProxyApplication):
    ConnectionClass = WindmillConnection

    def get_connection(self, url):
        return self.ConnectionClass(url.scheme, url.netloc)