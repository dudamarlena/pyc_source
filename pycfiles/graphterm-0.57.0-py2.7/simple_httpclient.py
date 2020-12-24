# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.5-x86_64/egg/graphterm/bin/tornado/simple_httpclient.py
# Compiled at: 2012-01-23 23:44:33
from __future__ import with_statement
from tornado.escape import utf8, _unicode, native_str
from tornado.httpclient import HTTPRequest, HTTPResponse, HTTPError, AsyncHTTPClient, main
from tornado.httputil import HTTPHeaders
from tornado.iostream import IOStream, SSLIOStream
from tornado import stack_context
from tornado.util import b
import base64, collections, contextlib, copy, functools, logging, os.path, re, socket, sys, time, urlparse, zlib
try:
    from io import BytesIO
except ImportError:
    from cStringIO import StringIO as BytesIO

try:
    import ssl
except ImportError:
    ssl = None

_DEFAULT_CA_CERTS = os.path.dirname(__file__) + '/ca-certificates.crt'

class SimpleAsyncHTTPClient(AsyncHTTPClient):
    """Non-blocking HTTP client with no external dependencies.

    This class implements an HTTP 1.1 client on top of Tornado's IOStreams.
    It does not currently implement all applicable parts of the HTTP
    specification, but it does enough to work with major web service APIs
    (mostly tested against the Twitter API so far).

    This class has not been tested extensively in production and
    should be considered somewhat experimental as of the release of
    tornado 1.2.  It is intended to become the default AsyncHTTPClient
    implementation in a future release.  It may either be used
    directly, or to facilitate testing of this class with an existing
    application, setting the environment variable
    USE_SIMPLE_HTTPCLIENT=1 will cause this class to transparently
    replace tornado.httpclient.AsyncHTTPClient.

    Some features found in the curl-based AsyncHTTPClient are not yet
    supported.  In particular, proxies are not supported, connections
    are not reused, and callers cannot select the network interface to be
    used.

    Python 2.6 or higher is required for HTTPS support.  Users of Python 2.5
    should use the curl-based AsyncHTTPClient if HTTPS support is required.

    """

    def initialize(self, io_loop=None, max_clients=10, max_simultaneous_connections=None, hostname_mapping=None, max_buffer_size=104857600):
        """Creates a AsyncHTTPClient.

        Only a single AsyncHTTPClient instance exists per IOLoop
        in order to provide limitations on the number of pending connections.
        force_instance=True may be used to suppress this behavior.

        max_clients is the number of concurrent requests that can be in
        progress.  max_simultaneous_connections has no effect and is accepted
        only for compatibility with the curl-based AsyncHTTPClient.  Note
        that these arguments are only used when the client is first created,
        and will be ignored when an existing client is reused.

        hostname_mapping is a dictionary mapping hostnames to IP addresses.
        It can be used to make local DNS changes when modifying system-wide
        settings like /etc/hosts is not possible or desirable (e.g. in
        unittests).

        max_buffer_size is the number of bytes that can be read by IOStream. It
        defaults to 100mb.
        """
        self.io_loop = io_loop
        self.max_clients = max_clients
        self.queue = collections.deque()
        self.active = {}
        self.hostname_mapping = hostname_mapping
        self.max_buffer_size = max_buffer_size

    def fetch(self, request, callback, **kwargs):
        if not isinstance(request, HTTPRequest):
            request = HTTPRequest(url=request, **kwargs)
        if not isinstance(request.headers, HTTPHeaders):
            request.headers = HTTPHeaders(request.headers)
        callback = stack_context.wrap(callback)
        self.queue.append((request, callback))
        self._process_queue()
        if self.queue:
            logging.debug('max_clients limit reached, request queued. %d active, %d queued requests.' % (
             len(self.active), len(self.queue)))

    def _process_queue(self):
        with stack_context.NullContext():
            while self.queue and len(self.active) < self.max_clients:
                request, callback = self.queue.popleft()
                key = object()
                self.active[key] = (request, callback)
                _HTTPConnection(self.io_loop, self, request, functools.partial(self._release_fetch, key), callback, self.max_buffer_size)

    def _release_fetch(self, key):
        del self.active[key]
        self._process_queue()


class _HTTPConnection(object):
    _SUPPORTED_METHODS = set(['GET', 'HEAD', 'POST', 'PUT', 'DELETE'])

    def __init__(self, io_loop, client, request, release_callback, final_callback, max_buffer_size):
        self.start_time = time.time()
        self.io_loop = io_loop
        self.client = client
        self.request = request
        self.release_callback = release_callback
        self.final_callback = final_callback
        self.code = None
        self.headers = None
        self.chunks = None
        self._decompressor = None
        self._timeout = None
        with stack_context.StackContext(self.cleanup):
            parsed = urlparse.urlsplit(_unicode(self.request.url))
            if ssl is None and parsed.scheme == 'https':
                raise ValueError('HTTPS requires either python2.6+ or curl_httpclient')
            if parsed.scheme not in ('http', 'https'):
                raise ValueError('Unsupported url scheme: %s' % self.request.url)
            netloc = parsed.netloc
            if '@' in netloc:
                userpass, _, netloc = netloc.rpartition('@')
            match = re.match('^(.+):(\\d+)$', netloc)
            if match:
                host = match.group(1)
                port = int(match.group(2))
            else:
                host = netloc
                port = 443 if parsed.scheme == 'https' else 80
            if re.match('^\\[.*\\]$', host):
                host = host[1:-1]
            if self.client.hostname_mapping is not None:
                host = self.client.hostname_mapping.get(host, host)
            if request.allow_ipv6:
                af = socket.AF_UNSPEC
            else:
                af = socket.AF_INET
            addrinfo = socket.getaddrinfo(host, port, af, socket.SOCK_STREAM, 0, 0)
            af, socktype, proto, canonname, sockaddr = addrinfo[0]
            if parsed.scheme == 'https':
                ssl_options = {}
                if request.validate_cert:
                    ssl_options['cert_reqs'] = ssl.CERT_REQUIRED
                if request.ca_certs is not None:
                    ssl_options['ca_certs'] = request.ca_certs
                else:
                    ssl_options['ca_certs'] = _DEFAULT_CA_CERTS
                if request.client_key is not None:
                    ssl_options['keyfile'] = request.client_key
                if request.client_cert is not None:
                    ssl_options['certfile'] = request.client_cert
                if sys.version_info >= (2, 7):
                    ssl_options['ciphers'] = 'DEFAULT:!SSLv2'
                else:
                    ssl_options['ssl_version'] = ssl.PROTOCOL_SSLv3
                self.stream = SSLIOStream(socket.socket(af, socktype, proto), io_loop=self.io_loop, ssl_options=ssl_options, max_buffer_size=max_buffer_size)
            else:
                self.stream = IOStream(socket.socket(af, socktype, proto), io_loop=self.io_loop, max_buffer_size=max_buffer_size)
            timeout = min(request.connect_timeout, request.request_timeout)
            if timeout:
                self._timeout = self.io_loop.add_timeout(self.start_time + timeout, self._on_timeout)
            self.stream.set_close_callback(self._on_close)
            self.stream.connect(sockaddr, functools.partial(self._on_connect, parsed))
        return

    def _on_timeout(self):
        self._timeout = None
        self._run_callback(HTTPResponse(self.request, 599, request_time=time.time() - self.start_time, error=HTTPError(599, 'Timeout')))
        self.stream.close()
        return

    def _on_connect(self, parsed):
        if self._timeout is not None:
            self.io_loop.remove_timeout(self._timeout)
            self._timeout = None
        if self.request.request_timeout:
            self._timeout = self.io_loop.add_timeout(self.start_time + self.request.request_timeout, self._on_timeout)
        if self.request.validate_cert and isinstance(self.stream, SSLIOStream):
            match_hostname(self.stream.socket.getpeercert(), parsed.hostname)
        if self.request.method not in self._SUPPORTED_METHODS and not self.request.allow_nonstandard_methods:
            raise KeyError('unknown method %s' % self.request.method)
        for key in ('network_interface', 'proxy_host', 'proxy_port', 'proxy_username',
                    'proxy_password'):
            if getattr(self.request, key, None):
                raise NotImplementedError('%s not supported' % key)

        if 'Host' not in self.request.headers:
            self.request.headers['Host'] = parsed.netloc
        username, password = (None, None)
        if parsed.username is not None:
            username, password = parsed.username, parsed.password
        else:
            if self.request.auth_username is not None:
                username = self.request.auth_username
                password = self.request.auth_password or ''
            if username is not None:
                auth = utf8(username) + b(':') + utf8(password)
                self.request.headers['Authorization'] = b('Basic ') + base64.b64encode(auth)
            if self.request.user_agent:
                self.request.headers['User-Agent'] = self.request.user_agent
            if self.request.allow_nonstandard_methods or self.request.method in ('POST',
                                                                                 'PUT'):
                if not self.request.body is not None:
                    raise AssertionError
                else:
                    assert self.request.body is None
            if self.request.body is not None:
                self.request.headers['Content-Length'] = str(len(self.request.body))
            if self.request.method == 'POST' and 'Content-Type' not in self.request.headers:
                self.request.headers['Content-Type'] = 'application/x-www-form-urlencoded'
            if self.request.use_gzip:
                self.request.headers['Accept-Encoding'] = 'gzip'
            req_path = (parsed.path or '/') + ('?' + parsed.query if parsed.query else '')
            request_lines = [
             utf8('%s %s HTTP/1.1' % (self.request.method,
              req_path))]
            for k, v in self.request.headers.get_all():
                line = utf8(k) + b(': ') + utf8(v)
                if b('\n') in line:
                    raise ValueError('Newline in header: ' + repr(line))
                request_lines.append(line)

        self.stream.write(b('\r\n').join(request_lines) + b('\r\n\r\n'))
        if self.request.body is not None:
            self.stream.write(self.request.body)
        self.stream.read_until_regex(b('\r?\n\r?\n'), self._on_headers)
        return

    def _release(self):
        if self.release_callback is not None:
            release_callback = self.release_callback
            self.release_callback = None
            release_callback()
        return

    def _run_callback(self, response):
        self._release()
        if self.final_callback is not None:
            final_callback = self.final_callback
            self.final_callback = None
            final_callback(response)
        return

    @contextlib.contextmanager
    def cleanup(self):
        try:
            yield
        except Exception as e:
            logging.warning('uncaught exception', exc_info=True)
            self._run_callback(HTTPResponse(self.request, 599, error=e, request_time=time.time() - self.start_time))

    def _on_close(self):
        self._run_callback(HTTPResponse(self.request, 599, request_time=time.time() - self.start_time, error=HTTPError(599, 'Connection closed')))

    def _on_headers(self, data):
        data = native_str(data.decode('latin1'))
        first_line, _, header_data = data.partition('\n')
        match = re.match('HTTP/1.[01] ([0-9]+)', first_line)
        assert match
        self.code = int(match.group(1))
        self.headers = HTTPHeaders.parse(header_data)
        if 'Content-Length' in self.headers:
            if ',' in self.headers['Content-Length']:
                pieces = re.split(',\\s*', self.headers['Content-Length'])
                if any(i != pieces[0] for i in pieces):
                    raise ValueError('Multiple unequal Content-Lengths: %r' % self.headers['Content-Length'])
                self.headers['Content-Length'] = pieces[0]
            content_length = int(self.headers['Content-Length'])
        else:
            content_length = None
        if self.request.header_callback is not None:
            for k, v in self.headers.get_all():
                self.request.header_callback('%s: %s\r\n' % (k, v))

        if self.request.method == 'HEAD':
            self._on_body(b(''))
            return
        else:
            if 100 <= self.code < 200 or self.code in (204, 304):
                assert 'Transfer-Encoding' not in self.headers
                assert content_length in (None, 0)
                self._on_body(b(''))
                return
            if self.request.use_gzip and self.headers.get('Content-Encoding') == 'gzip':
                self._decompressor = zlib.decompressobj(16 + zlib.MAX_WBITS)
            if self.headers.get('Transfer-Encoding') == 'chunked':
                self.chunks = []
                self.stream.read_until(b('\r\n'), self._on_chunk_length)
            elif content_length is not None:
                self.stream.read_bytes(content_length, self._on_body)
            else:
                self.stream.read_until_close(self._on_body)
            return

    def _on_body(self, data):
        if self._timeout is not None:
            self.io_loop.remove_timeout(self._timeout)
            self._timeout = None
        original_request = getattr(self.request, 'original_request', self.request)
        if self.request.follow_redirects and self.request.max_redirects > 0 and self.code in (301,
                                                                                              302,
                                                                                              303,
                                                                                              307):
            new_request = copy.copy(self.request)
            new_request.url = urlparse.urljoin(self.request.url, self.headers['Location'])
            new_request.max_redirects -= 1
            del new_request.headers['Host']
            if self.code == 303:
                new_request.method = 'GET'
                new_request.body = None
                for h in ['Content-Length', 'Content-Type',
                 'Content-Encoding', 'Transfer-Encoding']:
                    try:
                        del self.request.headers[h]
                    except KeyError:
                        pass

            new_request.original_request = original_request
            final_callback = self.final_callback
            self.final_callback = None
            self._release()
            self.client.fetch(new_request, final_callback)
            self.stream.close()
            return
        else:
            if self._decompressor:
                data = self._decompressor.decompress(data)
            if self.request.streaming_callback:
                if self.chunks is None:
                    self.request.streaming_callback(data)
                buffer = BytesIO()
            else:
                buffer = BytesIO(data)
            response = HTTPResponse(original_request, self.code, headers=self.headers, request_time=time.time() - self.start_time, buffer=buffer, effective_url=self.request.url)
            self._run_callback(response)
            self.stream.close()
            return

    def _on_chunk_length(self, data):
        length = int(data.strip(), 16)
        if length == 0:
            self._decompressor = None
            self._on_body(b('').join(self.chunks))
        else:
            self.stream.read_bytes(length + 2, self._on_chunk_data)
        return

    def _on_chunk_data(self, data):
        assert data[-2:] == b('\r\n')
        chunk = data[:-2]
        if self._decompressor:
            chunk = self._decompressor.decompress(chunk)
        if self.request.streaming_callback is not None:
            self.request.streaming_callback(chunk)
        else:
            self.chunks.append(chunk)
        self.stream.read_until(b('\r\n'), self._on_chunk_length)
        return


class CertificateError(ValueError):
    pass


def _dnsname_to_pat(dn):
    pats = []
    for frag in dn.split('.'):
        if frag == '*':
            pats.append('[^.]+')
        else:
            frag = re.escape(frag)
            pats.append(frag.replace('\\*', '[^.]*'))

    return re.compile('\\A' + ('\\.').join(pats) + '\\Z', re.IGNORECASE)


def match_hostname(cert, hostname):
    """Verify that *cert* (in decoded format as returned by
    SSLSocket.getpeercert()) matches the *hostname*.  RFC 2818 rules
    are mostly followed, but IP addresses are not accepted for *hostname*.

    CertificateError is raised on failure. On success, the function
    returns nothing.
    """
    if not cert:
        raise ValueError('empty or no certificate')
    dnsnames = []
    san = cert.get('subjectAltName', ())
    for key, value in san:
        if key == 'DNS':
            if _dnsname_to_pat(value).match(hostname):
                return
            dnsnames.append(value)

    if not san:
        for sub in cert.get('subject', ()):
            for key, value in sub:
                if key == 'commonName':
                    if _dnsname_to_pat(value).match(hostname):
                        return
                    dnsnames.append(value)

    if len(dnsnames) > 1:
        raise CertificateError("hostname %r doesn't match either of %s" % (
         hostname, (', ').join(map(repr, dnsnames))))
    elif len(dnsnames) == 1:
        raise CertificateError("hostname %r doesn't match %r" % (
         hostname, dnsnames[0]))
    else:
        raise CertificateError('no appropriate commonName or subjectAltName fields were found')


if __name__ == '__main__':
    AsyncHTTPClient.configure(SimpleAsyncHTTPClient)
    main()