# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\pycoon\wsgi\servers\cherrypy\wsgiserver.py
# Compiled at: 2007-02-04 07:09:44
"""A high-speed, production ready, thread pooled, generic WSGI server.

Simplest example on how to use this module directly
(without using CherryPy's application machinery):

    from cherrypy import wsgiserver
    
    def my_crazy_app(environ, start_response):
        status = '200 OK'
        response_headers = [('Content-type','text/plain')]
        start_response(status, response_headers)
        return ['Hello world!
']
    
    # Here we set our application to the script_name '/' 
    wsgi_apps = [('/', my_crazy_app)]
    
    server = wsgiserver.CherryPyWSGIServer(('localhost', 8070), wsgi_apps,
                                           server_name='localhost')
    
    # Want SSL support? Just set these attributes
    # server.ssl_certificate = <filename>
    # server.ssl_private_key = <filename>
    
    if __name__ == '__main__':
        server.start()

This won't call the CherryPy engine (application side) at all, only the
WSGI server, which is independant from the rest of CherryPy. Don't
let the name "CherryPyWSGIServer" throw you; the name merely reflects
its origin, not it's coupling.

The CherryPy WSGI server can serve as many WSGI application
as you want in one instance:

    wsgi_apps = [('/', my_crazy_app), (/blog', my_blog_app)]

"""
import base64, Queue, os, re
quoted_slash = re.compile('(?i)%2F')
import rfc822, socket
try:
    import cStringIO as StringIO
except ImportError:
    import StringIO

import sys, threading, time, traceback
from urllib import unquote
from urlparse import urlparse
try:
    from OpenSSL import SSL
    from OpenSSL import crypto
except ImportError:
    SSL = None

import errno
socket_errors_to_ignore = []
for _ in ('EPIPE', 'ETIMEDOUT', 'ECONNREFUSED', 'ECONNRESET', 'EHOSTDOWN', 'EHOSTUNREACH', 'WSAECONNABORTED', 'WSAECONNREFUSED', 'WSAECONNRESET', 'WSAENETRESET', 'WSAETIMEDOUT'):
    if _ in dir(errno):
        socket_errors_to_ignore.append(getattr(errno, _))

socket_errors_to_ignore = dict.fromkeys(socket_errors_to_ignore).keys()
socket_errors_to_ignore.append('timed out')
comma_separated_headers = [
 'ACCEPT', 'ACCEPT-CHARSET', 'ACCEPT-ENCODING', 'ACCEPT-LANGUAGE', 'ACCEPT-RANGES', 'ALLOW', 'CACHE-CONTROL', 'CONNECTION', 'CONTENT-ENCODING', 'CONTENT-LANGUAGE', 'EXPECT', 'IF-MATCH', 'IF-NONE-MATCH', 'PRAGMA', 'PROXY-AUTHENTICATE', 'TE', 'TRAILER', 'TRANSFER-ENCODING', 'UPGRADE', 'VARY', 'VIA', 'WARNING', 'WWW-AUTHENTICATE']

class HTTPRequest(object):
    """An HTTP Request (and response).
    
    A single HTTP connection may consist of multiple request/response pairs.
    
    connection: the HTTP Connection object which spawned this request.
    rfile: the 'read' fileobject from the connection's socket
    ready: when True, the request has been parsed and is ready to begin
        generating the response. When False, signals the calling Connection
        that the response should not be generated and the connection should
        close.
    close_connection: signals the calling Connection that the request
        should close. This does not imply an error! The client and/or
        server may each request that the connection be closed.
    chunked_write: if True, output will be encoded with the "chunked"
        transfer-coding. This value is set automatically inside
        send_headers.
    """
    __module__ = __name__

    def __init__(self, connection):
        self.connection = connection
        self.rfile = self.connection.rfile
        self.sendall = self.connection.sendall
        self.environ = connection.environ.copy()
        self.ready = False
        self.started_response = False
        self.status = ''
        self.outheaders = []
        self.sent_headers = False
        self.close_connection = False
        self.chunked_write = False

    def parse_request(self):
        """Parse the next HTTP request start-line and message-headers."""
        request_line = self.rfile.readline()
        if not request_line:
            self.ready = False
            return
        if request_line == '\r\n':
            request_line = self.rfile.readline()
            if not request_line:
                self.ready = False
                return
        server = self.connection.server
        self.environ['SERVER_SOFTWARE'] = '%s WSGI Server' % server.version
        (method, path, req_protocol) = request_line.strip().split(' ', 2)
        self.environ['REQUEST_METHOD'] = method
        (scheme, location, path, params, qs, frag) = urlparse(path)
        if frag:
            self.simple_response('400 Bad Request', 'Illegal #fragment in Request-URI.')
            return
        if scheme:
            self.environ['wsgi.url_scheme'] = scheme
        if params:
            path = path + ';' + params
        atoms = [ unquote(x) for x in quoted_slash.split(path) ]
        path = ('%2F').join(atoms)
        if path == '*':
            self.environ['SCRIPT_NAME'] = ''
            self.environ['PATH_INFO'] = '*'
            self.wsgi_app = server.mount_points[(-1)][1]
        else:
            for (mount_point, wsgi_app) in server.mount_points:
                if path.startswith(mount_point + '/') or path == mount_point:
                    self.environ['SCRIPT_NAME'] = mount_point
                    self.environ['PATH_INFO'] = path[len(mount_point):]
                    self.wsgi_app = wsgi_app
                    break
            else:
                self.simple_response('404 Not Found')
                return

            self.environ['QUERY_STRING'] = qs
            rp = (
             int(req_protocol[5]), int(req_protocol[7]))
            sp = (int(server.protocol[5]), int(server.protocol[7]))
            if sp[0] != rp[0]:
                self.simple_response('505 HTTP Version Not Supported')
                return
            self.environ['SERVER_PROTOCOL'] = req_protocol
            self.environ['ACTUAL_SERVER_PROTOCOL'] = server.protocol
            self.response_protocol = 'HTTP/%s.%s' % min(rp, sp)
            if location:
                self.environ['SERVER_NAME'] = location
            headers = rfc822.Message(self.rfile, seekable=0)
            self.environ.update(self.parse_headers(headers))
            creds = headers.getheader('Authorization', '').split(' ', 1)
            self.environ['AUTH_TYPE'] = creds[0]
            if creds[0].lower() == 'basic':
                (user, pw) = base64.decodestring(creds[1]).split(':', 1)
                self.environ['REMOTE_USER'] = user
            if self.response_protocol == 'HTTP/1.1':
                if headers.getheader('Connection', '') == 'close':
                    self.close_connection = True
                    self.outheaders.append(('Connection', 'close'))
            elif headers.getheader('Connection', '') == 'Keep-Alive':
                if self.close_connection == False:
                    self.outheaders.append(('Connection', 'Keep-Alive'))
            else:
                self.close_connection = True
        te = headers.getheader('Transfer-Encoding', '')
        te = [ x.strip() for x in te.split(',') if x.strip() ]
        if te:
            while te:
                enc = te.pop()
                if enc.lower() == 'chunked':
                    if not self.decode_chunked():
                        return
                else:
                    self.simple_response('501 Unimplemented')
                    self.close_connection = True
                    return

        else:
            cl = headers.getheader('Content-length')
            if method in ('POST', 'PUT') and cl is None:
                self.simple_response('411 Length Required')
                return
        if headers.getheader('Expect', '') == '100-continue':
            self.simple_response(100)
        self.ready = True
        return

    def parse_headers(self, headers):
        """Parse the given HTTP request message-headers."""
        environ = {}
        ct = headers.dict.get('content-type')
        if ct:
            environ['CONTENT_TYPE'] = ct
        cl = headers.dict.get('content-length')
        if cl:
            environ['CONTENT_LENGTH'] = cl
        for line in headers.headers:
            if line[:1].isspace():
                v = line.strip()
            else:
                (k, v) = line.split(':', 1)
                k, v = k.strip().upper(), v.strip()
                envname = 'HTTP_' + k.replace('-', '_')
            if k in comma_separated_headers:
                existing = environ.get(envname)
                if existing:
                    v = (', ').join((existing, v))
            environ[envname] = v

        return environ

    def decode_chunked(self):
        """Decode the 'chunked' transfer coding."""
        cl = 0
        data = StringIO.StringIO()
        while True:
            line = self.rfile.readline().strip().split(';', 1)
            chunk_size = int(line.pop(0), 16)
            if chunk_size <= 0:
                break
            cl += chunk_size
            data.write(self.rfile.read(chunk_size))
            crlf = self.rfile.read(2)
            if crlf != '\r\n':
                self.simple_response('400 Bad Request', "Bad chunked transfer coding (expected '\\r\\n', got %r)" % crlf)
                return

        headers = rfc822.Message(self.rfile, seekable=0)
        self.environ.update(self.parse_headers(headers))
        data.seek(0)
        self.environ['wsgi.input'] = data
        self.environ['CONTENT_LENGTH'] = str(cl) or ''
        return True

    def respond(self):
        """Call the appropriate WSGI app and write its iterable output."""
        response = self.wsgi_app(self.environ, self.start_response)
        try:
            for chunk in response:
                self.write(chunk)

        finally:
            if hasattr(response, 'close'):
                response.close()
        if self.ready and not self.sent_headers and not self.connection.server.interrupt:
            self.sent_headers = True
            self.send_headers()
        if self.chunked_write:
            self.sendall('0\r\n\r\n')

    def simple_response(self, status, msg=''):
        """Write a simple response back to the client."""
        status = str(status)
        buf = ['%s %s\r\n' % (self.connection.server.protocol, status), 'Content-Length: %s\r\n' % len(msg)]
        if status[:3] == '413' and self.response_protocol == 'HTTP/1.1':
            self.close_connection = True
            buf.append('Connection: close\r\n')
        buf.append('\r\n')
        if msg:
            buf.append(msg)
        self.sendall(('').join(buf))

    def start_response(self, status, headers, exc_info=None):
        """WSGI callable to begin the HTTP response."""
        if self.started_response:
            if not exc_info:
                assert False, 'Already started response'
            else:
                try:
                    raise exc_info[0], exc_info[1], exc_info[2]
                finally:
                    exc_info = None
        self.started_response = True
        self.status = status
        self.outheaders.extend(headers)
        return self.write

    def write(self, chunk):
        """WSGI callable to write unbuffered data to the client.
        
        This method is also used internally by start_response (to write
        data from the iterable returned by the WSGI application).
        """
        if not self.sent_headers:
            self.sent_headers = True
            self.send_headers()
        if self.chunked_write:
            buf = [
             hex(len(chunk))[2:], '\r\n', chunk, '\r\n']
            self.sendall(('').join(buf))
        else:
            self.sendall(chunk)

    def send_headers(self):
        """Assert, process, and send the HTTP response message-headers."""
        hkeys = [ key.lower() for (key, value) in self.outheaders ]
        status = int(self.status[:3])
        if self.response_protocol == 'HTTP/1.1':
            if status == 413:
                self.close_connection = True
            elif 'content-length' not in hkeys:
                if status < 200 or status in (204, 205, 304):
                    pass
                else:
                    self.chunked_write = True
                    self.outheaders.append(('Transfer-Encoding', 'chunked'))
        if self.close_connection and 'connection' not in hkeys:
            self.outheaders.append(('Connection', 'close'))
        if 'date' not in hkeys:
            self.outheaders.append(('Date', rfc822.formatdate()))
        server = self.connection.server
        if 'server' not in hkeys:
            self.outheaders.append(('Server', server.version))
        buf = [server.protocol, ' ', self.status, '\r\n']
        try:
            for (k, v) in self.outheaders:
                buf.append(k + ': ' + v + '\r\n')

        except TypeError:
            if not isinstance(k, str):
                raise TypeError('WSGI response header key %r is not a string.')
            if not isinstance(v, str):
                raise TypeError('WSGI response header value %r is not a string.')
            else:
                raise

        buf.append('\r\n')
        self.sendall(('').join(buf))


def _ssl_wrap_method(method, is_reader=False):
    """Wrap the given method with SSL error-trapping.
    
    is_reader: if False (the default), EOF errors will be raised.
        If True, EOF errors will return "" (to emulate normal sockets).
    """

    def ssl_method_wrapper(self, *args, **kwargs):
        start = time.time()
        while True:
            try:
                return method(self, *args, **kwargs)
            except (SSL.WantReadError, SSL.WantWriteError):
                time.sleep(self.ssl_retry)
            except SSL.SysCallError, e:
                if is_reader and e.args == (-1, 'Unexpected EOF'):
                    return ''
                errno = e.args[0]
                if is_reader and errno in socket_errors_to_ignore:
                    return ''
                raise socket.error(errno)
            except SSL.Error, e:
                if is_reader and e.args == (-1, 'Unexpected EOF'):
                    return ''
                if is_reader and e.args[0][0][2] == 'ssl handshake failure':
                    return ''
                raise

            if time.time() - start > self.ssl_timeout:
                raise socket.timeout('timed out')

    return ssl_method_wrapper


class SSL_fileobject(socket._fileobject):
    """Faux file object attached to a socket object."""
    __module__ = __name__
    ssl_timeout = 3
    ssl_retry = 0.01
    close = _ssl_wrap_method(socket._fileobject.close)
    flush = _ssl_wrap_method(socket._fileobject.flush)
    write = _ssl_wrap_method(socket._fileobject.write)
    writelines = _ssl_wrap_method(socket._fileobject.writelines)
    read = _ssl_wrap_method(socket._fileobject.read, is_reader=True)
    readline = _ssl_wrap_method(socket._fileobject.readline, is_reader=True)
    readlines = _ssl_wrap_method(socket._fileobject.readlines, is_reader=True)


class HTTPConnection(object):
    """An HTTP connection (active socket).
    
    socket: the raw socket object (usually TCP) for this connection.
    addr: the "bind address" for the remote end of the socket.
        For IP sockets, this is a tuple of (REMOTE_ADDR, REMOTE_PORT).
        For UNIX domain sockets, this will be a string.
    server: the HTTP Server for this Connection. Usually, the server
        object possesses a passive (server) socket which spawns multiple,
        active (client) sockets, one for each connection.
    
    environ: a WSGI environ template. This will be copied for each request.
    rfile: a fileobject for reading from the socket.
    sendall: a function for writing (+ flush) to the socket.
    """
    __module__ = __name__
    rbufsize = -1
    RequestHandlerClass = HTTPRequest
    environ = {'wsgi.version': (1, 0), 'wsgi.url_scheme': 'http', 'wsgi.multithread': True, 'wsgi.multiprocess': False, 'wsgi.run_once': False, 'wsgi.errors': sys.stderr}

    def __init__(self, sock, addr, server):
        self.socket = sock
        self.addr = addr
        self.server = server
        self.environ = self.environ.copy()
        if SSL and isinstance(sock, SSL.ConnectionType):
            timeout = sock.gettimeout()
            self.rfile = SSL_fileobject(sock, 'r', self.rbufsize)
            self.rfile.ssl_timeout = timeout
            self.sendall = _ssl_wrap_method(sock.sendall)
            self.environ['wsgi.url_scheme'] = 'https'
            self.environ['HTTPS'] = 'on'
            sslenv = getattr(server, 'ssl_environ', None)
            if sslenv:
                self.environ.update(sslenv)
        else:
            self.rfile = sock.makefile('r', self.rbufsize)
            self.sendall = sock.sendall
        self.environ.update({'wsgi.input': self.rfile, 'SERVER_NAME': self.server.server_name})
        if isinstance(self.server.bind_addr, basestring):
            self.environ['SERVER_PORT'] = ''
        else:
            self.environ['SERVER_PORT'] = str(self.server.bind_addr[1])
            self.environ['REMOTE_ADDR'] = self.addr[0]
            self.environ['REMOTE_PORT'] = str(self.addr[1])
        return

    def communicate(self):
        """Read each request and respond appropriately."""
        try:
            while True:
                req = None
                req = self.RequestHandlerClass(self)
                req.parse_request()
                if not req.ready:
                    return
                req.respond()
                if req.close_connection:
                    return

        except socket.error, e:
            errno = e.args[0]
            if errno not in socket_errors_to_ignore:
                if req:
                    req.simple_response('500 Internal Server Error', format_exc())
            return
        except (KeyboardInterrupt, SystemExit):
            raise
        except:
            if req:
                req.simple_response('500 Internal Server Error', format_exc())

        return

    def close(self):
        """Close the socket underlying this connection."""
        self.rfile.close()
        self.socket.close()


def format_exc(limit=None):
    """Like print_exc() but return a string. Backport for Python 2.3."""
    try:
        (etype, value, tb) = sys.exc_info()
        return ('').join(traceback.format_exception(etype, value, tb, limit))
    finally:
        etype = value = tb = None
    return


_SHUTDOWNREQUEST = None

class WorkerThread(threading.Thread):
    """Thread which continuously polls a Queue for Connection objects.
    
    server: the HTTP Server which spawned this thread, and which owns the
        Queue and is placing active connections into it.
    ready: a simple flag for the calling server to know when this thread
        has begun polling the Queue.
    
    Due to the timing issues of polling a Queue, a WorkerThread does not
    check its own 'ready' flag after it has started. To stop the thread,
    it is necessary to stick a _SHUTDOWNREQUEST object onto the Queue
    (one for each running WorkerThread).
    """
    __module__ = __name__

    def __init__(self, server):
        self.ready = False
        self.server = server
        threading.Thread.__init__(self)

    def run(self):
        try:
            self.ready = True
            while True:
                conn = self.server.requests.get()
                if conn is _SHUTDOWNREQUEST:
                    return
                try:
                    conn.communicate()
                finally:
                    conn.close()

        except (KeyboardInterrupt, SystemExit), exc:
            self.server.interrupt = exc


class SSLConnection:
    """A thread-safe wrapper for an SSL.Connection.
    
    *args: the arguments to create the wrapped SSL.Connection(*args).
    """
    __module__ = __name__

    def __init__(self, *args):
        self._ssl_conn = SSL.Connection(*args)
        self._lock = threading.RLock()

    for f in ('get_context', 'pending', 'send', 'write', 'recv', 'read', 'renegotiate',
              'bind', 'listen', 'connect', 'accept', 'setblocking', 'fileno', 'shutdown',
              'close', 'get_cipher_list', 'getpeername', 'getsockname', 'getsockopt',
              'setsockopt', 'makefile', 'get_app_data', 'set_app_data', 'state_string',
              'sock_shutdown', 'get_peer_certificate', 'want_read', 'want_write',
              'set_connect_state', 'set_accept_state', 'connect_ex', 'sendall', 'settimeout'):
        exec 'def %s(self, *args):\n        self._lock.acquire()\n        try:\n            return self._ssl_conn.%s(*args)\n        finally:\n            self._lock.release()\n' % (f, f)


class CherryPyWSGIServer(object):
    """An HTTP server for WSGI.
    
    bind_addr: a (host, port) tuple if TCP sockets are desired;
        for UNIX sockets, supply the filename as a string.
    wsgi_app: the WSGI 'application callable'; multiple WSGI applications
        may be passed as (script_name, callable) pairs.
    numthreads: the number of worker threads to create (default 10).
    server_name: the string to set for WSGI's SERVER_NAME environ entry.
        Defaults to socket.gethostname().
    max: the maximum number of queued requests (defaults to -1 = no limit).
    request_queue_size: the 'backlog' argument to socket.listen();
        specifies the maximum number of queued connections (default 5).
    timeout: the timeout in seconds for accepted connections (default 10).
    
    protocol: the version string to write in the Status-Line of all
        HTTP responses. For example, "HTTP/1.1" (the default). This
        also limits the supported features used in the response.
    
    
    SSL/HTTPS
    ---------
    The OpenSSL module must be importable for SSL functionality.
    You can obtain it from http://pyopenssl.sourceforge.net/
    
    ssl_certificate: the filename of the server SSL certificate.
    ssl_privatekey: the filename of the server's private key file.
    
    If either of these is None (both are None by default), this server
    will not use SSL. If both are given and are valid, they will be read
    on server start and used in the SSL context for the listening socket.
    """
    __module__ = __name__
    protocol = 'HTTP/1.1'
    version = 'CherryPy/3.0.0'
    ready = False
    _interrupt = None
    ConnectionClass = HTTPConnection
    ssl_certificate = None
    ssl_private_key = None

    def __init__(self, bind_addr, wsgi_app, numthreads=10, server_name=None, max=-1, request_queue_size=5, timeout=10):
        self.requests = Queue.Queue(max)
        if callable(wsgi_app):
            self.mount_points = [
             (
              '', wsgi_app)]
        else:
            self.mount_points = wsgi_app
        self.mount_points.sort()
        self.mount_points.reverse()
        self.bind_addr = bind_addr
        self.numthreads = numthreads or 1
        if not server_name:
            server_name = socket.gethostname()
        self.server_name = server_name
        self.request_queue_size = request_queue_size
        self._workerThreads = []
        self.timeout = timeout

    def start(self):
        """Run the server forever."""
        self._interrupt = None

        def bind(family, type, proto=0):
            """Create (or recreate) the actual socket object."""
            self.socket = socket.socket(family, type, proto)
            self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            if self.ssl_certificate and self.ssl_private_key:
                if SSL is None:
                    raise ImportError('You must install pyOpenSSL to use HTTPS.')
                ctx = SSL.Context(SSL.SSLv23_METHOD)
                ctx.use_privatekey_file(self.ssl_private_key)
                ctx.use_certificate_file(self.ssl_certificate)
                self.socket = SSLConnection(ctx, self.socket)
                self.populate_ssl_environ()
            self.socket.bind(self.bind_addr)
            return

        if isinstance(self.bind_addr, basestring):
            try:
                os.unlink(self.bind_addr)
            except:
                pass
            else:
                try:
                    os.chmod(self.bind_addr, 511)
                except:
                    pass
                else:
                    info = [
                     (
                      socket.AF_UNIX, socket.SOCK_STREAM, 0, '', self.bind_addr)]
        else:
            (host, port) = self.bind_addr
            flags = 0
            if host == '':
                host = None
                flags = socket.AI_PASSIVE
            try:
                info = socket.getaddrinfo(host, port, socket.AF_UNSPEC, socket.SOCK_STREAM, 0, flags)
            except socket.gaierror:
                info = [
                 (
                  socket.AF_INET, socket.SOCK_STREAM, 0, '', self.bind_addr)]

        self.socket = None
        msg = 'No socket could be created'
        for res in info:
            (af, socktype, proto, canonname, sa) = res
            try:
                bind(af, socktype, proto)
            except socket.error, msg:
                if self.socket:
                    self.socket.close()
                self.socket = None
                continue

            break

        if not self.socket:
            raise socket.error, msg
        self.socket.settimeout(1)
        self.socket.listen(self.request_queue_size)
        for i in xrange(self.numthreads):
            self._workerThreads.append(WorkerThread(self))

        for worker in self._workerThreads:
            worker.setName('CP WSGIServer ' + worker.getName())
            worker.start()

        for worker in self._workerThreads:
            while not worker.ready:
                time.sleep(0.1)

        self.ready = True
        while self.ready:
            self.tick()
            if self.interrupt:
                while self.interrupt is True:
                    time.sleep(0.1)

                raise self.interrupt

        return

    def tick(self):
        """Accept a new connection and put it on the Queue."""
        try:
            (s, addr) = self.socket.accept()
            if not self.ready:
                return
            if hasattr(s, 'settimeout'):
                s.settimeout(self.timeout)
            conn = self.ConnectionClass(s, addr, self)
            self.requests.put(conn)
        except socket.timeout:
            return
        except socket.error, x:
            msg = x.args[1]
            if msg in ('Bad file descriptor', 'Socket operation on non-socket'):
                return
            if msg == 'Resource temporarily unavailable':
                return
            raise

    def _get_interrupt(self):
        return self._interrupt

    def _set_interrupt(self, interrupt):
        self._interrupt = True
        self.stop()
        self._interrupt = interrupt

    interrupt = property(_get_interrupt, _set_interrupt, doc='Set this to an Exception instance to interrupt the server.')

    def stop(self):
        """Gracefully shutdown a server that is serving forever."""
        self.ready = False
        sock = getattr(self, 'socket', None)
        if sock:
            if not isinstance(self.bind_addr, basestring):
                try:
                    (host, port) = sock.getsockname()[:2]
                except socket.error, x:
                    if x.args[1] != 'Bad file descriptor':
                        raise
                else:
                    for res in socket.getaddrinfo(host, port, socket.AF_UNSPEC, socket.SOCK_STREAM):
                        (af, socktype, proto, canonname, sa) = res
                        s = None
                        try:
                            s = socket.socket(af, socktype, proto)
                            s.settimeout(1.0)
                            s.connect((host, port))
                            s.close()
                        except socket.error:
                            if s:
                                s.close()

            if hasattr(sock, 'close'):
                sock.close()
            self.socket = None
        for worker in self._workerThreads:
            self.requests.put(_SHUTDOWNREQUEST)

        current = threading.currentThread()
        while self._workerThreads:
            worker = self._workerThreads.pop()
            if worker is not current and worker.isAlive:
                try:
                    worker.join()
                except AssertionError:
                    pass

        return

    def populate_ssl_environ(self):
        """Create WSGI environ entries to be merged into each request."""
        cert = open(self.ssl_certificate).read()
        cert = crypto.load_certificate(crypto.FILETYPE_PEM, cert)
        self.ssl_environ = {}
        self.ssl_environ.update({'SSL_SERVER_M_VERSION': cert.get_version(), 'SSL_SERVER_M_SERIAL': cert.get_serial_number()})
        for (prefix, dn) in [('I', cert.get_issuer()), ('S', cert.get_subject())]:
            dnstr = str(dn)[18:-2]
            wsgikey = 'SSL_SERVER_%s_DN' % prefix
            self.ssl_environ[wsgikey] = dnstr
            while dnstr:
                pos = dnstr.rfind('=')
                dnstr, value = dnstr[:pos], dnstr[pos + 1:]
                pos = dnstr.rfind('/')
                dnstr, key = dnstr[:pos], dnstr[pos + 1:]
                if key and value:
                    wsgikey = 'SSL_SERVER_%s_DN_%s' % (prefix, key)
                    self.ssl_environ[wsgikey] = value