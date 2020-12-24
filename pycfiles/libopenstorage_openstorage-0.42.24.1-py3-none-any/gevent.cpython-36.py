# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-build-ed191__6/grpcio/grpc/experimental/gevent.py
# Compiled at: 2020-01-10 16:25:22
# Size of source mod 2**32: 973 bytes
"""gRPC's Python gEvent APIs."""
from grpc._cython import cygrpc as _cygrpc

def init_gevent():
    """Patches gRPC's libraries to be compatible with gevent.

    This must be called AFTER the python standard lib has been patched,
    but BEFORE creating and gRPC objects.

    In order for progress to be made, the application must drive the event loop.
    """
    _cygrpc.init_grpc_gevent()