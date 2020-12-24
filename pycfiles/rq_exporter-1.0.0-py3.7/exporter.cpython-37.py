# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/rq_exporter/exporter.py
# Compiled at: 2020-04-23 04:20:06
# Size of source mod 2**32: 860 bytes
"""
RQ exporter module.

Register the RQ collector and create the WSGI application instance.

"""
from prometheus_client import make_wsgi_app
from prometheus_client.core import REGISTRY
from .collector import RQCollector
from .utils import get_redis_connection

def register_collector():
    """Register the RQ collector instance.

    Raises:
        IOError: From `get_redis_connection` if there was an error opening
            the password file.
        redis.exceptions.RedisError: On Redis connection errors.

    """
    REGISTRY.register(RQCollector(get_redis_connection()))


def create_app():
    """Create a WSGI application.

    Returns:
        function: WSGI application function.

    """
    register_collector()
    return make_wsgi_app()