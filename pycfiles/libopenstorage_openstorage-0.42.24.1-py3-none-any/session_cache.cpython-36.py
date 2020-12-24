# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-build-ed191__6/grpcio/grpc/experimental/session_cache.py
# Compiled at: 2020-01-10 16:25:22
# Size of source mod 2**32: 1533 bytes
"""gRPC's APIs for TLS Session Resumption support"""
from grpc._cython import cygrpc as _cygrpc

def ssl_session_cache_lru(capacity):
    """Creates an SSLSessionCache with LRU replacement policy

    Args:
      capacity: Size of the cache

    Returns:
      An SSLSessionCache with LRU replacement policy that can be passed as a value for
      the grpc.ssl_session_cache option to a grpc.Channel. SSL session caches are used
      to store session tickets, which clients can present to resume previous TLS sessions
      with a server.
    """
    return SSLSessionCache(_cygrpc.SSLSessionCacheLRU(capacity))


class SSLSessionCache(object):
    __doc__ = 'An encapsulation of a session cache used for TLS session resumption.\n\n    Instances of this class can be passed to a Channel as values for the\n    grpc.ssl_session_cache option\n    '

    def __init__(self, cache):
        self._cache = cache

    def __int__(self):
        return int(self._cache)