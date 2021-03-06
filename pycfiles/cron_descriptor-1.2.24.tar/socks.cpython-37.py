# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /private/var/folders/pb/598z8h910dvf2wrvwnbyl_2m0000gn/T/pip-install-65c3rg8f/urllib3/urllib3/contrib/socks.py
# Compiled at: 2019-11-10 08:27:46
# Size of source mod 2**32: 7036 bytes
__doc__ = '\nThis module contains provisional support for SOCKS proxies from within\nurllib3. This module supports SOCKS4, SOCKS4A (an extension of SOCKS4), and\nSOCKS5. To enable its functionality, either install PySocks or install this\nmodule with the ``socks`` extra.\n\nThe SOCKS implementation supports the full range of urllib3 features. It also\nsupports the following SOCKS features:\n\n- SOCKS4A (``proxy_url=\'socks4a://...``)\n- SOCKS4 (``proxy_url=\'socks4://...``)\n- SOCKS5 with remote DNS (``proxy_url=\'socks5h://...``)\n- SOCKS5 with local DNS (``proxy_url=\'socks5://...``)\n- Usernames and passwords for the SOCKS proxy\n\n .. note::\n    It is recommended to use ``socks5h://`` or ``socks4a://`` schemes in\n    your ``proxy_url`` to ensure that DNS resolution is done from the remote\n    server instead of client-side when connecting to a domain name.\n\nSOCKS4 supports IPv4 and domain names with the SOCKS4A extension. SOCKS5\nsupports IPv4, IPv6, and domain names.\n\nWhen connecting to a SOCKS4 proxy the ``username`` portion of the ``proxy_url``\nwill be sent as the ``userid`` section of the SOCKS request::\n\n    proxy_url="socks4a://<userid>@proxy-host"\n\nWhen connecting to a SOCKS5 proxy the ``username`` and ``password`` portion\nof the ``proxy_url`` will be sent as the username/password to authenticate\nwith the proxy::\n\n    proxy_url="socks5h://<username>:<password>@proxy-host"\n\n'
from __future__ import absolute_import
try:
    import socks
except ImportError:
    import warnings
    from ..exceptions import DependencyWarning
    warnings.warn('SOCKS support in urllib3 requires the installation of optional dependencies: specifically, PySocks.  For more information, see https://urllib3.readthedocs.io/en/latest/contrib.html#socks-proxies', DependencyWarning)
    raise

from socket import error as SocketError, timeout as SocketTimeout
from ..connection import HTTPConnection, HTTPSConnection
from ..connectionpool import HTTPConnectionPool, HTTPSConnectionPool
from ..exceptions import ConnectTimeoutError, NewConnectionError
from ..poolmanager import PoolManager
from util.url import parse_url
try:
    import ssl
except ImportError:
    ssl = None

class SOCKSConnection(HTTPConnection):
    """SOCKSConnection"""

    def __init__(self, *args, **kwargs):
        self._socks_options = kwargs.pop('_socks_options')
        (super(SOCKSConnection, self).__init__)(*args, **kwargs)

    def _new_conn(self):
        """
        Establish a new connection via the SOCKS proxy.
        """
        extra_kw = {}
        if self.source_address:
            extra_kw['source_address'] = self.source_address
        if self.socket_options:
            extra_kw['socket_options'] = self.socket_options
        try:
            conn = (socks.create_connection)((self.host, self.port), proxy_type=self._socks_options['socks_version'], 
             proxy_addr=self._socks_options['proxy_host'], 
             proxy_port=self._socks_options['proxy_port'], 
             proxy_username=self._socks_options['username'], 
             proxy_password=self._socks_options['password'], 
             proxy_rdns=self._socks_options['rdns'], 
             timeout=self.timeout, **extra_kw)
        except SocketTimeout:
            raise ConnectTimeoutError(self, 'Connection to %s timed out. (connect timeout=%s)' % (
             self.host, self.timeout))
        except socks.ProxyError as e:
            try:
                if e.socket_err:
                    error = e.socket_err
                    if isinstance(error, SocketTimeout):
                        raise ConnectTimeoutError(self, 'Connection to %s timed out. (connect timeout=%s)' % (
                         self.host, self.timeout))
                    else:
                        raise NewConnectionError(self, 'Failed to establish a new connection: %s' % error)
                else:
                    raise NewConnectionError(self, 'Failed to establish a new connection: %s' % e)
            finally:
                e = None
                del e

        except SocketError as e:
            try:
                raise NewConnectionError(self, 'Failed to establish a new connection: %s' % e)
            finally:
                e = None
                del e

        return conn


class SOCKSHTTPSConnection(SOCKSConnection, HTTPSConnection):
    pass


class SOCKSHTTPConnectionPool(HTTPConnectionPool):
    ConnectionCls = SOCKSConnection


class SOCKSHTTPSConnectionPool(HTTPSConnectionPool):
    ConnectionCls = SOCKSHTTPSConnection


class SOCKSProxyManager(PoolManager):
    """SOCKSProxyManager"""
    pool_classes_by_scheme = {'http':SOCKSHTTPConnectionPool, 
     'https':SOCKSHTTPSConnectionPool}

    def __init__(self, proxy_url, username=None, password=None, num_pools=10, headers=None, **connection_pool_kw):
        parsed = parse_url(proxy_url)
        if username is None:
            if password is None:
                if parsed.auth is not None:
                    split = parsed.auth.split(':')
                    if len(split) == 2:
                        username, password = split
        elif parsed.scheme == 'socks5':
            socks_version = socks.PROXY_TYPE_SOCKS5
            rdns = False
        elif parsed.scheme == 'socks5h':
            socks_version = socks.PROXY_TYPE_SOCKS5
            rdns = True
        elif parsed.scheme == 'socks4':
            socks_version = socks.PROXY_TYPE_SOCKS4
            rdns = False
        elif parsed.scheme == 'socks4a':
            socks_version = socks.PROXY_TYPE_SOCKS4
            rdns = True
        else:
            raise ValueError('Unable to determine SOCKS version from %s' % proxy_url)
        self.proxy_url = proxy_url
        socks_options = {'socks_version':socks_version, 
         'proxy_host':parsed.host, 
         'proxy_port':parsed.port, 
         'username':username, 
         'password':password, 
         'rdns':rdns}
        connection_pool_kw['_socks_options'] = socks_options
        (super(SOCKSProxyManager, self).__init__)(
         num_pools, headers, **connection_pool_kw)
        self.pool_classes_by_scheme = SOCKSProxyManager.pool_classes_by_scheme