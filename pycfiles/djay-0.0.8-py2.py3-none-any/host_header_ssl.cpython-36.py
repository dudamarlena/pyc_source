# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-m_4qh6p6/requests-toolbelt/requests_toolbelt/adapters/host_header_ssl.py
# Compiled at: 2019-07-30 18:47:11
# Size of source mod 2**32: 1396 bytes
"""
requests_toolbelt.adapters.host_header_ssl
==========================================

This file contains an implementation of the HostHeaderSSLAdapter.
"""
from requests.adapters import HTTPAdapter

class HostHeaderSSLAdapter(HTTPAdapter):
    __doc__ = '\n    A HTTPS Adapter for Python Requests that sets the hostname for certificate\n    verification based on the Host header.\n\n    This allows requesting the IP address directly via HTTPS without getting\n    a "hostname doesn\'t match" exception.\n\n    Example usage:\n\n        >>> s.mount(\'https://\', HostHeaderSSLAdapter())\n        >>> s.get("https://93.184.216.34", headers={"Host": "example.org"})\n\n    '

    def send(self, request, **kwargs):
        host_header = None
        for header in request.headers:
            if header.lower() == 'host':
                host_header = request.headers[header]
                break

        connection_pool_kwargs = self.poolmanager.connection_pool_kw
        if host_header:
            connection_pool_kwargs['assert_hostname'] = host_header
        else:
            if 'assert_hostname' in connection_pool_kwargs:
                connection_pool_kwargs.pop('assert_hostname', None)
        return (super(HostHeaderSSLAdapter, self).send)(request, **kwargs)