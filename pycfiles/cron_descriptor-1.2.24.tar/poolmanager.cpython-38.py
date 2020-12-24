# uncompyle6 version 3.6.7
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: ./vendor/urllib3/poolmanager.py
# Compiled at: 2019-11-10 08:27:46
# Size of source mod 2**32: 17053 bytes
from __future__ import absolute_import
import collections, functools, logging
from ._collections import RecentlyUsedContainer
from .connectionpool import HTTPConnectionPool, HTTPSConnectionPool
from .connectionpool import port_by_scheme
from .exceptions import LocationValueError, MaxRetryError, ProxySchemeUnknown
from .packages import six
from packages.six.moves.urllib.parse import urljoin
from .request import RequestMethods
from util.url import parse_url
from util.retry import Retry
__all__ = [
 'PoolManager', 'ProxyManager', 'proxy_from_url']
log = logging.getLogger(__name__)
SSL_KEYWORDS = ('key_file', 'cert_file', 'cert_reqs', 'ca_certs', 'ssl_version', 'ca_cert_dir',
                'ssl_context', 'key_password')
_key_fields = ('key_scheme', 'key_host', 'key_port', 'key_timeout', 'key_retries',
               'key_strict', 'key_block', 'key_source_address', 'key_key_file', 'key_key_password',
               'key_cert_file', 'key_cert_reqs', 'key_ca_certs', 'key_ssl_version',
               'key_ca_cert_dir', 'key_ssl_context', 'key_maxsize', 'key_headers',
               'key__proxy', 'key__proxy_headers', 'key_socket_options', 'key__socks_options',
               'key_assert_hostname', 'key_assert_fingerprint', 'key_server_hostname')
PoolKey = collections.namedtuple('PoolKey', _key_fields)

def _default_key_normalizer(key_class, request_context):
    """
    Create a pool key out of a request context dictionary.

    According to RFC 3986, both the scheme and host are case-insensitive.
    Therefore, this function normalizes both before constructing the pool
    key for an HTTPS request. If you wish to change this behaviour, provide
    alternate callables to ``key_fn_by_scheme``.

    :param key_class:
        The class to use when constructing the key. This should be a namedtuple
        with the ``scheme`` and ``host`` keys at a minimum.
    :type  key_class: namedtuple
    :param request_context:
        A dictionary-like object that contain the context for a request.
    :type  request_context: dict

    :return: A namedtuple that can be used as a connection pool key.
    :rtype:  PoolKey
    """
    context = request_context.copy()
    context['scheme'] = context['scheme'].lower()
    context['host'] = context['host'].lower()
    for key in ('headers', '_proxy_headers', '_socks_options'):
        if key in context:
            if context[key] is not None:
                context[key] = frozenset(context[key].items())
            socket_opts = context.get('socket_options')
            if socket_opts is not None:
                context['socket_options'] = tuple(socket_opts)
            for key in list(context.keys()):
                context['key_' + key] = context.pop(key)

    for field in key_class._fields:
        if field not in context:
            context[field] = None
        return key_class(**context)


key_fn_by_scheme = {'http':functools.partial(_default_key_normalizer, PoolKey), 
 'https':functools.partial(_default_key_normalizer, PoolKey)}
pool_classes_by_scheme = {'http':HTTPConnectionPool, 
 'https':HTTPSConnectionPool}

class PoolManager(RequestMethods):
    """PoolManager"""
    proxy = None

    def __init__(self, num_pools=10, headers=None, **connection_pool_kw):
        RequestMethods.__init__(self, headers)
        self.connection_pool_kw = connection_pool_kw
        self.pools = RecentlyUsedContainer(num_pools, dispose_func=(lambda p: p.close()))
        self.pool_classes_by_scheme = pool_classes_by_scheme
        self.key_fn_by_scheme = key_fn_by_scheme.copy()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.clear()
        return False

    def _new_pool(self, scheme, host, port, request_context=None):
        """
        Create a new :class:`ConnectionPool` based on host, port, scheme, and
        any additional pool keyword arguments.

        If ``request_context`` is provided, it is provided as keyword arguments
        to the pool class used. This method is used to actually create the
        connection pools handed out by :meth:`connection_from_url` and
        companion methods. It is intended to be overridden for customization.
        """
        pool_cls = self.pool_classes_by_scheme[scheme]
        if request_context is None:
            request_context = self.connection_pool_kw.copy()
        for key in ('scheme', 'host', 'port'):
            request_context.pop(key, None)

        if scheme == 'http':
            for kw in SSL_KEYWORDS:
                request_context.pop(kw, None)

        return pool_cls(host, port, **request_context)

    def clear(self):
        """
        Empty our store of pools and direct them all to close.

        This will not affect in-flight connections, but they will not be
        re-used after completion.
        """
        self.pools.clear()

    def connection_from_host(self, host, port=None, scheme='http', pool_kwargs=None):
        """
        Get a :class:`ConnectionPool` based on the host, port, and scheme.

        If ``port`` isn't given, it will be derived from the ``scheme`` using
        ``urllib3.connectionpool.port_by_scheme``. If ``pool_kwargs`` is
        provided, it is merged with the instance's ``connection_pool_kw``
        variable and used to create the new connection pool, if one is
        needed.
        """
        if not host:
            raise LocationValueError('No host specified.')
        request_context = self._merge_pool_kwargs(pool_kwargs)
        request_context['scheme'] = scheme or 
        if not port:
            port = port_by_scheme.get(request_context['scheme'].lower(), 80)
        request_context['port'] = port
        request_context['host'] = host
        return self.connection_from_context(request_context)

    def connection_from_context(self, request_context):
        """
        Get a :class:`ConnectionPool` based on the request context.

        ``request_context`` must at least contain the ``scheme`` key and its
        value must be a key in ``key_fn_by_scheme`` instance variable.
        """
        scheme = request_context['scheme'].lower()
        pool_key_constructor = self.key_fn_by_scheme[scheme]
        pool_key = pool_key_constructor(request_context)
        return self.connection_from_pool_key(pool_key, request_context=request_context)

    def connection_from_pool_key--- This code section failed: ---

 L. 257         0  LOAD_FAST                'self'
                2  LOAD_ATTR                pools
                4  LOAD_ATTR                lock
                6  SETUP_WITH           98  'to 98'
                8  POP_TOP          

 L. 260        10  LOAD_FAST                'self'
               12  LOAD_ATTR                pools
               14  LOAD_METHOD              get
               16  LOAD_FAST                'pool_key'
               18  CALL_METHOD_1         1  ''
               20  STORE_FAST               'pool'

 L. 261        22  LOAD_FAST                'pool'
               24  POP_JUMP_IF_FALSE    42  'to 42'

 L. 262        26  LOAD_FAST                'pool'
               28  POP_BLOCK        
               30  ROT_TWO          
               32  BEGIN_FINALLY    
               34  WITH_CLEANUP_START
               36  WITH_CLEANUP_FINISH
               38  POP_FINALLY           0  ''
               40  RETURN_VALUE     
             42_0  COME_FROM            24  '24'

 L. 265        42  LOAD_FAST                'request_context'
               44  LOAD_STR                 'scheme'
               46  BINARY_SUBSCR    
               48  STORE_FAST               'scheme'

 L. 266        50  LOAD_FAST                'request_context'
               52  LOAD_STR                 'host'
               54  BINARY_SUBSCR    
               56  STORE_FAST               'host'

 L. 267        58  LOAD_FAST                'request_context'
               60  LOAD_STR                 'port'
               62  BINARY_SUBSCR    
               64  STORE_FAST               'port'

 L. 268        66  LOAD_FAST                'self'
               68  LOAD_ATTR                _new_pool
               70  LOAD_FAST                'scheme'
               72  LOAD_FAST                'host'
               74  LOAD_FAST                'port'
               76  LOAD_FAST                'request_context'
               78  LOAD_CONST               ('request_context',)
               80  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
               82  STORE_FAST               'pool'

 L. 269        84  LOAD_FAST                'pool'
               86  LOAD_FAST                'self'
               88  LOAD_ATTR                pools
               90  LOAD_FAST                'pool_key'
               92  STORE_SUBSCR     
               94  POP_BLOCK        
               96  BEGIN_FINALLY    
             98_0  COME_FROM_WITH        6  '6'
               98  WITH_CLEANUP_START
              100  WITH_CLEANUP_FINISH
              102  END_FINALLY      

 L. 271       104  LOAD_FAST                'pool'
              106  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `POP_BLOCK' instruction at offset 28

    def connection_from_url(self, url, pool_kwargs=None):
        """
        Similar to :func:`urllib3.connectionpool.connection_from_url`.

        If ``pool_kwargs`` is not provided and a new pool needs to be
        constructed, ``self.connection_pool_kw`` is used to initialize
        the :class:`urllib3.connectionpool.ConnectionPool`. If ``pool_kwargs``
        is provided, it is used instead. Note that if a new pool does not
        need to be created for the request, the provided ``pool_kwargs`` are
        not used.
        """
        u = parse_url(url)
        return self.connection_from_host((u.host),
          port=(u.port), scheme=(u.scheme), pool_kwargs=pool_kwargs)

    def _merge_pool_kwargs(self, override):
        """
        Merge a dictionary of override values for self.connection_pool_kw.

        This does not modify self.connection_pool_kw and returns a new dict.
        Any keys in the override dictionary with a value of ``None`` are
        removed from the merged dictionary.
        """
        base_pool_kwargs = self.connection_pool_kw.copy()
        if override:
            for key, value in override.items():
                if value is None:
                    try:
                        del base_pool_kwargs[key]
                    except KeyError:
                        pass

                else:
                    base_pool_kwargs[key] = value

        return base_pool_kwargs

    def urlopen--- This code section failed: ---

 L. 318         0  LOAD_GLOBAL              parse_url
                2  LOAD_FAST                'url'
                4  CALL_FUNCTION_1       1  ''
                6  STORE_FAST               'u'

 L. 319         8  LOAD_FAST                'self'
               10  LOAD_ATTR                connection_from_host
               12  LOAD_FAST                'u'
               14  LOAD_ATTR                host
               16  LOAD_FAST                'u'
               18  LOAD_ATTR                port
               20  LOAD_FAST                'u'
               22  LOAD_ATTR                scheme
               24  LOAD_CONST               ('port', 'scheme')
               26  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
               28  STORE_FAST               'conn'

 L. 321        30  LOAD_CONST               False
               32  LOAD_FAST                'kw'
               34  LOAD_STR                 'assert_same_host'
               36  STORE_SUBSCR     

 L. 322        38  LOAD_CONST               False
               40  LOAD_FAST                'kw'
               42  LOAD_STR                 'redirect'
               44  STORE_SUBSCR     

 L. 324        46  LOAD_STR                 'headers'
               48  LOAD_FAST                'kw'
               50  COMPARE_OP               not-in
               52  POP_JUMP_IF_FALSE    68  'to 68'

 L. 325        54  LOAD_FAST                'self'
               56  LOAD_ATTR                headers
               58  LOAD_METHOD              copy
               60  CALL_METHOD_0         0  ''
               62  LOAD_FAST                'kw'
               64  LOAD_STR                 'headers'
               66  STORE_SUBSCR     
             68_0  COME_FROM            52  '52'

 L. 327        68  LOAD_FAST                'self'
               70  LOAD_ATTR                proxy
               72  LOAD_CONST               None
               74  COMPARE_OP               is-not
               76  POP_JUMP_IF_FALSE   106  'to 106'
               78  LOAD_FAST                'u'
               80  LOAD_ATTR                scheme
               82  LOAD_STR                 'http'
               84  COMPARE_OP               ==
               86  POP_JUMP_IF_FALSE   106  'to 106'

 L. 328        88  LOAD_FAST                'conn'
               90  LOAD_ATTR                urlopen
               92  LOAD_FAST                'method'
               94  LOAD_FAST                'url'
               96  BUILD_TUPLE_2         2 
               98  LOAD_FAST                'kw'
              100  CALL_FUNCTION_EX_KW     1  'keyword args'
              102  STORE_FAST               'response'
              104  JUMP_FORWARD        124  'to 124'
            106_0  COME_FROM            86  '86'
            106_1  COME_FROM            76  '76'

 L. 330       106  LOAD_FAST                'conn'
              108  LOAD_ATTR                urlopen
              110  LOAD_FAST                'method'
              112  LOAD_FAST                'u'
              114  LOAD_ATTR                request_uri
              116  BUILD_TUPLE_2         2 
              118  LOAD_FAST                'kw'
              120  CALL_FUNCTION_EX_KW     1  'keyword args'
              122  STORE_FAST               'response'
            124_0  COME_FROM           104  '104'

 L. 332       124  LOAD_FAST                'redirect'
              126  JUMP_IF_FALSE_OR_POP   134  'to 134'
              128  LOAD_FAST                'response'
              130  LOAD_METHOD              get_redirect_location
              132  CALL_METHOD_0         0  ''
            134_0  COME_FROM           126  '126'
              134  STORE_FAST               'redirect_location'

 L. 333       136  LOAD_FAST                'redirect_location'
              138  POP_JUMP_IF_TRUE    144  'to 144'

 L. 334       140  LOAD_FAST                'response'
              142  RETURN_VALUE     
            144_0  COME_FROM           138  '138'

 L. 337       144  LOAD_GLOBAL              urljoin
              146  LOAD_FAST                'url'
              148  LOAD_FAST                'redirect_location'
              150  CALL_FUNCTION_2       2  ''
              152  STORE_FAST               'redirect_location'

 L. 340       154  LOAD_FAST                'response'
              156  LOAD_ATTR                status
              158  LOAD_CONST               303
              160  COMPARE_OP               ==
              162  POP_JUMP_IF_FALSE   168  'to 168'

 L. 341       164  LOAD_STR                 'GET'
              166  STORE_FAST               'method'
            168_0  COME_FROM           162  '162'

 L. 343       168  LOAD_FAST                'kw'
              170  LOAD_METHOD              get
              172  LOAD_STR                 'retries'
              174  CALL_METHOD_1         1  ''
              176  STORE_FAST               'retries'

 L. 344       178  LOAD_GLOBAL              isinstance
              180  LOAD_FAST                'retries'
              182  LOAD_GLOBAL              Retry
              184  CALL_FUNCTION_2       2  ''
              186  POP_JUMP_IF_TRUE    202  'to 202'

 L. 345       188  LOAD_GLOBAL              Retry
              190  LOAD_ATTR                from_int
              192  LOAD_FAST                'retries'
              194  LOAD_FAST                'redirect'
              196  LOAD_CONST               ('redirect',)
              198  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              200  STORE_FAST               'retries'
            202_0  COME_FROM           186  '186'

 L. 350       202  LOAD_FAST                'retries'
              204  LOAD_ATTR                remove_headers_on_redirect
          206_208  POP_JUMP_IF_FALSE   280  'to 280'
              210  LOAD_FAST                'conn'
              212  LOAD_METHOD              is_same_host

 L. 351       214  LOAD_FAST                'redirect_location'

 L. 350       216  CALL_METHOD_1         1  ''
          218_220  POP_JUMP_IF_TRUE    280  'to 280'

 L. 353       222  LOAD_GLOBAL              list
              224  LOAD_GLOBAL              six
              226  LOAD_METHOD              iterkeys
              228  LOAD_FAST                'kw'
              230  LOAD_STR                 'headers'
              232  BINARY_SUBSCR    
              234  CALL_METHOD_1         1  ''
              236  CALL_FUNCTION_1       1  ''
              238  STORE_FAST               'headers'

 L. 354       240  LOAD_FAST                'headers'
              242  GET_ITER         
            244_0  COME_FROM           260  '260'
              244  FOR_ITER            280  'to 280'
              246  STORE_FAST               'header'

 L. 355       248  LOAD_FAST                'header'
              250  LOAD_METHOD              lower
              252  CALL_METHOD_0         0  ''
              254  LOAD_FAST                'retries'
              256  LOAD_ATTR                remove_headers_on_redirect
              258  COMPARE_OP               in
              260  POP_JUMP_IF_FALSE   244  'to 244'

 L. 356       262  LOAD_FAST                'kw'
              264  LOAD_STR                 'headers'
              266  BINARY_SUBSCR    
              268  LOAD_METHOD              pop
              270  LOAD_FAST                'header'
              272  LOAD_CONST               None
              274  CALL_METHOD_2         2  ''
              276  POP_TOP          
              278  JUMP_BACK           244  'to 244'
            280_0  COME_FROM           218  '218'
            280_1  COME_FROM           206  '206'

 L. 358       280  SETUP_FINALLY       304  'to 304'

 L. 359       282  LOAD_FAST                'retries'
              284  LOAD_ATTR                increment
              286  LOAD_FAST                'method'
              288  LOAD_FAST                'url'
              290  LOAD_FAST                'response'
              292  LOAD_FAST                'conn'
              294  LOAD_CONST               ('response', '_pool')
              296  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
              298  STORE_FAST               'retries'
              300  POP_BLOCK        
              302  JUMP_FORWARD        340  'to 340'
            304_0  COME_FROM_FINALLY   280  '280'

 L. 360       304  DUP_TOP          
              306  LOAD_GLOBAL              MaxRetryError
              308  COMPARE_OP               exception-match
          310_312  POP_JUMP_IF_FALSE   338  'to 338'
              314  POP_TOP          
              316  POP_TOP          
              318  POP_TOP          

 L. 361       320  LOAD_FAST                'retries'
              322  LOAD_ATTR                raise_on_redirect
          324_326  POP_JUMP_IF_FALSE   330  'to 330'

 L. 362       328  RAISE_VARARGS_0       0  ''
            330_0  COME_FROM           324  '324'

 L. 363       330  LOAD_FAST                'response'
              332  ROT_FOUR         
              334  POP_EXCEPT       
              336  RETURN_VALUE     
            338_0  COME_FROM           310  '310'
              338  END_FINALLY      
            340_0  COME_FROM           302  '302'

 L. 365       340  LOAD_FAST                'retries'
              342  LOAD_FAST                'kw'
              344  LOAD_STR                 'retries'
              346  STORE_SUBSCR     

 L. 366       348  LOAD_FAST                'redirect'
              350  LOAD_FAST                'kw'
              352  LOAD_STR                 'redirect'
              354  STORE_SUBSCR     

 L. 368       356  LOAD_GLOBAL              log
              358  LOAD_METHOD              info
              360  LOAD_STR                 'Redirecting %s -> %s'
              362  LOAD_FAST                'url'
              364  LOAD_FAST                'redirect_location'
              366  CALL_METHOD_3         3  ''
              368  POP_TOP          

 L. 369       370  LOAD_FAST                'self'
              372  LOAD_ATTR                urlopen
              374  LOAD_FAST                'method'
              376  LOAD_FAST                'redirect_location'
              378  BUILD_TUPLE_2         2 
              380  LOAD_FAST                'kw'
              382  CALL_FUNCTION_EX_KW     1  'keyword args'
              384  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `ROT_FOUR' instruction at offset 332


class ProxyManager(PoolManager):
    """ProxyManager"""

    def __init__(self, proxy_url, num_pools=10, headers=None, proxy_headers=None, **connection_pool_kw):
        if isinstanceproxy_urlHTTPConnectionPool:
            proxy_url = '%s://%s:%i' % (
             proxy_url.scheme,
             proxy_url.host,
             proxy_url.port)
        proxy = parse_url(proxy_url)
        if not proxy.port:
            port = port_by_scheme.get(proxy.scheme, 80)
            proxy = proxy._replace(port=port)
        if proxy.scheme not in ('http', 'https'):
            raise ProxySchemeUnknown(proxy.scheme)
        self.proxy = proxy
        self.proxy_headers = proxy_headers or 
        connection_pool_kw['_proxy'] = self.proxy
        connection_pool_kw['_proxy_headers'] = self.proxy_headers
        (superProxyManagerself.__init__)(num_pools, headers, **connection_pool_kw)

    def connection_from_host(self, host, port=None, scheme='http', pool_kwargs=None):
        if scheme == 'https':
            return superProxyManagerself.connection_from_host(host,
              port, scheme, pool_kwargs=pool_kwargs)
        return superProxyManagerself.connection_from_host((self.proxy.host),
          (self.proxy.port), (self.proxy.scheme), pool_kwargs=pool_kwargs)

    def _set_proxy_headers(self, url, headers=None):
        """
        Sets headers needed by proxies: specifically, the Accept and Host
        headers. Only sets headers not provided by the user.
        """
        headers_ = {'Accept': '*/*'}
        netloc = parse_url(url).netloc
        if netloc:
            headers_['Host'] = netloc
        if headers:
            headers_.update(headers)
        return headers_

    def urlopen(self, method, url, redirect=True, **kw):
        """Same as HTTP(S)ConnectionPool.urlopen, ``url`` must be absolute."""
        u = parse_url(url)
        if u.scheme == 'http':
            headers = kw.get('headers', self.headers)
            kw['headers'] = self._set_proxy_headers(url, headers)
        return (superProxyManagerself.urlopen)(method, url, redirect=redirect, **kw)


def proxy_from_url(url, **kw):
    return ProxyManager(proxy_url=url, **kw)