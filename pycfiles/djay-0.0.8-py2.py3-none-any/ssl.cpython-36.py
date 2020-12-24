# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-m_4qh6p6/requests-toolbelt/requests_toolbelt/adapters/ssl.py
# Compiled at: 2019-07-30 18:47:11
# Size of source mod 2**32: 2399 bytes
"""

requests_toolbelt.ssl_adapter
=============================

This file contains an implementation of the SSLAdapter originally demonstrated
in this blog post:
https://lukasa.co.uk/2013/01/Choosing_SSL_Version_In_Requests/

"""
import requests
from requests.adapters import HTTPAdapter
from .._compat import poolmanager

class SSLAdapter(HTTPAdapter):
    __doc__ = "\n    A HTTPS Adapter for Python Requests that allows the choice of the SSL/TLS\n    version negotiated by Requests. This can be used either to enforce the\n    choice of high-security TLS versions (where supported), or to work around\n    misbehaving servers that fail to correctly negotiate the default TLS\n    version being offered.\n\n    Example usage:\n\n        >>> import requests\n        >>> import ssl\n        >>> from requests_toolbelt import SSLAdapter\n        >>> s = requests.Session()\n        >>> s.mount('https://', SSLAdapter(ssl.PROTOCOL_TLSv1))\n\n    You can replace the chosen protocol with any that are available in the\n    default Python SSL module. All subsequent requests that match the adapter\n    prefix will use the chosen SSL version instead of the default.\n\n    This adapter will also attempt to change the SSL/TLS version negotiated by\n    Requests when using a proxy. However, this may not always be possible:\n    prior to Requests v2.4.0 the adapter did not have access to the proxy setup\n    code. In earlier versions of Requests, this adapter will not function\n    properly when used with proxies.\n    "
    __attrs__ = HTTPAdapter.__attrs__ + ['ssl_version']

    def __init__(self, ssl_version=None, **kwargs):
        self.ssl_version = ssl_version
        (super(SSLAdapter, self).__init__)(**kwargs)

    def init_poolmanager(self, connections, maxsize, block=False):
        self.poolmanager = poolmanager.PoolManager(num_pools=connections,
          maxsize=maxsize,
          block=block,
          ssl_version=(self.ssl_version))

    if requests.__build__ >= 132096:

        def proxy_manager_for(self, *args, **kwargs):
            kwargs['ssl_version'] = self.ssl_version
            return (super(SSLAdapter, self).proxy_manager_for)(*args, **kwargs)