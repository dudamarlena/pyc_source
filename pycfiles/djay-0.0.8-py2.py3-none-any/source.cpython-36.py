# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-m_4qh6p6/requests-toolbelt/requests_toolbelt/adapters/source.py
# Compiled at: 2019-07-30 18:47:11
# Size of source mod 2**32: 2608 bytes
"""
requests_toolbelt.source_adapter
================================

This file contains an implementation of the SourceAddressAdapter originally
demonstrated on the Requests GitHub page.
"""
from requests.adapters import HTTPAdapter
from .._compat import poolmanager, basestring

class SourceAddressAdapter(HTTPAdapter):
    __doc__ = '\n    A Source Address Adapter for Python Requests that enables you to choose the\n    local address to bind to. This allows you to send your HTTP requests from a\n    specific interface and IP address.\n\n    Two address formats are accepted. The first is a string: this will set the\n    local IP address to the address given in the string, and will also choose a\n    semi-random high port for the local port number.\n\n    The second is a two-tuple of the form (ip address, port): for example,\n    ``(\'10.10.10.10\', 8999)``. This will set the local IP address to the first\n    element, and the local port to the second element. If ``0`` is used as the\n    port number, a semi-random high port will be selected.\n\n    .. warning:: Setting an explicit local port can have negative interactions\n                 with connection-pooling in Requests: in particular, it risks\n                 the possibility of getting "Address in use" errors. The\n                 string-only argument is generally preferred to the tuple-form.\n\n    Example usage:\n\n    .. code-block:: python\n\n        import requests\n        from requests_toolbelt.adapters.source import SourceAddressAdapter\n\n        s = requests.Session()\n        s.mount(\'http://\', SourceAddressAdapter(\'10.10.10.10\'))\n        s.mount(\'https://\', SourceAddressAdapter((\'10.10.10.10\', 8999)))\n    '

    def __init__(self, source_address, **kwargs):
        if isinstance(source_address, basestring):
            self.source_address = (
             source_address, 0)
        else:
            if isinstance(source_address, tuple):
                self.source_address = source_address
            else:
                raise TypeError('source_address must be IP address string or (ip, port) tuple')
        (super(SourceAddressAdapter, self).__init__)(**kwargs)

    def init_poolmanager(self, connections, maxsize, block=False):
        self.poolmanager = poolmanager.PoolManager(num_pools=connections,
          maxsize=maxsize,
          block=block,
          source_address=(self.source_address))

    def proxy_manager_for(self, *args, **kwargs):
        kwargs['source_address'] = self.source_address
        return (super(SourceAddressAdapter, self).proxy_manager_for)(*args, **kwargs)