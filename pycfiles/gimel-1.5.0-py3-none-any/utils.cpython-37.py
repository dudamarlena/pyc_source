# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ./vendor/redis/utils.py
# Compiled at: 2019-07-06 06:05:05
# Size of source mod 2**32: 666 bytes
from contextlib import contextmanager
try:
    import hiredis
    HIREDIS_AVAILABLE = True
except ImportError:
    HIREDIS_AVAILABLE = False

def from_url(url, db=None, **kwargs):
    """
    Returns an active Redis client generated from the given database URL.

    Will attempt to extract the database id from the path url fragment, if
    none is provided.
    """
    from redis.client import Redis
    return (Redis.from_url)(url, db, **kwargs)


@contextmanager
def pipeline(redis_obj):
    p = redis_obj.pipeline()
    yield p
    p.execute()


class dummy(object):
    __doc__ = '\n    Instances of this class can be used as an attribute container.\n    '