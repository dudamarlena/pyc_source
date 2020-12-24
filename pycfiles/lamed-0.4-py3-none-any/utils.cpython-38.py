# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /private/var/folders/pb/598z8h910dvf2wrvwnbyl_2m0000gn/T/pip-install-03p63p8r/redis/redis/utils.py
# Compiled at: 2020-04-05 04:25:10
# Size of source mod 2**32: 666 bytes
from contextlib import contextmanager
try:
    import hiredis
    HIREDIS_AVAILABLE = True
except ImportError:
    HIREDIS_AVAILABLE = False
else:

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
        (yield p)
        p.execute()


    class dummy(object):
        __doc__ = '\n    Instances of this class can be used as an attribute container.\n    '