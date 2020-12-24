# uncompyle6 version 3.6.7
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: ./vendor/requests/adapters.py
# Compiled at: 2019-11-10 08:27:46
# Size of source mod 2**32: 21344 bytes
__doc__ = '\nrequests.adapters\n~~~~~~~~~~~~~~~~~\n\nThis module contains the transport adapters that Requests uses to define\nand maintain connections.\n'
import os.path, socket
from urllib3.poolmanager import PoolManager, proxy_from_url
from urllib3.response import HTTPResponse
from urllib3.util import parse_url
import urllib3.util as TimeoutSauce
from urllib3.util.retry import Retry
from urllib3.exceptions import ClosedPoolError
from urllib3.exceptions import ConnectTimeoutError
import urllib3.exceptions as _HTTPError
from urllib3.exceptions import MaxRetryError
from urllib3.exceptions import NewConnectionError
import urllib3.exceptions as _ProxyError
from urllib3.exceptions import ProtocolError
from urllib3.exceptions import ReadTimeoutError
import urllib3.exceptions as _SSLError
from urllib3.exceptions import ResponseError
from urllib3.exceptions import LocationValueError
from .models import Response
from .compat import urlparse, basestring
from .utils import DEFAULT_CA_BUNDLE_PATH, extract_zipped_paths, get_encoding_from_headers, prepend_scheme_if_needed, get_auth_from_url, urldefragauth, select_proxy
from .structures import CaseInsensitiveDict
from .cookies import extract_cookies_to_jar
from .exceptions import ConnectionError, ConnectTimeout, ReadTimeout, SSLError, ProxyError, RetryError, InvalidSchema, InvalidProxyURL, InvalidURL
from .auth import _basic_auth_str
try:
    from urllib3.contrib.socks import SOCKSProxyManager
except ImportError:

    def SOCKSProxyManager(*args, **kwargs):
        raise InvalidSchema('Missing dependencies for SOCKS support.')


else:
    DEFAULT_POOLBLOCK = False
    DEFAULT_POOLSIZE = 10
    DEFAULT_RETRIES = 0
    DEFAULT_POOL_TIMEOUT = None

    class BaseAdapter(object):
        """BaseAdapter"""

        def __init__(self):
            super(BaseAdapter, self).__init__()

        def send(self, request, stream=False, timeout=None, verify=True, cert=None, proxies=None):
            """Sends PreparedRequest object. Returns Response object.

        :param request: The :class:`PreparedRequest <PreparedRequest>` being sent.
        :param stream: (optional) Whether to stream the request content.
        :param timeout: (optional) How long to wait for the server to send
            data before giving up, as a float, or a :ref:`(connect timeout,
            read timeout) <timeouts>` tuple.
        :type timeout: float or tuple
        :param verify: (optional) Either a boolean, in which case it controls whether we verify
            the server's TLS certificate, or a string, in which case it must be a path
            to a CA bundle to use
        :param cert: (optional) Any user-provided SSL certificate to be trusted.
        :param proxies: (optional) The proxies dictionary to apply to the request.
        """
            raise NotImplementedError

        def close(self):
            """Cleans up adapter specific items."""
            raise NotImplementedError


    class HTTPAdapter(BaseAdapter):
        """HTTPAdapter"""
        __attrs__ = [
         'max_retries', 'config', '_pool_connections', '_pool_maxsize',
         '_pool_block']

        def __init__(self, pool_connections=DEFAULT_POOLSIZE, pool_maxsize=DEFAULT_POOLSIZE, max_retries=DEFAULT_RETRIES, pool_block=DEFAULT_POOLBLOCK):
            if max_retries == DEFAULT_RETRIES:
                self.max_retries = Retry(0, read=False)
            else:
                self.max_retries = Retry.from_int(max_retries)
            self.config = {}
            self.proxy_manager = {}
            super(HTTPAdapter, self).__init__()
            self._pool_connections = pool_connections
            self._pool_maxsize = pool_maxsize
            self._pool_block = pool_block
            self.init_poolmanager(pool_connections, pool_maxsize, block=pool_block)

        def __getstate__--- This code section failed: ---

 L. 132         0  LOAD_CLOSURE             'self'
                2  BUILD_TUPLE_1         1 
                4  LOAD_DICTCOMP            '<code_object <dictcomp>>'
                6  LOAD_STR                 'HTTPAdapter.__getstate__.<locals>.<dictcomp>'
                8  MAKE_FUNCTION_8          'closure'
               10  LOAD_DEREF               'self'
               12  LOAD_ATTR                __attrs__
               14  GET_ITER         
               16  CALL_FUNCTION_1       1  ''
               18  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1

        def __setstate__(self, state):
            self.proxy_manager = {}
            self.config = {}
            for attr, value in state.items():
                setattr(self, attr, value)

            self.init_poolmanager((self._pool_connections), (self._pool_maxsize), block=(self._pool_block))

        def init_poolmanager(self, connections, maxsize, block=DEFAULT_POOLBLOCK, **pool_kwargs):
            """Initializes a urllib3 PoolManager.

        This method should not be called from user code, and is only
        exposed for use when subclassing the
        :class:`HTTPAdapter <requests.adapters.HTTPAdapter>`.

        :param connections: The number of urllib3 connection pools to cache.
        :param maxsize: The maximum number of connections to save in the pool.
        :param block: Block when no free connections are available.
        :param pool_kwargs: Extra keyword arguments used to initialize the Pool Manager.
        """
            self._pool_connections = connections
            self._pool_maxsize = maxsize
            self._pool_block = block
            self.poolmanager = PoolManager(num_pools=connections, maxsize=maxsize, block=block, 
             strict=True, **pool_kwargs)

        def proxy_manager_for(self, proxy, **proxy_kwargs):
            """Return urllib3 ProxyManager for the given proxy.

        This method should not be called from user code, and is only
        exposed for use when subclassing the
        :class:`HTTPAdapter <requests.adapters.HTTPAdapter>`.

        :param proxy: The proxy to return a urllib3 ProxyManager for.
        :param proxy_kwargs: Extra keyword arguments used to configure the Proxy Manager.
        :returns: ProxyManager
        :rtype: urllib3.ProxyManager
        """
            if proxy in self.proxy_manager:
                manager = self.proxy_manager[proxy]
            elif proxy.lower().startswith('socks'):
                username, password = get_auth_from_url(proxy)
                manager = self.proxy_manager[proxy] = SOCKSProxyManager(
 proxy, username=username, 
                 password=password, 
                 num_pools=self._pool_connections, 
                 maxsize=self._pool_maxsize, 
                 block=self._pool_block, **proxy_kwargs)
            else:
                proxy_headers = self.proxy_headers(proxy)
                manager = self.proxy_manager[proxy] = proxy_from_url(
 proxy, proxy_headers=proxy_headers, 
                 num_pools=self._pool_connections, 
                 maxsize=self._pool_maxsize, 
                 block=self._pool_block, **proxy_kwargs)
            return manager

        def cert_verify(self, conn, url, verify, cert):
            """Verify a SSL certificate. This method should not be called from user
        code, and is only exposed for use when subclassing the
        :class:`HTTPAdapter <requests.adapters.HTTPAdapter>`.

        :param conn: The urllib3 connection object associated with the cert.
        :param url: The requested URL.
        :param verify: Either a boolean, in which case it controls whether we verify
            the server's TLS certificate, or a string, in which case it must be a path
            to a CA bundle to use
        :param cert: The SSL certificate to verify.
        """
            if url.lower().startswith('https'):
                if verify:
                    cert_loc = None
                    if verify is not True:
                        cert_loc = verify
                    else:
                        if not cert_loc:
                            cert_loc = extract_zipped_paths(DEFAULT_CA_BUNDLE_PATH)
                        raise cert_loc and os.path.exists(cert_loc) or 
                    conn.cert_reqs = 'CERT_REQUIRED'
                    if not os.path.isdir(cert_loc):
                        conn.ca_certs = cert_loc
                else:
                    conn.ca_cert_dir = cert_loc
            else:
                conn.cert_reqs = 'CERT_NONE'
                conn.ca_certs = None
                conn.ca_cert_dir = None
            if cert:
                if not isinstance(cert, basestring):
                    conn.cert_file = cert[0]
                    conn.key_file = cert[1]
                else:
                    conn.cert_file = cert
                    conn.key_file = None
                if conn.cert_file:
                    if not os.path.exists(conn.cert_file):
                        raise IOError('Could not find the TLS certificate file, invalid path: {}'.format(conn.cert_file))
                if conn.key_file:
                    if not os.path.exists(conn.key_file):
                        raise IOError('Could not find the TLS key file, invalid path: {}'.format(conn.key_file))

        def build_response(self, req, resp):
            """Builds a :class:`Response <requests.Response>` object from a urllib3
        response. This should not be called from user code, and is only exposed
        for use when subclassing the
        :class:`HTTPAdapter <requests.adapters.HTTPAdapter>`

        :param req: The :class:`PreparedRequest <PreparedRequest>` used to generate the response.
        :param resp: The urllib3 response object.
        :rtype: requests.Response
        """
            response = Response()
            response.status_code = getattr(resp, 'status', None)
            response.headers = CaseInsensitiveDict(getattr(resp, 'headers', {}))
            response.encoding = get_encoding_from_headers(response.headers)
            response.raw = resp
            response.reason = response.raw.reason
            if isinstance(req.url, bytes):
                response.url = req.url.decode('utf-8')
            else:
                response.url = req.url
            extract_cookies_to_jar(response.cookies, req, resp)
            response.request = req
            response.connection = self
            return response

        def get_connection(self, url, proxies=None):
            """Returns a urllib3 connection for the given URL. This should not be
        called from user code, and is only exposed for use when subclassing the
        :class:`HTTPAdapter <requests.adapters.HTTPAdapter>`.

        :param url: The URL to connect to.
        :param proxies: (optional) A Requests-style dictionary of proxies used on this request.
        :rtype: urllib3.ConnectionPool
        """
            proxy = select_proxy(url, proxies)
            if proxy:
                proxy = prepend_scheme_if_needed(proxy, 'http')
                proxy_url = parse_url(proxy)
                if not proxy_url.host:
                    raise InvalidProxyURL('Please check proxy URL. It is malformed and could be missing the host.')
                proxy_manager = self.proxy_manager_for(proxy)
                conn = proxy_manager.connection_from_url(url)
            else:
                parsed = urlparse(url)
                url = parsed.geturl()
                conn = self.poolmanager.connection_from_url(url)
            return conn

        def close(self):
            """Disposes of any internal state.

        Currently, this closes the PoolManager and any active ProxyManager,
        which closes any pooled connections.
        """
            self.poolmanager.clear()
            for proxy in self.proxy_manager.values():
                proxy.clear()

        def request_url(self, request, proxies):
            """Obtain the url to use when making the final request.

        If the message is being sent through a HTTP proxy, the full URL has to
        be used. Otherwise, we should only use the path portion of the URL.

        This should not be called from user code, and is only exposed for use
        when subclassing the
        :class:`HTTPAdapter <requests.adapters.HTTPAdapter>`.

        :param request: The :class:`PreparedRequest <PreparedRequest>` being sent.
        :param proxies: A dictionary of schemes or schemes and hosts to proxy URLs.
        :rtype: str
        """
            proxy = select_proxy(request.url, proxies)
            scheme = urlparse(request.url).scheme
            is_proxied_http_request = proxy and scheme != 'https'
            using_socks_proxy = False
            if proxy:
                proxy_scheme = urlparse(proxy).scheme.lower()
                using_socks_proxy = proxy_scheme.startswith('socks')
            url = request.path_url
            if is_proxied_http_request:
                if not using_socks_proxy:
                    url = urldefragauth(request.url)
            return url

        def add_headers(self, request, **kwargs):
            """Add any headers needed by the connection. As of v2.0 this does
        nothing by default, but is left for overriding by users that subclass
        the :class:`HTTPAdapter <requests.adapters.HTTPAdapter>`.

        This should not be called from user code, and is only exposed for use
        when subclassing the
        :class:`HTTPAdapter <requests.adapters.HTTPAdapter>`.

        :param request: The :class:`PreparedRequest <PreparedRequest>` to add headers to.
        :param kwargs: The keyword arguments from the call to send().
        """
            pass

        def proxy_headers(self, proxy):
            """Returns a dictionary of the headers to add to any request sent
        through a proxy. This works with urllib3 magic to ensure that they are
        correctly sent to the proxy, rather than in a tunnelled request if
        CONNECT is being used.

        This should not be called from user code, and is only exposed for use
        when subclassing the
        :class:`HTTPAdapter <requests.adapters.HTTPAdapter>`.

        :param proxy: The url of the proxy being used for this request.
        :rtype: dict
        """
            headers = {}
            username, password = get_auth_from_url(proxy)
            if username:
                headers['Proxy-Authorization'] = _basic_auth_str(username, password)
            return headers

        def send(self, request, stream=False, timeout=None, verify=True, cert=None, proxies=None):
            """Sends PreparedRequest object. Returns Response object.

        :param request: The :class:`PreparedRequest <PreparedRequest>` being sent.
        :param stream: (optional) Whether to stream the request content.
        :param timeout: (optional) How long to wait for the server to send
            data before giving up, as a float, or a :ref:`(connect timeout,
            read timeout) <timeouts>` tuple.
        :type timeout: float or tuple or urllib3 Timeout object
        :param verify: (optional) Either a boolean, in which case it controls whether
            we verify the server's TLS certificate, or a string, in which case it
            must be a path to a CA bundle to use
        :param cert: (optional) Any user-provided SSL certificate to be trusted.
        :param proxies: (optional) The proxies dictionary to apply to the request.
        :rtype: requests.Response
        """
            try:
                conn = self.get_connection(request.url, proxies)
            except LocationValueError as e:
                try:
                    raise InvalidURL(e, request=request)
                finally:
                    e = None
                    del e

            else:
                self.cert_verify(conn, request.url, verify, cert)
                url = self.request_url(request, proxies)
                self.add_headers(request, stream=stream, timeout=timeout, verify=verify, cert=cert, proxies=proxies)
                chunked = not (request.body is None or )
                if isinstance(timeout, tuple):
                    try:
                        connect, read = timeout
                        timeout = TimeoutSauce(connect=connect, read=read)
                    except ValueError as e:
                        try:
                            err = 'Invalid timeout {}. Pass a (connect, read) timeout tuple, or a single float to set both timeouts to the same value'.format(timeout)
                            raise ValueError(err)
                        finally:
                            e = None
                            del e

                elif isinstance(timeout, TimeoutSauce):
                    pass
                else:
                    timeout = TimeoutSauce(connect=timeout, read=timeout)
                try:
                    if not chunked:
                        resp = conn.urlopen(method=(request.method),
                          url=url,
                          body=(request.body),
                          headers=(request.headers),
                          redirect=False,
                          assert_same_host=False,
                          preload_content=False,
                          decode_content=False,
                          retries=(self.max_retries),
                          timeout=timeout)
                    else:
                        if hasattr(conn, 'proxy_pool'):
                            conn = conn.proxy_pool
                        low_conn = conn._get_conn(timeout=DEFAULT_POOL_TIMEOUT)
                    try:
                        low_conn.putrequest((request.method), url,
                          skip_accept_encoding=True)
                        for header, value in request.headers.items():
                            low_conn.putheader(header, value)

                        low_conn.endheaders()
                        for i in request.body:
                            low_conn.send(hex(len(i))[2:].encode('utf-8'))
                            low_conn.send(b'\r\n')
                            low_conn.send(i)
                            low_conn.send(b'\r\n')

                        low_conn.send(b'0\r\n\r\n')
                        try:
                            r = low_conn.getresponse(buffering=True)
                        except TypeError:
                            r = low_conn.getresponse()
                        else:
                            resp = HTTPResponse.from_httplib(r,
                              pool=conn,
                              connection=low_conn,
                              preload_content=False,
                              decode_content=False)
                    except:
                        low_conn.close()
                        raise

                except (ProtocolError, socket.error) as err:
                    try:
                        raise ConnectionError(err, request=request)
                    finally:
                        err = None
                        del err

                except MaxRetryError as e:
                    try:
                        if isinstance(e.reason, ConnectTimeoutError):
                            if not isinstance(e.reason, NewConnectionError):
                                raise ConnectTimeout(e, request=request)
                        if isinstance(e.reason, ResponseError):
                            raise RetryError(e, request=request)
                        if isinstance(e.reason, _ProxyError):
                            raise ProxyError(e, request=request)
                        if isinstance(e.reason, _SSLError):
                            raise SSLError(e, request=request)
                        raise ConnectionError(e, request=request)
                    finally:
                        e = None
                        del e

                except ClosedPoolError as e:
                    try:
                        raise ConnectionError(e, request=request)
                    finally:
                        e = None
                        del e

                except _ProxyError as e:
                    try:
                        raise ProxyError(e)
                    finally:
                        e = None
                        del e

                except (_SSLError, _HTTPError) as e:
                    try:
                        if isinstance(e, _SSLError):
                            raise SSLError(e, request=request)
                        elif isinstance(e, ReadTimeoutError):
                            raise ReadTimeout(e, request=request)
                        else:
                            raise
                    finally:
                        e = None
                        del e

                else:
                    return self.build_response(request, resp)