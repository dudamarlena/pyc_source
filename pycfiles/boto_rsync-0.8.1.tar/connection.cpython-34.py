# uncompyle6 version 3.6.7
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.10-x86_64/egg/boto/connection.py
# Compiled at: 2015-11-24 05:02:18
# Size of source mod 2**32: 50964 bytes
__doc__ = '\nHandles basic connections to AWS\n'
from datetime import datetime
import errno, os, random, re, socket, sys, time, xml.sax, copy
from boto import auth
from boto import auth_handler
import boto, boto.utils, boto.handler, boto.cacerts
from boto import config, UserAgent
from boto.compat import six, http_client, urlparse, quote, encodebytes
from boto.exception import AWSConnectionError
from boto.exception import BotoClientError
from boto.exception import BotoServerError
from boto.exception import PleaseRetryException
from boto.provider import Provider
from boto.resultset import ResultSet
HAVE_HTTPS_CONNECTION = False
try:
    import ssl
    from boto import https_connection
    if hasattr(ssl, 'SSLError'):
        HAVE_HTTPS_CONNECTION = True
except ImportError:
    pass

try:
    import threading
except ImportError:
    import dummy_threading as threading

ON_APP_ENGINE = all(key in os.environ for key in (
 'USER_IS_ADMIN', 'CURRENT_VERSION_ID', 'APPLICATION_ID'))
PORTS_BY_SECURITY = {True: 443,  False: 80}
DEFAULT_CA_CERTS_FILE = os.path.join(os.path.dirname(os.path.abspath(boto.cacerts.__file__)), 'cacerts.txt')

class HostConnectionPool(object):
    """HostConnectionPool"""

    def __init__(self):
        self.queue = []

    def size(self):
        """
        Returns the number of connections in the pool for this host.
        Some of the connections may still be in use, and may not be
        ready to be returned by get().
        """
        return len(self.queue)

    def put(self, conn):
        """
        Adds a connection to the pool, along with the time it was
        added.
        """
        self.queue.append((conn, time.time()))

    def get(self):
        """
        Returns the next connection in this pool that is ready to be
        reused.  Returns None if there aren't any.
        """
        self.clean()
        for _ in range(len(self.queue)):
            conn, _ = self.queue.pop(0)
            if self._conn_ready(conn):
                return conn
            self.put(conn)

    def _conn_ready(self, conn):
        """
        There is a nice state diagram at the top of http_client.py.  It
        indicates that once the response headers have been read (which
        _mexe does before adding the connection to the pool), a
        response is attached to the connection, and it stays there
        until it's done reading.  This isn't entirely true: even after
        the client is done reading, the response may be closed, but
        not removed from the connection yet.

        This is ugly, reading a private instance variable, but the
        state we care about isn't available in any public methods.
        """
        if ON_APP_ENGINE:
            return False
        else:
            response = getattr(conn, '_HTTPConnection__response', None)
            return response is None or response.isclosed()

    def clean(self):
        """
        Get rid of stale connections.
        """
        while len(self.queue) > 0 and self._pair_stale(self.queue[0]):
            self.queue.pop(0)

    def _pair_stale(self, pair):
        """
        Returns true of the (connection,time) pair is too old to be
        used.
        """
        _conn, return_time = pair
        now = time.time()
        return return_time + ConnectionPool.STALE_DURATION < now


class ConnectionPool(object):
    """ConnectionPool"""
    CLEAN_INTERVAL = 5.0
    STALE_DURATION = 60.0

    def __init__(self):
        self.host_to_pool = {}
        self.last_clean_time = 0.0
        self.mutex = threading.Lock()
        ConnectionPool.STALE_DURATION = config.getfloat('Boto', 'connection_stale_duration', ConnectionPool.STALE_DURATION)

    def __getstate__(self):
        pickled_dict = copy.copy(self.__dict__)
        pickled_dict['host_to_pool'] = {}
        del pickled_dict['mutex']
        return pickled_dict

    def __setstate__(self, dct):
        self.__init__()

    def size(self):
        """
        Returns the number of connections in the pool.
        """
        return sum(pool.size() for pool in self.host_to_pool.values())

    def get_http_connection(self, host, port, is_secure):
        """
        Gets a connection from the pool for the named host.  Returns
        None if there is no connection that can be reused. It's the caller's
        responsibility to call close() on the connection when it's no longer
        needed.
        """
        self.clean()
        with self.mutex:
            key = (
             host, port, is_secure)
            if key not in self.host_to_pool:
                return
            else:
                return self.host_to_pool[key].get()

    def put_http_connection(self, host, port, is_secure, conn):
        """
        Adds a connection to the pool of connections that can be
        reused for the named host.
        """
        with self.mutex:
            key = (
             host, port, is_secure)
            if key not in self.host_to_pool:
                self.host_to_pool[key] = HostConnectionPool()
            self.host_to_pool[key].put(conn)

    def clean(self):
        """
        Clean up the stale connections in all of the pools, and then
        get rid of empty pools.  Pools clean themselves every time a
        connection is fetched; this cleaning takes care of pools that
        aren't being used any more, so nothing is being gotten from
        them.
        """
        with self.mutex:
            now = time.time()
            if self.last_clean_time + self.CLEAN_INTERVAL < now:
                to_remove = []
                for host, pool in self.host_to_pool.items():
                    pool.clean()
                    if pool.size() == 0:
                        to_remove.append(host)
                        continue

                for host in to_remove:
                    del self.host_to_pool[host]

                self.last_clean_time = now


class HTTPRequest(object):

    def __init__(self, method, protocol, host, port, path, auth_path, params, headers, body):
        """Represents an HTTP request.

        :type method: string
        :param method: The HTTP method name, 'GET', 'POST', 'PUT' etc.

        :type protocol: string
        :param protocol: The http protocol used, 'http' or 'https'.

        :type host: string
        :param host: Host to which the request is addressed. eg. abc.com

        :type port: int
        :param port: port on which the request is being sent. Zero means unset,
            in which case default port will be chosen.

        :type path: string
        :param path: URL path that is being accessed.

        :type auth_path: string
        :param path: The part of the URL path used when creating the
            authentication string.

        :type params: dict
        :param params: HTTP url query parameters, with key as name of
            the param, and value as value of param.

        :type headers: dict
        :param headers: HTTP headers, with key as name of the header and value
            as value of header.

        :type body: string
        :param body: Body of the HTTP request. If not present, will be None or
            empty string ('').
        """
        self.method = method
        self.protocol = protocol
        self.host = host
        self.port = port
        self.path = path
        if auth_path is None:
            auth_path = path
        self.auth_path = auth_path
        self.params = params
        if headers and 'Transfer-Encoding' in headers and headers['Transfer-Encoding'] == 'chunked' and self.method != 'PUT':
            self.headers = headers.copy()
            del self.headers['Transfer-Encoding']
        else:
            self.headers = headers
        self.body = body

    def __str__(self):
        return 'method:(%s) protocol:(%s) host(%s) port(%s) path(%s) params(%s) headers(%s) body(%s)' % (
         self.method,
         self.protocol, self.host, self.port, self.path, self.params,
         self.headers, self.body)

    def authorize(self, connection, **kwargs):
        if not getattr(self, '_headers_quoted', False):
            for key in self.headers:
                val = self.headers[key]
                if isinstance(val, six.text_type):
                    safe = '!"#$%&\'()*+,/:;<=>?@[\\]^`{|}~'
                    self.headers[key] = quote(val.encode('utf-8'), safe)
                    continue

            setattr(self, '_headers_quoted', True)
        self.headers['User-Agent'] = UserAgent
        connection._auth_handler.add_auth(self, **kwargs)
        if 'Content-Length' not in self.headers:
            if 'Transfer-Encoding' not in self.headers or self.headers['Transfer-Encoding'] != 'chunked':
                self.headers['Content-Length'] = str(len(self.body))


class HTTPResponse(http_client.HTTPResponse):

    def __init__(self, *args, **kwargs):
        http_client.HTTPResponse.__init__(self, *args, **kwargs)
        self._cached_response = ''

    def read(self, amt=None):
        """Read the response.

        This method does not have the same behavior as
        http_client.HTTPResponse.read.  Instead, if this method is called with
        no ``amt`` arg, then the response body will be cached.  Subsequent
        calls to ``read()`` with no args **will return the cached response**.

        """
        if amt is None:
            if not self._cached_response:
                self._cached_response = http_client.HTTPResponse.read(self)
            return self._cached_response
        else:
            return http_client.HTTPResponse.read(self, amt)


class AWSAuthConnection(object):

    def __init__(self, host, aws_access_key_id=None, aws_secret_access_key=None, is_secure=True, port=None, proxy=None, proxy_port=None, proxy_user=None, proxy_pass=None, debug=0, https_connection_factory=None, path='/', provider='aws', security_token=None, suppress_consec_slashes=True, validate_certs=True, profile_name=None):
        """
        :type host: str
        :param host: The host to make the connection to

        :keyword str aws_access_key_id: Your AWS Access Key ID (provided by
            Amazon). If none is specified, the value in your
            ``AWS_ACCESS_KEY_ID`` environmental variable is used.
        :keyword str aws_secret_access_key: Your AWS Secret Access Key
            (provided by Amazon). If none is specified, the value in your
            ``AWS_SECRET_ACCESS_KEY`` environmental variable is used.
        :keyword str security_token: The security token associated with
            temporary credentials issued by STS.  Optional unless using
            temporary credentials.  If none is specified, the environment
            variable ``AWS_SECURITY_TOKEN`` is used if defined.

        :type is_secure: boolean
        :param is_secure: Whether the connection is over SSL

        :type https_connection_factory: list or tuple
        :param https_connection_factory: A pair of an HTTP connection
            factory and the exceptions to catch.  The factory should have
            a similar interface to L{http_client.HTTPSConnection}.

        :param str proxy: Address/hostname for a proxy server

        :type proxy_port: int
        :param proxy_port: The port to use when connecting over a proxy

        :type proxy_user: str
        :param proxy_user: The username to connect with on the proxy

        :type proxy_pass: str
        :param proxy_pass: The password to use when connection over a proxy.

        :type port: int
        :param port: The port to use to connect

        :type suppress_consec_slashes: bool
        :param suppress_consec_slashes: If provided, controls whether
            consecutive slashes will be suppressed in key paths.

        :type validate_certs: bool
        :param validate_certs: Controls whether SSL certificates
            will be validated or not.  Defaults to True.

        :type profile_name: str
        :param profile_name: Override usual Credentials section in config
            file to use a named set of keys instead.
        """
        self.suppress_consec_slashes = suppress_consec_slashes
        self.num_retries = 6
        if config.has_option('Boto', 'is_secure'):
            is_secure = config.getboolean('Boto', 'is_secure')
        self.is_secure = is_secure
        self.https_validate_certificates = config.getbool('Boto', 'https_validate_certificates', validate_certs)
        if self.https_validate_certificates and not HAVE_HTTPS_CONNECTION:
            raise BotoClientError('SSL server certificate validation is enabled in boto configuration, but Python dependencies required to support this feature are not available. Certificate validation is only supported when running under Python 2.6 or later.')
        certs_file = config.get_value('Boto', 'ca_certificates_file', DEFAULT_CA_CERTS_FILE)
        if certs_file == 'system':
            certs_file = None
        self.ca_certificates_file = certs_file
        if port:
            self.port = port
        else:
            self.port = PORTS_BY_SECURITY[is_secure]
        self.handle_proxy(proxy, proxy_port, proxy_user, proxy_pass)
        self.http_exceptions = (
         http_client.HTTPException, socket.error,
         socket.gaierror, http_client.BadStatusLine)
        self.http_unretryable_exceptions = []
        if HAVE_HTTPS_CONNECTION:
            self.http_unretryable_exceptions.append(https_connection.InvalidCertificateException)
        self.socket_exception_values = (
         errno.EINTR,)
        if https_connection_factory is not None:
            self.https_connection_factory = https_connection_factory[0]
            self.http_exceptions += https_connection_factory[1]
        else:
            self.https_connection_factory = None
        if is_secure:
            self.protocol = 'https'
        else:
            self.protocol = 'http'
        self.host = host
        self.path = path
        if not isinstance(debug, six.integer_types):
            debug = 0
        self.debug = config.getint('Boto', 'debug', debug)
        self.host_header = None
        self.http_connection_kwargs = {}
        if (
         sys.version_info[0], sys.version_info[1]) >= (2, 6):
            self.http_connection_kwargs['timeout'] = config.getint('Boto', 'http_socket_timeout', 70)
        if isinstance(provider, Provider):
            self.provider = provider
        else:
            self._provider_type = provider
            self.provider = Provider(self._provider_type, aws_access_key_id, aws_secret_access_key, security_token, profile_name)
        if self.provider.host:
            self.host = self.provider.host
        if self.provider.port:
            self.port = self.provider.port
        if self.provider.host_header:
            self.host_header = self.provider.host_header
        self._pool = ConnectionPool()
        self._connection = (self.host, self.port, self.is_secure)
        self._last_rs = None
        self._auth_handler = auth.get_auth_handler(host, config, self.provider, self._required_auth_capability())
        if getattr(self, 'AuthServiceName', None) is not None:
            self.auth_service_name = self.AuthServiceName
        self.request_hook = None

    def __repr__(self):
        return '%s:%s' % (self.__class__.__name__, self.host)

    def _required_auth_capability(self):
        return []

    def _get_auth_service_name(self):
        return getattr(self._auth_handler, 'service_name')

    def _set_auth_service_name(self, value):
        self._auth_handler.service_name = value

    auth_service_name = property(_get_auth_service_name, _set_auth_service_name)

    def _get_auth_region_name(self):
        return getattr(self._auth_handler, 'region_name')

    def _set_auth_region_name(self, value):
        self._auth_handler.region_name = value

    auth_region_name = property(_get_auth_region_name, _set_auth_region_name)

    def connection(self):
        return self.get_http_connection(*self._connection)

    connection = property(connection)

    def aws_access_key_id(self):
        return self.provider.access_key

    aws_access_key_id = property(aws_access_key_id)
    gs_access_key_id = aws_access_key_id
    access_key = aws_access_key_id

    def aws_secret_access_key(self):
        return self.provider.secret_key

    aws_secret_access_key = property(aws_secret_access_key)
    gs_secret_access_key = aws_secret_access_key
    secret_key = aws_secret_access_key

    def profile_name(self):
        return self.provider.profile_name

    profile_name = property(profile_name)

    def get_path(self, path='/'):
        if not self.suppress_consec_slashes:
            return self.path + re.sub('^(/*)/', '\\1', path)
        pos = path.find('?')
        if pos >= 0:
            params = path[pos:]
            path = path[:pos]
        else:
            params = None
        if path[(-1)] == '/':
            need_trailing = True
        else:
            need_trailing = False
        path_elements = self.path.split('/')
        path_elements.extend(path.split('/'))
        path_elements = [p for p in path_elements if p]
        path = '/' + '/'.join(path_elements)
        if path[(-1)] != '/' and need_trailing:
            path += '/'
        if params:
            path = path + params
        return path

    def server_name(self, port=None):
        if not port:
            port = self.port
        if port == 80:
            signature_host = self.host
        else:
            if (ON_APP_ENGINE and sys.version[:3] == '2.5' or sys.version[:3] in ('2.6',
                                                                                  '2.7')) and port == 443:
                signature_host = self.host
            else:
                signature_host = '%s:%d' % (self.host, port)
        return signature_host

    def handle_proxy(self, proxy, proxy_port, proxy_user, proxy_pass):
        self.proxy = proxy
        self.proxy_port = proxy_port
        self.proxy_user = proxy_user
        self.proxy_pass = proxy_pass
        if 'http_proxy' in os.environ and not self.proxy:
            pattern = re.compile('(?:http://)?(?:(?P<user>[\\w\\-\\.]+):(?P<pass>.*)@)?(?P<host>[\\w\\-\\.]+)(?::(?P<port>\\d+))?')
            match = pattern.match(os.environ['http_proxy'])
            if match:
                self.proxy = match.group('host')
                self.proxy_port = match.group('port')
                self.proxy_user = match.group('user')
                self.proxy_pass = match.group('pass')
        elif not self.proxy:
            self.proxy = config.get_value('Boto', 'proxy', None)
        if not self.proxy_port:
            self.proxy_port = config.get_value('Boto', 'proxy_port', None)
        if not self.proxy_user:
            self.proxy_user = config.get_value('Boto', 'proxy_user', None)
        if not self.proxy_pass:
            self.proxy_pass = config.get_value('Boto', 'proxy_pass', None)
        if not self.proxy_port and self.proxy:
            print('http_proxy environment variable does not specify a port, using default')
            self.proxy_port = self.port
        self.no_proxy = os.environ.get('no_proxy', '') or os.environ.get('NO_PROXY', '')
        self.use_proxy = self.proxy is not None

    def get_http_connection(self, host, port, is_secure):
        conn = self._pool.get_http_connection(host, port, is_secure)
        if conn is not None:
            return conn
        else:
            return self.new_http_connection(host, port, is_secure)

    def skip_proxy(self, host):
        if not self.no_proxy:
            return False
        if self.no_proxy == '*':
            return True
        hostonly = host
        hostonly = host.split(':')[0]
        for name in self.no_proxy.split(','):
            if name and (hostonly.endswith(name) or host.endswith(name)):
                return True

        return False

    def new_http_connection(self, host, port, is_secure):
        if host is None:
            host = self.server_name()
        host = boto.utils.parse_host(host)
        http_connection_kwargs = self.http_connection_kwargs.copy()
        http_connection_kwargs['port'] = port
        if self.use_proxy and not is_secure and not self.skip_proxy(host):
            host = self.proxy
            http_connection_kwargs['port'] = int(self.proxy_port)
        if is_secure:
            boto.log.debug('establishing HTTPS connection: host=%s, kwargs=%s', host, http_connection_kwargs)
            if self.use_proxy and not self.skip_proxy(host):
                connection = self.proxy_ssl(host, is_secure and 443 or 80)
            else:
                if self.https_connection_factory:
                    connection = self.https_connection_factory(host)
                else:
                    if self.https_validate_certificates and HAVE_HTTPS_CONNECTION:
                        connection = https_connection.CertValidatingHTTPSConnection(host, ca_certs=self.ca_certificates_file, **http_connection_kwargs)
                    else:
                        connection = http_client.HTTPSConnection(host, **http_connection_kwargs)
        else:
            boto.log.debug('establishing HTTP connection: kwargs=%s' % http_connection_kwargs)
            if self.https_connection_factory:
                connection = self.https_connection_factory(host, **http_connection_kwargs)
            else:
                connection = http_client.HTTPConnection(host, **http_connection_kwargs)
        if self.debug > 1:
            connection.set_debuglevel(self.debug)
        if host.split(':')[0] == self.host and is_secure == self.is_secure:
            self._connection = (
             host, port, is_secure)
        connection.response_class = HTTPResponse
        return connection

    def put_http_connection(self, host, port, is_secure, connection):
        self._pool.put_http_connection(host, port, is_secure, connection)

    def proxy_ssl(self, host=None, port=None):
        if host and port:
            host = '%s:%d' % (host, port)
        else:
            host = '%s:%d' % (self.host, self.port)
        timeout = self.http_connection_kwargs.get('timeout')
        if timeout is not None:
            sock = socket.create_connection((self.proxy,
             int(self.proxy_port)), timeout)
        else:
            sock = socket.create_connection((self.proxy, int(self.proxy_port)))
        boto.log.debug('Proxy connection: CONNECT %s HTTP/1.0\r\n', host)
        sock.sendall('CONNECT %s HTTP/1.0\r\n' % host)
        sock.sendall('User-Agent: %s\r\n' % UserAgent)
        if self.proxy_user and self.proxy_pass:
            for k, v in self.get_proxy_auth_header().items():
                sock.sendall('%s: %s\r\n' % (k, v))

            if config.getbool('Boto', 'send_crlf_after_proxy_auth_headers', False):
                sock.sendall('\r\n')
        else:
            sock.sendall('\r\n')
        resp = http_client.HTTPResponse(sock, strict=True, debuglevel=self.debug)
        resp.begin()
        if resp.status != 200:
            raise socket.error(-71, 'Error talking to HTTP proxy %s:%s: %s (%s)' % (
             self.proxy, self.proxy_port,
             resp.status, resp.reason))
        resp.close()
        h = http_client.HTTPConnection(host)
        if self.https_validate_certificates and HAVE_HTTPS_CONNECTION:
            msg = 'wrapping ssl socket for proxied connection; '
            if self.ca_certificates_file:
                msg += 'CA certificate file=%s' % self.ca_certificates_file
            else:
                msg += 'using system provided SSL certs'
            boto.log.debug(msg)
            key_file = self.http_connection_kwargs.get('key_file', None)
            cert_file = self.http_connection_kwargs.get('cert_file', None)
            sslSock = ssl.wrap_socket(sock, keyfile=key_file, certfile=cert_file, cert_reqs=ssl.CERT_REQUIRED, ca_certs=self.ca_certificates_file)
            cert = sslSock.getpeercert()
            hostname = self.host.split(':', 0)[0]
            if not https_connection.ValidateCertificateHostname(cert, hostname):
                raise https_connection.InvalidCertificateException(hostname, cert, 'hostname mismatch')
        else:
            if hasattr(http_client, 'ssl'):
                sslSock = http_client.ssl.SSLSocket(sock)
            else:
                sslSock = socket.ssl(sock, None, None)
                sslSock = http_client.FakeSocket(sock, sslSock)
        h.sock = sslSock
        return h

    def prefix_proxy_to_path(self, path, host=None):
        path = self.protocol + '://' + (host or self.server_name()) + path
        return path

    def get_proxy_auth_header(self):
        auth = encodebytes(self.proxy_user + ':' + self.proxy_pass)
        return {'Proxy-Authorization': 'Basic %s' % auth}

    def get_proxy_url_with_auth(self):
        if not self.use_proxy:
            return
        if self.proxy_user or self.proxy_pass:
            if self.proxy_pass:
                login_info = '%s:%s@' % (self.proxy_user, self.proxy_pass)
            else:
                login_info = '%s@' % self.proxy_user
        else:
            login_info = ''
        return 'http://%s%s:%s' % (login_info, self.proxy, str(self.proxy_port or self.port))

    def set_host_header(self, request):
        try:
            request.headers['Host'] = self._auth_handler.host_header(self.host, request)
        except AttributeError:
            request.headers['Host'] = self.host.split(':', 1)[0]

    def set_request_hook(self, hook):
        self.request_hook = hook

    def _mexe(self, request, sender=None, override_num_retries=None, retry_handler=None):
        """
        mexe - Multi-execute inside a loop, retrying multiple times to handle
               transient Internet errors by simply trying again.
               Also handles redirects.

        This code was inspired by the S3Utils classes posted to the boto-users
        Google group by Larry Bates.  Thanks!

        """
        boto.log.debug('Method: %s' % request.method)
        boto.log.debug('Path: %s' % request.path)
        boto.log.debug('Data: %s' % request.body)
        boto.log.debug('Headers: %s' % request.headers)
        boto.log.debug('Host: %s' % request.host)
        boto.log.debug('Port: %s' % request.port)
        boto.log.debug('Params: %s' % request.params)
        response = None
        body = None
        ex = None
        if override_num_retries is None:
            num_retries = config.getint('Boto', 'num_retries', self.num_retries)
        else:
            num_retries = override_num_retries
        i = 0
        connection = self.get_http_connection(request.host, request.port, self.is_secure)
        if not isinstance(request.body, bytes) and hasattr(request.body, 'encode'):
            request.body = request.body.encode('utf-8')
        while i <= num_retries:
            next_sleep = min(random.random() * 2 ** i, boto.config.get('Boto', 'max_retry_delay', 60))
            try:
                boto.log.debug('Token: %s' % self.provider.security_token)
                request.authorize(connection=self)
                if 's3' not in self._required_auth_capability():
                    if not getattr(self, 'anon', False):
                        if not request.headers.get('Host'):
                            self.set_host_header(request)
                    boto.log.debug('Final headers: %s' % request.headers)
                    request.start_time = datetime.now()
                    if callable(sender):
                        response = sender(connection, request.method, request.path, request.body, request.headers)
                else:
                    connection.request(request.method, request.path, request.body, request.headers)
                    response = connection.getresponse()
                boto.log.debug('Response headers: %s' % response.getheaders())
                location = response.getheader('location')
                if request.method == 'HEAD' and getattr(response, 'chunked', False):
                    response.chunked = 0
                if callable(retry_handler):
                    status = retry_handler(response, i, next_sleep)
                    if status:
                        msg, i, next_sleep = status
                        if msg:
                            boto.log.debug(msg)
                        time.sleep(next_sleep)
                        continue
                    if response.status in (500, 502, 503, 504):
                        msg = 'Received %d response.  ' % response.status
                        msg += 'Retrying in %3.1f seconds' % next_sleep
                        boto.log.debug(msg)
                        body = response.read()
                        if isinstance(body, bytes):
                            body = body.decode('utf-8')
                else:
                    if response.status < 300 or response.status >= 400 or not location:
                        conn_header_value = response.getheader('connection')
                        if conn_header_value == 'close':
                            connection.close()
                        else:
                            self.put_http_connection(request.host, request.port, self.is_secure, connection)
                        if self.request_hook is not None:
                            self.request_hook.handle_request_data(request, response)
                        return response
                    scheme, request.host, request.path, params, query, fragment = urlparse(location)
                    if query:
                        request.path += '?' + query
                    if ':' in request.host:
                        request.host, request.port = request.host.split(':', 1)
                    msg = 'Redirecting: %s' % scheme + '://'
                    msg += request.host + request.path
                    boto.log.debug(msg)
                    connection = self.get_http_connection(request.host, request.port, scheme == 'https')
                    response = None
                    continue
            except PleaseRetryException as e:
                boto.log.debug('encountered a retry exception: %s' % e)
                connection = self.new_http_connection(request.host, request.port, self.is_secure)
                response = e.response
                ex = e
            except self.http_exceptions as e:
                for unretryable in self.http_unretryable_exceptions:
                    if isinstance(e, unretryable):
                        boto.log.debug('encountered unretryable %s exception, re-raising' % e.__class__.__name__)
                        raise
                        continue

                boto.log.debug('encountered %s exception, reconnecting' % e.__class__.__name__)
                connection = self.new_http_connection(request.host, request.port, self.is_secure)
                ex = e

            time.sleep(next_sleep)
            i += 1

        if self.request_hook is not None:
            self.request_hook.handle_request_data(request, response, error=True)
        if response:
            raise BotoServerError(response.status, response.reason, body)
        else:
            if ex:
                raise ex
            else:
                msg = 'Please report this exception as a Boto Issue!'
                raise BotoClientError(msg)

    def build_base_http_request(self, method, path, auth_path, params=None, headers=None, data='', host=None):
        path = self.get_path(path)
        if auth_path is not None:
            auth_path = self.get_path(auth_path)
        if params is None:
            params = {}
        else:
            params = params.copy()
        if headers is None:
            headers = {}
        else:
            headers = headers.copy()
        if self.host_header and not boto.utils.find_matching_headers('host', headers):
            headers['host'] = self.host_header
        host = host or self.host
        if self.use_proxy:
            if not auth_path:
                auth_path = path
            path = self.prefix_proxy_to_path(path, host)
            if self.proxy_user and self.proxy_pass and not self.is_secure:
                headers.update(self.get_proxy_auth_header())
        return HTTPRequest(method, self.protocol, host, self.port, path, auth_path, params, headers, data)

    def make_request(self, method, path, headers=None, data='', host=None, auth_path=None, sender=None, override_num_retries=None, params=None, retry_handler=None):
        """Makes a request to the server, with stock multiple-retry logic."""
        if params is None:
            params = {}
        http_request = self.build_base_http_request(method, path, auth_path, params, headers, data, host)
        return self._mexe(http_request, sender, override_num_retries, retry_handler=retry_handler)

    def close(self):
        """(Optional) Close any open HTTP connections.  This is non-destructive,
        and making a new request will open a connection again."""
        boto.log.debug('closing all HTTP connections')
        self._connection = None


class AWSQueryConnection(AWSAuthConnection):
    APIVersion = ''
    ResponseError = BotoServerError

    def __init__(self, aws_access_key_id=None, aws_secret_access_key=None, is_secure=True, port=None, proxy=None, proxy_port=None, proxy_user=None, proxy_pass=None, host=None, debug=0, https_connection_factory=None, path='/', security_token=None, validate_certs=True, profile_name=None, provider='aws'):
        super(AWSQueryConnection, self).__init__(host, aws_access_key_id, aws_secret_access_key, is_secure, port, proxy, proxy_port, proxy_user, proxy_pass, debug, https_connection_factory, path, security_token=security_token, validate_certs=validate_certs, profile_name=profile_name, provider=provider)

    def _required_auth_capability(self):
        return []

    def get_utf8_value(self, value):
        return boto.utils.get_utf8_value(value)

    def make_request(self, action, params=None, path='/', verb='GET'):
        http_request = self.build_base_http_request(verb, path, None, params, {}, '', self.host)
        if action:
            http_request.params['Action'] = action
        if self.APIVersion:
            http_request.params['Version'] = self.APIVersion
        return self._mexe(http_request)

    def build_list_params(self, params, items, label):
        if isinstance(items, six.string_types):
            items = [
             items]
        for i in range(1, len(items) + 1):
            params['%s.%d' % (label, i)] = items[(i - 1)]

    def build_complex_list_params(self, params, items, label, names):
        """Serialize a list of structures.

        For example::

            items = [('foo', 'bar', 'baz'), ('foo2', 'bar2', 'baz2')]
            label = 'ParamName.member'
            names = ('One', 'Two', 'Three')
            self.build_complex_list_params(params, items, label, names)

        would result in the params dict being updated with these params::

            ParamName.member.1.One = foo
            ParamName.member.1.Two = bar
            ParamName.member.1.Three = baz

            ParamName.member.2.One = foo2
            ParamName.member.2.Two = bar2
            ParamName.member.2.Three = baz2

        :type params: dict
        :param params: The params dict.  The complex list params
            will be added to this dict.

        :type items: list of tuples
        :param items: The list to serialize.

        :type label: string
        :param label: The prefix to apply to the parameter.

        :type names: tuple of strings
        :param names: The names associated with each tuple element.

        """
        for i, item in enumerate(items, 1):
            current_prefix = '%s.%s' % (label, i)
            for key, value in zip(names, item):
                full_key = '%s.%s' % (current_prefix, key)
                params[full_key] = value

    def get_list(self, action, params, markers, path='/', parent=None, verb='GET'):
        if not parent:
            parent = self
        response = self.make_request(action, params, path, verb)
        body = response.read()
        boto.log.debug(body)
        if not body:
            boto.log.error('Null body %s' % body)
            raise self.ResponseError(response.status, response.reason, body)
        else:
            if response.status == 200:
                rs = ResultSet(markers)
                h = boto.handler.XmlHandler(rs, parent)
                if isinstance(body, six.text_type):
                    body = body.encode('utf-8')
                xml.sax.parseString(body, h)
                return rs
            boto.log.error('%s %s' % (response.status, response.reason))
            boto.log.error('%s' % body)
            raise self.ResponseError(response.status, response.reason, body)

    def get_object(self, action, params, cls, path='/', parent=None, verb='GET'):
        if not parent:
            parent = self
        response = self.make_request(action, params, path, verb)
        body = response.read()
        boto.log.debug(body)
        if not body:
            boto.log.error('Null body %s' % body)
            raise self.ResponseError(response.status, response.reason, body)
        else:
            if response.status == 200:
                obj = cls(parent)
                h = boto.handler.XmlHandler(obj, parent)
                if isinstance(body, six.text_type):
                    body = body.encode('utf-8')
                xml.sax.parseString(body, h)
                return obj
            boto.log.error('%s %s' % (response.status, response.reason))
            boto.log.error('%s' % body)
            raise self.ResponseError(response.status, response.reason, body)

    def get_status(self, action, params, path='/', parent=None, verb='GET'):
        if not parent:
            parent = self
        response = self.make_request(action, params, path, verb)
        body = response.read()
        boto.log.debug(body)
        if not body:
            boto.log.error('Null body %s' % body)
            raise self.ResponseError(response.status, response.reason, body)
        else:
            if response.status == 200:
                rs = ResultSet()
                h = boto.handler.XmlHandler(rs, parent)
                xml.sax.parseString(body, h)
                return rs.status
            boto.log.error('%s %s' % (response.status, response.reason))
            boto.log.error('%s' % body)
            raise self.ResponseError(response.status, response.reason, body)