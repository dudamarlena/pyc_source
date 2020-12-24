# uncompyle6 version 3.6.7
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: ./vendor/urllib3/connectionpool.py
# Compiled at: 2019-11-10 08:27:46
# Size of source mod 2**32: 36446 bytes
from __future__ import absolute_import
import errno, logging, sys, warnings
from socket import error as SocketError, timeout as SocketTimeout
import socket
from .exceptions import ClosedPoolError, ProtocolError, EmptyPoolError, HeaderParsingError, HostChangedError, LocationValueError, MaxRetryError, ProxyError, ReadTimeoutError, SSLError, TimeoutError, InsecureRequestWarning, NewConnectionError
from packages.ssl_match_hostname import CertificateError
from .packages import six
from packages.six.moves import queue
from .connection import port_by_scheme, DummyConnection, HTTPConnection, HTTPSConnection, VerifiedHTTPSConnection, HTTPException, BaseSSLError
from .request import RequestMethods
from .response import HTTPResponse
from util.connection import is_connection_dropped
from util.request import set_file_position
from util.response import assert_header_parsing
from util.retry import Retry
from util.timeout import Timeout
from util.url import get_host, parse_url, Url, _normalize_host as normalize_host, _encode_target
from util.queue import LifoQueue
xrange = six.moves.xrange
log = logging.getLogger(__name__)
_Default = object()

class ConnectionPool(object):
    """ConnectionPool"""
    scheme = None
    QueueCls = LifoQueue

    def __init__(self, host, port=None):
        if not host:
            raise LocationValueError('No host specified.')
        self.host = _normalize_host(host, scheme=(self.scheme))
        self._proxy_host = host.lower()
        self.port = port

    def __str__(self):
        return '%s(host=%r, port=%r)' % (type(self).__name__, self.host, self.port)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
        return False

    def close(self):
        """
        Close all pooled connections and disable the pool.
        """
        pass


_blocking_errnos = {
 errno.EAGAIN, errno.EWOULDBLOCK}

class HTTPConnectionPool(ConnectionPool, RequestMethods):
    """HTTPConnectionPool"""
    scheme = 'http'
    ConnectionCls = HTTPConnection
    ResponseCls = HTTPResponse

    def __init__(self, host, port=None, strict=False, timeout=Timeout.DEFAULT_TIMEOUT, maxsize=1, block=False, headers=None, retries=None, _proxy=None, _proxy_headers=None, **conn_kw):
        ConnectionPool.__init__(self, host, port)
        RequestMethods.__init__(self, headers)
        self.strict = strict
        if not isinstance(timeout, Timeout):
            timeout = Timeout.from_float(timeout)
        if retries is None:
            retries = Retry.DEFAULT
        self.timeout = timeout
        self.retries = retries
        self.pool = self.QueueCls(maxsize)
        self.block = block
        self.proxy = _proxy
        self.proxy_headers = _proxy_headers or 
        for _ in xrange(maxsize):
            self.pool.put(None)

        self.num_connections = 0
        self.num_requests = 0
        self.conn_kw = conn_kw
        if self.proxy:
            self.conn_kw.setdefault('socket_options', [])

    def _new_conn(self):
        """
        Return a fresh :class:`HTTPConnection`.
        """
        self.num_connections += 1
        log.debug('Starting new HTTP connection (%d): %s:%s', self.num_connections, self.host, self.port or )
        conn = (self.ConnectionCls)(host=self.host, 
         port=self.port, 
         timeout=self.timeout.connect_timeout, 
         strict=self.strict, **self.conn_kw)
        return conn

    def _get_conn(self, timeout=None):
        """
        Get a connection. Will return a pooled connection if one is available.

        If no connections are available and :prop:`.block` is ``False``, then a
        fresh connection is returned.

        :param timeout:
            Seconds to wait before giving up and raising
            :class:`urllib3.exceptions.EmptyPoolError` if the pool is empty and
            :prop:`.block` is ``True``.
        """
        conn = None
        try:
            conn = self.pool.get(block=(self.block), timeout=timeout)
        except AttributeError:
            raise ClosedPoolError(self, 'Pool is closed.')
        except queue.Empty:
            if self.block:
                raise EmptyPoolError(self, 'Pool reached maximum size and no more connections are allowed.')
        else:
            if conn:
                if is_connection_dropped(conn):
                    log.debug('Resetting dropped connection: %s', self.host)
                    conn.close()
                    if getattr(conn, 'auto_open', 1) == 0:
                        conn = None
            return conn or 

    def _put_conn--- This code section failed: ---

 L. 290         0  SETUP_FINALLY        24  'to 24'

 L. 291         2  LOAD_FAST                'self'
                4  LOAD_ATTR                pool
                6  LOAD_ATTR                put
                8  LOAD_FAST                'conn'
               10  LOAD_CONST               False
               12  LOAD_CONST               ('block',)
               14  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               16  POP_TOP          

 L. 292        18  POP_BLOCK        
               20  LOAD_CONST               None
               22  RETURN_VALUE     
             24_0  COME_FROM_FINALLY     0  '0'

 L. 293        24  DUP_TOP          
               26  LOAD_GLOBAL              AttributeError
               28  COMPARE_OP               exception-match
               30  POP_JUMP_IF_FALSE    42  'to 42'
               32  POP_TOP          
               34  POP_TOP          
               36  POP_TOP          

 L. 295        38  POP_EXCEPT       
               40  JUMP_FORWARD         78  'to 78'
             42_0  COME_FROM            30  '30'

 L. 296        42  DUP_TOP          
               44  LOAD_GLOBAL              queue
               46  LOAD_ATTR                Full
               48  COMPARE_OP               exception-match
               50  POP_JUMP_IF_FALSE    76  'to 76'
               52  POP_TOP          
               54  POP_TOP          
               56  POP_TOP          

 L. 298        58  LOAD_GLOBAL              log
               60  LOAD_METHOD              warning
               62  LOAD_STR                 'Connection pool is full, discarding connection: %s'
               64  LOAD_FAST                'self'
               66  LOAD_ATTR                host
               68  CALL_METHOD_2         2  ''
               70  POP_TOP          
               72  POP_EXCEPT       
               74  JUMP_FORWARD         78  'to 78'
             76_0  COME_FROM            50  '50'
               76  END_FINALLY      
             78_0  COME_FROM            74  '74'
             78_1  COME_FROM            40  '40'

 L. 301        78  LOAD_FAST                'conn'
               80  POP_JUMP_IF_FALSE    90  'to 90'

 L. 302        82  LOAD_FAST                'conn'
               84  LOAD_METHOD              close
               86  CALL_METHOD_0         0  ''
               88  POP_TOP          
             90_0  COME_FROM            80  '80'

Parse error at or near `RETURN_VALUE' instruction at offset 22

    def _validate_conn(self, conn):
        """
        Called right before a request is made, after the socket is created.
        """
        pass

    def _prepare_proxy(self, conn):
        pass

    def _get_timeout(self, timeout):
        """ Helper that always returns a :class:`urllib3.util.Timeout` """
        if timeout is _Default:
            return self.timeout.clone()
        if isinstance(timeout, Timeout):
            return timeout.clone()
        return Timeout.from_float(timeout)

    def _raise_timeout(self, err, url, timeout_value):
        """Is the error actually a timeout? Will raise a ReadTimeout or pass"""
        if isinstance(err, SocketTimeout):
            raise ReadTimeoutError(self, url, 'Read timed out. (read timeout=%s)' % timeout_value)
        if hasattr(err, 'errno'):
            if err.errno in _blocking_errnos:
                raise ReadTimeoutError(self, url, 'Read timed out. (read timeout=%s)' % timeout_value)
        if 'timed out' in str(err) or 'did not complete (read)' in str(err):
            raise ReadTimeoutError(self, url, 'Read timed out. (read timeout=%s)' % timeout_value)

    def _make_request(self, conn, method, url, timeout=_Default, chunked=False, **httplib_request_kw):
        """
        Perform a request on a given urllib connection object taken from our
        pool.

        :param conn:
            a connection from one of our connection pools

        :param timeout:
            Socket timeout in seconds for the request. This can be a
            float or integer, which will set the same timeout value for
            the socket connect and the socket read, or an instance of
            :class:`urllib3.util.Timeout`, which gives you more fine-grained
            control over your timeouts.
        """
        self.num_requests += 1
        timeout_obj = self._get_timeout(timeout)
        timeout_obj.start_connect()
        conn.timeout = timeout_obj.connect_timeout
        try:
            self._validate_conn(conn)
        except (SocketTimeout, BaseSSLError) as e:
            try:
                self._raise_timeout(err=e, url=url, timeout_value=(conn.timeout))
                raise
            finally:
                e = None
                del e

        else:
            if chunked:
                (conn.request_chunked)(method, url, **httplib_request_kw)
            else:
                (conn.request)(method, url, **httplib_request_kw)
            read_timeout = timeout_obj.read_timeout
            if getattr(conn, 'sock', None):
                if read_timeout == 0:
                    raise ReadTimeoutError(self, url, 'Read timed out. (read timeout=%s)' % read_timeout)
                elif read_timeout is Timeout.DEFAULT_TIMEOUT:
                    conn.sock.settimeout(socket.getdefaulttimeout())
                else:
                    conn.sock.settimeout(read_timeout)
        try:
            try:
                httplib_response = conn.getresponse(buffering=True)
            except TypeError:
                try:
                    httplib_response = conn.getresponse()
                except BaseException as e:
                    try:
                        six.raise_from(e, None)
                    finally:
                        e = None
                        del e

        except (SocketTimeout, BaseSSLError, SocketError) as e:
            try:
                self._raise_timeout(err=e, url=url, timeout_value=read_timeout)
                raise
            finally:
                e = None
                del e

        else:
            http_version = getattr(conn, '_http_vsn_str', 'HTTP/?')
            log.debug('%s://%s:%s "%s %s %s" %s %s', self.scheme, self.host, self.port, method, url, http_version, httplib_response.status, httplib_response.length)
            try:
                assert_header_parsing(httplib_response.msg)
            except (HeaderParsingError, TypeError) as hpe:
                try:
                    log.warning('Failed to parse headers (url=%s): %s',
                      (self._absolute_url(url)),
                      hpe,
                      exc_info=True)
                finally:
                    hpe = None
                    del hpe

            else:
                return httplib_response

    def _absolute_url(self, path):
        return Url(scheme=(self.scheme), host=(self.host), port=(self.port), path=path).url

    def close(self):
        """
        Close all pooled connections and disable the pool.
        """
        if self.pool is None:
            return
        old_pool, self.pool = self.pool, None
        try:
            while True:
                conn = old_pool.get(block=False)
                if conn:
                    conn.close()

        except queue.Empty:
            pass

    def is_same_host(self, url):
        """
        Check if the given ``url`` is a member of the same host as this
        connection pool.
        """
        if url.startswith('/'):
            return True
        scheme, host, port = get_host(url)
        if host is not None:
            host = _normalize_host(host, scheme=scheme)
        if self.port:
            port = port or port_by_scheme.get(scheme)
        elif not self.port:
            if port == port_by_scheme.get(scheme):
                port = None
        return (scheme, host, port) == (self.scheme, self.host, self.port)

    def urlopen--- This code section failed: ---

 L. 600         0  LOAD_FAST                'headers'
                2  LOAD_CONST               None
                4  COMPARE_OP               is
                6  POP_JUMP_IF_FALSE    14  'to 14'

 L. 601         8  LOAD_FAST                'self'
               10  LOAD_ATTR                headers
               12  STORE_FAST               'headers'
             14_0  COME_FROM             6  '6'

 L. 603        14  LOAD_GLOBAL              isinstance
               16  LOAD_FAST                'retries'
               18  LOAD_GLOBAL              Retry
               20  CALL_FUNCTION_2       2  ''
               22  POP_JUMP_IF_TRUE     42  'to 42'

 L. 604        24  LOAD_GLOBAL              Retry
               26  LOAD_ATTR                from_int
               28  LOAD_FAST                'retries'
               30  LOAD_FAST                'redirect'
               32  LOAD_FAST                'self'
               34  LOAD_ATTR                retries
               36  LOAD_CONST               ('redirect', 'default')
               38  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
               40  STORE_FAST               'retries'
             42_0  COME_FROM            22  '22'

 L. 606        42  LOAD_FAST                'release_conn'
               44  LOAD_CONST               None
               46  COMPARE_OP               is
               48  POP_JUMP_IF_FALSE    62  'to 62'

 L. 607        50  LOAD_FAST                'response_kw'
               52  LOAD_METHOD              get
               54  LOAD_STR                 'preload_content'
               56  LOAD_CONST               True
               58  CALL_METHOD_2         2  ''
               60  STORE_FAST               'release_conn'
             62_0  COME_FROM            48  '48'

 L. 610        62  LOAD_FAST                'assert_same_host'
               64  POP_JUMP_IF_FALSE    88  'to 88'
               66  LOAD_FAST                'self'
               68  LOAD_METHOD              is_same_host
               70  LOAD_FAST                'url'
               72  CALL_METHOD_1         1  ''
               74  POP_JUMP_IF_TRUE     88  'to 88'

 L. 611        76  LOAD_GLOBAL              HostChangedError
               78  LOAD_FAST                'self'
               80  LOAD_FAST                'url'
               82  LOAD_FAST                'retries'
               84  CALL_FUNCTION_3       3  ''
               86  RAISE_VARARGS_1       1  ''
             88_0  COME_FROM            74  '74'
             88_1  COME_FROM            64  '64'

 L. 614        88  LOAD_FAST                'url'
               90  LOAD_METHOD              startswith
               92  LOAD_STR                 '/'
               94  CALL_METHOD_1         1  ''
               96  POP_JUMP_IF_FALSE   114  'to 114'

 L. 615        98  LOAD_GLOBAL              six
              100  LOAD_METHOD              ensure_str
              102  LOAD_GLOBAL              _encode_target
              104  LOAD_FAST                'url'
              106  CALL_FUNCTION_1       1  ''
              108  CALL_METHOD_1         1  ''
              110  STORE_FAST               'url'
              112  JUMP_FORWARD        130  'to 130'
            114_0  COME_FROM            96  '96'

 L. 617       114  LOAD_GLOBAL              six
              116  LOAD_METHOD              ensure_str
              118  LOAD_GLOBAL              parse_url
              120  LOAD_FAST                'url'
              122  CALL_FUNCTION_1       1  ''
              124  LOAD_ATTR                url
              126  CALL_METHOD_1         1  ''
              128  STORE_FAST               'url'
            130_0  COME_FROM           112  '112'

 L. 619       130  LOAD_CONST               None
              132  STORE_FAST               'conn'

 L. 630       134  LOAD_FAST                'release_conn'
              136  STORE_FAST               'release_this_conn'

 L. 635       138  LOAD_FAST                'self'
              140  LOAD_ATTR                scheme
              142  LOAD_STR                 'http'
              144  COMPARE_OP               ==
              146  POP_JUMP_IF_FALSE   168  'to 168'

 L. 636       148  LOAD_FAST                'headers'
              150  LOAD_METHOD              copy
              152  CALL_METHOD_0         0  ''
              154  STORE_FAST               'headers'

 L. 637       156  LOAD_FAST                'headers'
              158  LOAD_METHOD              update
              160  LOAD_FAST                'self'
              162  LOAD_ATTR                proxy_headers
              164  CALL_METHOD_1         1  ''
              166  POP_TOP          
            168_0  COME_FROM           146  '146'

 L. 641       168  LOAD_CONST               None
              170  STORE_FAST               'err'

 L. 645       172  LOAD_CONST               False
              174  STORE_FAST               'clean_exit'

 L. 649       176  LOAD_GLOBAL              set_file_position
              178  LOAD_FAST                'body'
              180  LOAD_FAST                'body_pos'
              182  CALL_FUNCTION_2       2  ''
              184  STORE_FAST               'body_pos'

 L. 651   186_188  SETUP_FINALLY       562  'to 562'
              190  SETUP_FINALLY       344  'to 344'

 L. 653       192  LOAD_FAST                'self'
              194  LOAD_METHOD              _get_timeout
              196  LOAD_FAST                'timeout'
              198  CALL_METHOD_1         1  ''
              200  STORE_FAST               'timeout_obj'

 L. 654       202  LOAD_FAST                'self'
              204  LOAD_ATTR                _get_conn
              206  LOAD_FAST                'pool_timeout'
              208  LOAD_CONST               ('timeout',)
              210  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
              212  STORE_FAST               'conn'

 L. 656       214  LOAD_FAST                'timeout_obj'
              216  LOAD_ATTR                connect_timeout
              218  LOAD_FAST                'conn'
              220  STORE_ATTR               timeout

 L. 658       222  LOAD_FAST                'self'
              224  LOAD_ATTR                proxy
              226  LOAD_CONST               None
              228  COMPARE_OP               is-not
              230  JUMP_IF_FALSE_OR_POP   244  'to 244'
              232  LOAD_GLOBAL              getattr

 L. 659       234  LOAD_FAST                'conn'

 L. 659       236  LOAD_STR                 'sock'

 L. 659       238  LOAD_CONST               None

 L. 658       240  CALL_FUNCTION_3       3  ''
              242  UNARY_NOT        
            244_0  COME_FROM           230  '230'
              244  STORE_FAST               'is_new_proxy_conn'

 L. 661       246  LOAD_FAST                'is_new_proxy_conn'
          248_250  POP_JUMP_IF_FALSE   262  'to 262'

 L. 662       252  LOAD_FAST                'self'
              254  LOAD_METHOD              _prepare_proxy
              256  LOAD_FAST                'conn'
              258  CALL_METHOD_1         1  ''
              260  POP_TOP          
            262_0  COME_FROM           248  '248'

 L. 665       262  LOAD_FAST                'self'
              264  LOAD_ATTR                _make_request

 L. 666       266  LOAD_FAST                'conn'

 L. 667       268  LOAD_FAST                'method'

 L. 668       270  LOAD_FAST                'url'

 L. 669       272  LOAD_FAST                'timeout_obj'

 L. 670       274  LOAD_FAST                'body'

 L. 671       276  LOAD_FAST                'headers'

 L. 672       278  LOAD_FAST                'chunked'

 L. 665       280  LOAD_CONST               ('timeout', 'body', 'headers', 'chunked')
              282  CALL_FUNCTION_KW_7     7  '7 total positional and keyword args'
              284  STORE_FAST               'httplib_response'

 L. 679       286  LOAD_FAST                'release_conn'
          288_290  POP_JUMP_IF_TRUE    296  'to 296'
              292  LOAD_FAST                'conn'
              294  JUMP_FORWARD        298  'to 298'
            296_0  COME_FROM           288  '288'
              296  LOAD_CONST               None
            298_0  COME_FROM           294  '294'
              298  STORE_FAST               'response_conn'

 L. 682       300  LOAD_FAST                'method'
              302  LOAD_FAST                'response_kw'
              304  LOAD_STR                 'request_method'
              306  STORE_SUBSCR     

 L. 685       308  LOAD_FAST                'self'
              310  LOAD_ATTR                ResponseCls
              312  LOAD_ATTR                from_httplib

 L. 686       314  LOAD_FAST                'httplib_response'

 L. 685       316  BUILD_TUPLE_1         1 

 L. 687       318  LOAD_FAST                'self'

 L. 688       320  LOAD_FAST                'response_conn'

 L. 689       322  LOAD_FAST                'retries'

 L. 685       324  LOAD_CONST               ('pool', 'connection', 'retries')
              326  BUILD_CONST_KEY_MAP_3     3 

 L. 690       328  LOAD_FAST                'response_kw'

 L. 685       330  BUILD_MAP_UNPACK_WITH_CALL_2     2 
              332  CALL_FUNCTION_EX_KW     1  'keyword args'
              334  STORE_FAST               'response'

 L. 694       336  LOAD_CONST               True
              338  STORE_FAST               'clean_exit'
              340  POP_BLOCK        
              342  JUMP_FORWARD        558  'to 558'
            344_0  COME_FROM_FINALLY   190  '190'

 L. 696       344  DUP_TOP          
              346  LOAD_GLOBAL              queue
              348  LOAD_ATTR                Empty
              350  COMPARE_OP               exception-match
          352_354  POP_JUMP_IF_FALSE   376  'to 376'
              356  POP_TOP          
              358  POP_TOP          
              360  POP_TOP          

 L. 698       362  LOAD_GLOBAL              EmptyPoolError
              364  LOAD_FAST                'self'
              366  LOAD_STR                 'No pool connections are available.'
              368  CALL_FUNCTION_2       2  ''
              370  RAISE_VARARGS_1       1  ''
              372  POP_EXCEPT       
              374  JUMP_FORWARD        558  'to 558'
            376_0  COME_FROM           352  '352'

 L. 700       376  DUP_TOP          

 L. 701       378  LOAD_GLOBAL              TimeoutError

 L. 702       380  LOAD_GLOBAL              HTTPException

 L. 703       382  LOAD_GLOBAL              SocketError

 L. 704       384  LOAD_GLOBAL              ProtocolError

 L. 705       386  LOAD_GLOBAL              BaseSSLError

 L. 706       388  LOAD_GLOBAL              SSLError

 L. 707       390  LOAD_GLOBAL              CertificateError

 L. 700       392  BUILD_TUPLE_7         7 
              394  COMPARE_OP               exception-match
          396_398  POP_JUMP_IF_FALSE   556  'to 556'
              400  POP_TOP          
              402  STORE_FAST               'e'
              404  POP_TOP          
              406  SETUP_FINALLY       544  'to 544'

 L. 711       408  LOAD_CONST               False
              410  STORE_FAST               'clean_exit'

 L. 712       412  LOAD_GLOBAL              isinstance
              414  LOAD_FAST                'e'
              416  LOAD_GLOBAL              BaseSSLError
              418  LOAD_GLOBAL              CertificateError
              420  BUILD_TUPLE_2         2 
              422  CALL_FUNCTION_2       2  ''
          424_426  POP_JUMP_IF_FALSE   438  'to 438'

 L. 713       428  LOAD_GLOBAL              SSLError
              430  LOAD_FAST                'e'
              432  CALL_FUNCTION_1       1  ''
              434  STORE_FAST               'e'
              436  JUMP_FORWARD        500  'to 500'
            438_0  COME_FROM           424  '424'

 L. 714       438  LOAD_GLOBAL              isinstance
              440  LOAD_FAST                'e'
              442  LOAD_GLOBAL              SocketError
              444  LOAD_GLOBAL              NewConnectionError
              446  BUILD_TUPLE_2         2 
              448  CALL_FUNCTION_2       2  ''
          450_452  POP_JUMP_IF_FALSE   474  'to 474'
              454  LOAD_FAST                'self'
              456  LOAD_ATTR                proxy
          458_460  POP_JUMP_IF_FALSE   474  'to 474'

 L. 715       462  LOAD_GLOBAL              ProxyError
              464  LOAD_STR                 'Cannot connect to proxy.'
              466  LOAD_FAST                'e'
              468  CALL_FUNCTION_2       2  ''
              470  STORE_FAST               'e'
              472  JUMP_FORWARD        500  'to 500'
            474_0  COME_FROM           458  '458'
            474_1  COME_FROM           450  '450'

 L. 716       474  LOAD_GLOBAL              isinstance
              476  LOAD_FAST                'e'
              478  LOAD_GLOBAL              SocketError
              480  LOAD_GLOBAL              HTTPException
              482  BUILD_TUPLE_2         2 
              484  CALL_FUNCTION_2       2  ''
          486_488  POP_JUMP_IF_FALSE   500  'to 500'

 L. 717       490  LOAD_GLOBAL              ProtocolError
              492  LOAD_STR                 'Connection aborted.'
              494  LOAD_FAST                'e'
              496  CALL_FUNCTION_2       2  ''
              498  STORE_FAST               'e'
            500_0  COME_FROM           486  '486'
            500_1  COME_FROM           472  '472'
            500_2  COME_FROM           436  '436'

 L. 719       500  LOAD_FAST                'retries'
              502  LOAD_ATTR                increment

 L. 720       504  LOAD_FAST                'method'

 L. 720       506  LOAD_FAST                'url'

 L. 720       508  LOAD_FAST                'e'

 L. 720       510  LOAD_FAST                'self'

 L. 720       512  LOAD_GLOBAL              sys
              514  LOAD_METHOD              exc_info
              516  CALL_METHOD_0         0  ''
              518  LOAD_CONST               2
              520  BINARY_SUBSCR    

 L. 719       522  LOAD_CONST               ('error', '_pool', '_stacktrace')
              524  CALL_FUNCTION_KW_5     5  '5 total positional and keyword args'
              526  STORE_FAST               'retries'

 L. 722       528  LOAD_FAST                'retries'
              530  LOAD_METHOD              sleep
              532  CALL_METHOD_0         0  ''
              534  POP_TOP          

 L. 725       536  LOAD_FAST                'e'
              538  STORE_FAST               'err'
              540  POP_BLOCK        
              542  BEGIN_FINALLY    
            544_0  COME_FROM_FINALLY   406  '406'
              544  LOAD_CONST               None
              546  STORE_FAST               'e'
              548  DELETE_FAST              'e'
              550  END_FINALLY      
              552  POP_EXCEPT       
              554  JUMP_FORWARD        558  'to 558'
            556_0  COME_FROM           396  '396'
              556  END_FINALLY      
            558_0  COME_FROM           554  '554'
            558_1  COME_FROM           374  '374'
            558_2  COME_FROM           342  '342'
              558  POP_BLOCK        
              560  BEGIN_FINALLY    
            562_0  COME_FROM_FINALLY   186  '186'

 L. 728       562  LOAD_FAST                'clean_exit'
          564_566  POP_JUMP_IF_TRUE    586  'to 586'

 L. 733       568  LOAD_FAST                'conn'
          570_572  JUMP_IF_FALSE_OR_POP   580  'to 580'
              574  LOAD_FAST                'conn'
              576  LOAD_METHOD              close
              578  CALL_METHOD_0         0  ''
            580_0  COME_FROM           570  '570'
              580  STORE_FAST               'conn'

 L. 734       582  LOAD_CONST               True
              584  STORE_FAST               'release_this_conn'
            586_0  COME_FROM           564  '564'

 L. 736       586  LOAD_FAST                'release_this_conn'
          588_590  POP_JUMP_IF_FALSE   602  'to 602'

 L. 740       592  LOAD_FAST                'self'
              594  LOAD_METHOD              _put_conn
              596  LOAD_FAST                'conn'
              598  CALL_METHOD_1         1  ''
              600  POP_TOP          
            602_0  COME_FROM           588  '588'
              602  END_FINALLY      

 L. 742       604  LOAD_FAST                'conn'
          606_608  POP_JUMP_IF_TRUE    666  'to 666'

 L. 744       610  LOAD_GLOBAL              log
              612  LOAD_METHOD              warning

 L. 745       614  LOAD_STR                 "Retrying (%r) after connection broken by '%r': %s"

 L. 746       616  LOAD_FAST                'retries'

 L. 747       618  LOAD_FAST                'err'

 L. 748       620  LOAD_FAST                'url'

 L. 744       622  CALL_METHOD_4         4  ''
              624  POP_TOP          

 L. 750       626  LOAD_FAST                'self'
              628  LOAD_ATTR                urlopen

 L. 751       630  LOAD_FAST                'method'

 L. 752       632  LOAD_FAST                'url'

 L. 753       634  LOAD_FAST                'body'

 L. 754       636  LOAD_FAST                'headers'

 L. 755       638  LOAD_FAST                'retries'

 L. 756       640  LOAD_FAST                'redirect'

 L. 757       642  LOAD_FAST                'assert_same_host'

 L. 750       644  BUILD_TUPLE_7         7 

 L. 758       646  LOAD_FAST                'timeout'

 L. 759       648  LOAD_FAST                'pool_timeout'

 L. 760       650  LOAD_FAST                'release_conn'

 L. 761       652  LOAD_FAST                'body_pos'

 L. 750       654  LOAD_CONST               ('timeout', 'pool_timeout', 'release_conn', 'body_pos')
              656  BUILD_CONST_KEY_MAP_4     4 

 L. 762       658  LOAD_FAST                'response_kw'

 L. 750       660  BUILD_MAP_UNPACK_WITH_CALL_2     2 
              662  CALL_FUNCTION_EX_KW     1  'keyword args'
              664  RETURN_VALUE     
            666_0  COME_FROM           606  '606'

 L. 765       666  LOAD_CODE                <code_object drain_and_release_conn>
              668  LOAD_STR                 'HTTPConnectionPool.urlopen.<locals>.drain_and_release_conn'
              670  MAKE_FUNCTION_0          ''
              672  STORE_FAST               'drain_and_release_conn'

 L. 781       674  LOAD_FAST                'redirect'
          676_678  JUMP_IF_FALSE_OR_POP   686  'to 686'
              680  LOAD_FAST                'response'
              682  LOAD_METHOD              get_redirect_location
              684  CALL_METHOD_0         0  ''
            686_0  COME_FROM           676  '676'
              686  STORE_FAST               'redirect_location'

 L. 782       688  LOAD_FAST                'redirect_location'
          690_692  POP_JUMP_IF_FALSE   850  'to 850'

 L. 783       694  LOAD_FAST                'response'
              696  LOAD_ATTR                status
              698  LOAD_CONST               303
              700  COMPARE_OP               ==
          702_704  POP_JUMP_IF_FALSE   710  'to 710'

 L. 784       706  LOAD_STR                 'GET'
              708  STORE_FAST               'method'
            710_0  COME_FROM           702  '702'

 L. 786       710  SETUP_FINALLY       734  'to 734'

 L. 787       712  LOAD_FAST                'retries'
              714  LOAD_ATTR                increment
              716  LOAD_FAST                'method'
              718  LOAD_FAST                'url'
              720  LOAD_FAST                'response'
              722  LOAD_FAST                'self'
              724  LOAD_CONST               ('response', '_pool')
              726  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
              728  STORE_FAST               'retries'
              730  POP_BLOCK        
              732  JUMP_FORWARD        778  'to 778'
            734_0  COME_FROM_FINALLY   710  '710'

 L. 788       734  DUP_TOP          
              736  LOAD_GLOBAL              MaxRetryError
              738  COMPARE_OP               exception-match
          740_742  POP_JUMP_IF_FALSE   776  'to 776'
              744  POP_TOP          
              746  POP_TOP          
              748  POP_TOP          

 L. 789       750  LOAD_FAST                'retries'
              752  LOAD_ATTR                raise_on_redirect
          754_756  POP_JUMP_IF_FALSE   768  'to 768'

 L. 792       758  LOAD_FAST                'drain_and_release_conn'
              760  LOAD_FAST                'response'
              762  CALL_FUNCTION_1       1  ''
              764  POP_TOP          

 L. 793       766  RAISE_VARARGS_0       0  ''
            768_0  COME_FROM           754  '754'

 L. 794       768  LOAD_FAST                'response'
              770  ROT_FOUR         
              772  POP_EXCEPT       
              774  RETURN_VALUE     
            776_0  COME_FROM           740  '740'
              776  END_FINALLY      
            778_0  COME_FROM           732  '732'

 L. 797       778  LOAD_FAST                'drain_and_release_conn'
              780  LOAD_FAST                'response'
              782  CALL_FUNCTION_1       1  ''
              784  POP_TOP          

 L. 799       786  LOAD_FAST                'retries'
              788  LOAD_METHOD              sleep_for_retry
              790  LOAD_FAST                'response'
              792  CALL_METHOD_1         1  ''
              794  POP_TOP          

 L. 800       796  LOAD_GLOBAL              log
              798  LOAD_METHOD              debug
              800  LOAD_STR                 'Redirecting %s -> %s'
              802  LOAD_FAST                'url'
              804  LOAD_FAST                'redirect_location'
              806  CALL_METHOD_3         3  ''
              808  POP_TOP          

 L. 801       810  LOAD_FAST                'self'
              812  LOAD_ATTR                urlopen

 L. 802       814  LOAD_FAST                'method'

 L. 803       816  LOAD_FAST                'redirect_location'

 L. 804       818  LOAD_FAST                'body'

 L. 805       820  LOAD_FAST                'headers'

 L. 801       822  BUILD_TUPLE_4         4 

 L. 806       824  LOAD_FAST                'retries'

 L. 807       826  LOAD_FAST                'redirect'

 L. 808       828  LOAD_FAST                'assert_same_host'

 L. 809       830  LOAD_FAST                'timeout'

 L. 810       832  LOAD_FAST                'pool_timeout'

 L. 811       834  LOAD_FAST                'release_conn'

 L. 812       836  LOAD_FAST                'body_pos'

 L. 801       838  LOAD_CONST               ('retries', 'redirect', 'assert_same_host', 'timeout', 'pool_timeout', 'release_conn', 'body_pos')
              840  BUILD_CONST_KEY_MAP_7     7 

 L. 813       842  LOAD_FAST                'response_kw'

 L. 801       844  BUILD_MAP_UNPACK_WITH_CALL_2     2 
              846  CALL_FUNCTION_EX_KW     1  'keyword args'
              848  RETURN_VALUE     
            850_0  COME_FROM           690  '690'

 L. 817       850  LOAD_GLOBAL              bool
              852  LOAD_FAST                'response'
              854  LOAD_METHOD              getheader
              856  LOAD_STR                 'Retry-After'
              858  CALL_METHOD_1         1  ''
              860  CALL_FUNCTION_1       1  ''
              862  STORE_FAST               'has_retry_after'

 L. 818       864  LOAD_FAST                'retries'
              866  LOAD_METHOD              is_retry
              868  LOAD_FAST                'method'
              870  LOAD_FAST                'response'
              872  LOAD_ATTR                status
              874  LOAD_FAST                'has_retry_after'
              876  CALL_METHOD_3         3  ''
          878_880  POP_JUMP_IF_FALSE  1020  'to 1020'

 L. 819       882  SETUP_FINALLY       906  'to 906'

 L. 820       884  LOAD_FAST                'retries'
              886  LOAD_ATTR                increment
              888  LOAD_FAST                'method'
              890  LOAD_FAST                'url'
              892  LOAD_FAST                'response'
              894  LOAD_FAST                'self'
              896  LOAD_CONST               ('response', '_pool')
              898  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
              900  STORE_FAST               'retries'
              902  POP_BLOCK        
              904  JUMP_FORWARD        950  'to 950'
            906_0  COME_FROM_FINALLY   882  '882'

 L. 821       906  DUP_TOP          
              908  LOAD_GLOBAL              MaxRetryError
              910  COMPARE_OP               exception-match
          912_914  POP_JUMP_IF_FALSE   948  'to 948'
              916  POP_TOP          
              918  POP_TOP          
              920  POP_TOP          

 L. 822       922  LOAD_FAST                'retries'
              924  LOAD_ATTR                raise_on_status
          926_928  POP_JUMP_IF_FALSE   940  'to 940'

 L. 825       930  LOAD_FAST                'drain_and_release_conn'
              932  LOAD_FAST                'response'
              934  CALL_FUNCTION_1       1  ''
              936  POP_TOP          

 L. 826       938  RAISE_VARARGS_0       0  ''
            940_0  COME_FROM           926  '926'

 L. 827       940  LOAD_FAST                'response'
              942  ROT_FOUR         
              944  POP_EXCEPT       
              946  RETURN_VALUE     
            948_0  COME_FROM           912  '912'
              948  END_FINALLY      
            950_0  COME_FROM           904  '904'

 L. 830       950  LOAD_FAST                'drain_and_release_conn'
              952  LOAD_FAST                'response'
              954  CALL_FUNCTION_1       1  ''
              956  POP_TOP          

 L. 832       958  LOAD_FAST                'retries'
              960  LOAD_METHOD              sleep
              962  LOAD_FAST                'response'
              964  CALL_METHOD_1         1  ''
              966  POP_TOP          

 L. 833       968  LOAD_GLOBAL              log
              970  LOAD_METHOD              debug
              972  LOAD_STR                 'Retry: %s'
              974  LOAD_FAST                'url'
              976  CALL_METHOD_2         2  ''
              978  POP_TOP          

 L. 834       980  LOAD_FAST                'self'
              982  LOAD_ATTR                urlopen

 L. 835       984  LOAD_FAST                'method'

 L. 836       986  LOAD_FAST                'url'

 L. 837       988  LOAD_FAST                'body'

 L. 838       990  LOAD_FAST                'headers'

 L. 834       992  BUILD_TUPLE_4         4 

 L. 839       994  LOAD_FAST                'retries'

 L. 840       996  LOAD_FAST                'redirect'

 L. 841       998  LOAD_FAST                'assert_same_host'

 L. 842      1000  LOAD_FAST                'timeout'

 L. 843      1002  LOAD_FAST                'pool_timeout'

 L. 844      1004  LOAD_FAST                'release_conn'

 L. 845      1006  LOAD_FAST                'body_pos'

 L. 834      1008  LOAD_CONST               ('retries', 'redirect', 'assert_same_host', 'timeout', 'pool_timeout', 'release_conn', 'body_pos')
             1010  BUILD_CONST_KEY_MAP_7     7 

 L. 846      1012  LOAD_FAST                'response_kw'

 L. 834      1014  BUILD_MAP_UNPACK_WITH_CALL_2     2 
             1016  CALL_FUNCTION_EX_KW     1  'keyword args'
             1018  RETURN_VALUE     
           1020_0  COME_FROM           878  '878'

 L. 849      1020  LOAD_FAST                'response'
             1022  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `ROT_FOUR' instruction at offset 770


class HTTPSConnectionPool(HTTPConnectionPool):
    """HTTPSConnectionPool"""
    scheme = 'https'
    ConnectionCls = HTTPSConnection

    def __init__(self, host, port=None, strict=False, timeout=Timeout.DEFAULT_TIMEOUT, maxsize=1, block=False, headers=None, retries=None, _proxy=None, _proxy_headers=None, key_file=None, cert_file=None, cert_reqs=None, key_password=None, ca_certs=None, ssl_version=None, assert_hostname=None, assert_fingerprint=None, ca_cert_dir=None, **conn_kw):
        (HTTPConnectionPool.__init__)(
         self, 
         host, 
         port, 
         strict, 
         timeout, 
         maxsize, 
         block, 
         headers, 
         retries, 
         _proxy, 
         _proxy_headers, **conn_kw)
        self.key_file = key_file
        self.cert_file = cert_file
        self.cert_reqs = cert_reqs
        self.key_password = key_password
        self.ca_certs = ca_certs
        self.ca_cert_dir = ca_cert_dir
        self.ssl_version = ssl_version
        self.assert_hostname = assert_hostname
        self.assert_fingerprint = assert_fingerprint

    def _prepare_conn(self, conn):
        """
        Prepare the ``connection`` for :meth:`urllib3.util.ssl_wrap_socket`
        and establish the tunnel if proxy is used.
        """
        if isinstance(conn, VerifiedHTTPSConnection):
            conn.set_cert(key_file=(self.key_file),
              key_password=(self.key_password),
              cert_file=(self.cert_file),
              cert_reqs=(self.cert_reqs),
              ca_certs=(self.ca_certs),
              ca_cert_dir=(self.ca_cert_dir),
              assert_hostname=(self.assert_hostname),
              assert_fingerprint=(self.assert_fingerprint))
            conn.ssl_version = self.ssl_version
        return conn

    def _prepare_proxy(self, conn):
        """
        Establish tunnel connection early, because otherwise httplib
        would improperly set Host: header to proxy's IP:port.
        """
        conn.set_tunnel(self._proxy_host, self.port, self.proxy_headers)
        conn.connect()

    def _new_conn(self):
        """
        Return a fresh :class:`httplib.HTTPSConnection`.
        """
        self.num_connections += 1
        log.debug('Starting new HTTPS connection (%d): %s:%s', self.num_connections, self.host, self.port or )
        if not self.ConnectionCls or self.ConnectionCls is DummyConnection:
            raise SSLError("Can't connect to HTTPS URL because the SSL module is not available.")
        actual_host = self.host
        actual_port = self.port
        if self.proxy is not None:
            actual_host = self.proxy.host
            actual_port = self.proxy.port
        conn = (self.ConnectionCls)(host=actual_host, 
         port=actual_port, 
         timeout=self.timeout.connect_timeout, 
         strict=self.strict, 
         cert_file=self.cert_file, 
         key_file=self.key_file, 
         key_password=self.key_password, **self.conn_kw)
        return self._prepare_conn(conn)

    def _validate_conn(self, conn):
        super(HTTPSConnectionPool, self)._validate_conn(conn)
        if not getattr(conn, 'sock', None):
            conn.connect()
        if not conn.is_verified:
            warnings.warn('Unverified HTTPS request is being made. Adding certificate verification is strongly advised. See: https://urllib3.readthedocs.io/en/latest/advanced-usage.html#ssl-warnings', InsecureRequestWarning)


def connection_from_url(url, **kw):
    r"""
    Given a url, return an :class:`.ConnectionPool` instance of its host.

    This is a shortcut for not having to parse out the scheme, host, and port
    of the url before creating an :class:`.ConnectionPool` instance.

    :param url:
        Absolute URL string that must include the scheme. Port is optional.

    :param \**kw:
        Passes additional parameters to the constructor of the appropriate
        :class:`.ConnectionPool`. Useful for specifying things like
        timeout, maxsize, headers, etc.

    Example::

        >>> conn = connection_from_url('http://google.com/')
        >>> r = conn.request('GET', '/')
    """
    scheme, host, port = get_host(url)
    port = port or 
    if scheme == 'https':
        return HTTPSConnectionPool(host, port=port, **kw)
    return HTTPConnectionPool(host, port=port, **kw)


def _normalize_host(host, scheme):
    """
    Normalize hosts for comparisons and use with sockets.
    """
    host = normalize_host(host, scheme)
    if host.startswith('['):
        if host.endswith(']'):
            host = host[1:-1]
    return host