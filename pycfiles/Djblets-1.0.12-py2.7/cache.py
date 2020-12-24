# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-x86_64/egg/djblets/util/compat/django/core/cache.py
# Compiled at: 2019-06-12 01:17:17
from django.core.cache.backends.base import InvalidCacheBackendError
from django.utils.six.moves.urllib.parse import parse_qsl

def parse_backend_uri(backend_uri):
    """
    Converts the "backend_uri" into a cache scheme ('db', 'memcached', etc), a
    host and any extra params that are required for the backend. Returns a
    (scheme, host, params) tuple.
    """
    if backend_uri.find(':') == -1:
        raise InvalidCacheBackendError('Backend URI must start with scheme://')
    scheme, rest = backend_uri.split(':', 1)
    if not rest.startswith('//'):
        raise InvalidCacheBackendError('Backend URI must start with scheme://')
    host = rest[2:]
    qpos = rest.find('?')
    if qpos != -1:
        params = dict(parse_qsl(rest[qpos + 1:]))
        host = rest[2:qpos]
    else:
        params = {}
    if host.endswith('/'):
        host = host[:-1]
    return (scheme, host, params)