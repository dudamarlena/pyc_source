# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/amcnabb/python/mrs/http.py
# Compiled at: 2012-11-14 14:43:06
"""Mrs. HTTP

RPC mechanisms and HTTP servers built on Python's standard library.
"""
BACKLOG = 1024
PROCESS_REQUESTS_THREADS = 20
RETRIES = 10
RETRY_DELAY = 5
import errno, os, posixpath, socket, sys, threading, time
try:
    from http.client import HTTPConnection
    from http.server import SimpleHTTPRequestHandler
    from urllib.parse import urlsplit, urlunsplit, unquote
    import queue, socketserver
    from xmlrpc.client import ServerProxy, Transport
    from xmlrpc.server import SimpleXMLRPCRequestHandler, SimpleXMLRPCServer
except ImportError:
    from httplib import HTTPConnection
    from SimpleHTTPServer import SimpleHTTPRequestHandler
    from SimpleXMLRPCServer import SimpleXMLRPCRequestHandler, SimpleXMLRPCServer
    import Queue as queue, SocketServer as socketserver
    from urllib import unquote
    from urlparse import urlsplit, urlunsplit
    from xmlrpclib import ServerProxy, Transport

import logging
logger = logging.getLogger('mrs')
del logging
import codecs
codecs.lookup('ascii')
PY3 = sys.version_info[0] == 3
if not PY3:
    range = xrange

class TimeoutTransport(Transport):
    """An RPC transport that supports timeouts and retries."""

    def __init__(self, timeout):
        Transport.__init__(self)
        self.timeout = timeout

    def request(self, host, *args, **kwds):
        for i in range(RETRIES):
            try:
                return Transport.request(self, host, *args, **kwds)
            except socket.timeout:
                logger.error('RPC to %s failed: timed out.' % host)
                time.sleep(RETRY_DELAY)
                continue
            except socket.error as e:
                if e.errno == errno.ECONNREFUSED:
                    logger.error('RPC to %s failed: connection refused.' % host)
                    continue
                else:
                    logger.error('RPC to %s failed: %s' % (
                     host, str(e)))
                    break

        raise ConnectionFailed(host)

    def make_connection(self, host):
        if self._connection and host == self._connection[0]:
            return self._connection[1]
        chost, self._extra_headers, x509 = self.get_host_info(host)
        if self.timeout:
            self._connection = (
             host,
             NoDelayHTTPConnection(chost, timeout=self.timeout))
        else:
            self._connection = (
             host, NoDelayHTTPConnection(chost))
        return self._connection[1]

    if sys.version_info[0] == 2 and sys.version_info[1] < 7:

        def make_connection(self, host):
            prev = socket.getdefaulttimeout()
            socket.setdefaulttimeout(self.timeout)
            value = Transport.make_connection(self, host)
            socket.setdefaulttimeout(prev)
            return value


class NoDelayHTTPConnection(HTTPConnection):
    """HTTPConnection with Nagle's algorithm disabled (TCP_NODELAY enabled)."""

    def connect(self):
        HTTPConnection.connect(self)
        self.sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)


class TimeoutServerProxy(ServerProxy):
    """An RPC client that supports timeouts and retries."""

    def __init__(self, uri, timeout):
        transport = TimeoutTransport(timeout)
        uri = rpc_url(uri)
        ServerProxy.__init__(self, uri, transport=transport)


class ThreadPoolMixIn(socketserver.ThreadingMixIn):
    queue = None

    def process_request(self, request, client_address):
        if self.queue is None:
            self.queue = queue.Queue()
            for i in range(PROCESS_REQUESTS_THREADS):
                t = threading.Thread(target=self.process_requests_thread)
                t.daemon = True
                t.start()

        self.queue.put((request, client_address))
        return

    def process_requests_thread(self):
        while True:
            request, client_address = self.queue.get()
            self.process_request_thread(request, client_address)


class RPCRequestHandler(SimpleXMLRPCRequestHandler):
    """Simple HTTP request handler
    """
    protocol_version = 'HTTP/1.1'
    disable_nagle_algorithm = True
    if not hasattr(SimpleHTTPRequestHandler, 'disable_nagle_algorithm'):

        def setup(self):
            SimpleHTTPRequestHandler.setup(self)
            if self.disable_nagle_algorithm:
                self.connection.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, True)

    def _dispatch(self, method, params):
        host, _ = self.client_address
        return self.server._dispatch(method, params, host)


class RPCServer(SimpleXMLRPCServer):
    """XMLRPC Server that supports passing the client host to the method.

    This server takes an instance used for dispatching requests; methods of
    the instance beginning with 'xmlrpc_' are called.  If the uses_host
    attribute is set on the method, then the host is passed as a keyword
    argument.
    """
    request_queue_size = BACKLOG

    def __init__(self, addr, instance):
        SimpleXMLRPCServer.__init__(self, addr, requestHandler=RPCRequestHandler, logRequests=False)
        self.instance = instance

    def _dispatch(self, method, params, host):
        try:
            func = getattr(self.instance, 'xmlrpc_' + method)
        except AttributeError:
            raise RuntimeError('method "%s" is not supported' % method)

        try:
            if hasattr(func, 'uses_host'):
                return func(host=host, *params)
            else:
                return func(*params)

        except Exception as e:
            import traceback
            msg = 'Exception in RPC Server: %s' % e
            logger.critical(msg)
            tb = traceback.format_exc()
            msg = 'Traceback: %s' % tb
            logger.error(msg)
            raise


class ThreadingRPCServer(socketserver.ThreadingMixIn, RPCServer):
    pass


def uses_host(f):
    """Decorate f with the attribute `uses_host`.

    When XMLRPC renders the given XML RPC method, it will pass the host
    as a named argument.
    """
    f.uses_host = True
    return f


def rpc_url(urlstring):
    """Tidy a URL to be used to connect to an XML RPC server.

    >>> rpc_url('http://localhost')
    'http://localhost/RPC2'
    >>> rpc_url('localhost:8080')
    'http://localhost:8080/RPC2'
    >>> rpc_url('http://localhost/')
    'http://localhost/'
    >>> rpc_url('http://localhost/path/to/xmlrpc')
    'http://localhost/path/to/xmlrpc'
    >>> rpc_url('localhost/path/to/xmlrpc')
    'http://localhost/path/to/xmlrpc'
    >>>
    """
    if '://' not in urlstring:
        urlstring = 'http://' + urlstring
    scheme, netloc, path, query, fragment = urlsplit(urlstring)
    if not path and not query and not fragment:
        path = '/RPC2'
    return urlunsplit((scheme, netloc, path, query, fragment))


class BucketRequestHandler(SimpleHTTPRequestHandler):
    """HTTP request handler for serving buckets from local datasets."""
    wbufsize = -1
    disable_nagle_algorithm = True
    if not hasattr(SimpleHTTPRequestHandler, 'disable_nagle_algorithm'):

        def setup(self):
            SimpleHTTPRequestHandler.setup(self)
            if self.disable_nagle_algorithm:
                self.connection.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, True)

    def list_directory(self, path):
        self.send_error(403, 'Directory listing is forbidden')

    def translate_path(self, path):
        path = path.split('?', 1)[0]
        path = path.split('#', 1)[0]
        path = posixpath.normpath(unquote(path)).lstrip('/')
        words = path.split('/')
        if words[0] == '..':
            self.send_error(403, 'Forbidden')
            return
        return os.path.join(self.server.basedir, *words)

    def log_request(self, *args, **kwds):
        pass

    def guess_type(self, path):
        return 'application/octet-stream'


class BucketServer(socketserver.TCPServer):
    """HTTP server for serving buckets from local datasets."""
    request_queue_size = BACKLOG

    def __init__(self, addr, basedir):
        socketserver.TCPServer.__init__(self, addr, BucketRequestHandler)
        self.basedir = basedir


class ThreadingBucketServer(ThreadPoolMixIn, BucketServer):
    pass


class ConnectionFailed(Exception):
    """Exception for when an RPC request fails too many times."""

    def __init__(self, addr):
        self.addr = addr

    def __str__(self):
        return 'Connection to %s refused too many times' % self.addr