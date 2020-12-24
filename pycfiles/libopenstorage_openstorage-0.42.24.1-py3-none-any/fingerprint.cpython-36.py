# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-build-ed191__6/requests-toolbelt/requests_toolbelt/adapters/fingerprint.py
# Compiled at: 2020-01-10 16:25:32
# Size of source mod 2**32: 1404 bytes
"""Submodule containing the implementation for the FingerprintAdapter.

This file contains an implementation of a Transport Adapter that validates
the fingerprints of SSL certificates presented upon connection.
"""
from requests.adapters import HTTPAdapter
from .._compat import poolmanager

class FingerprintAdapter(HTTPAdapter):
    __doc__ = "\n    A HTTPS Adapter for Python Requests that verifies certificate fingerprints,\n    instead of certificate hostnames.\n\n    Example usage:\n\n    .. code-block:: python\n\n        import requests\n        import ssl\n        from requests_toolbelt.adapters.fingerprint import FingerprintAdapter\n\n        twitter_fingerprint = '...'\n        s = requests.Session()\n        s.mount(\n            'https://twitter.com',\n            FingerprintAdapter(twitter_fingerprint)\n        )\n\n    The fingerprint should be provided as a hexadecimal string, optionally\n    containing colons.\n    "
    __attrs__ = HTTPAdapter.__attrs__ + ['fingerprint']

    def __init__(self, fingerprint, **kwargs):
        self.fingerprint = fingerprint
        (super(FingerprintAdapter, self).__init__)(**kwargs)

    def init_poolmanager(self, connections, maxsize, block=False):
        self.poolmanager = poolmanager.PoolManager(num_pools=connections,
          maxsize=maxsize,
          block=block,
          assert_fingerprint=(self.fingerprint))