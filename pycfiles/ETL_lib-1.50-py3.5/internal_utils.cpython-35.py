# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\ETL\internal_utils.py
# Compiled at: 2020-01-14 18:43:38
# Size of source mod 2**32: 663 bytes
from functools import wraps

def extract_config_from_args(args, kwargs):
    try:
        from .config import Config
        return next(iter(a for a in args + tuple(kwargs.values()) if isinstance(a, Config)))
    except StopIteration as e:
        raise ValueError('The decorated function needs a Config instance object in either args or kwargs') from e


def needs_params(f):

    @wraps(f)
    def _impl(*args, **kwargs):
        config = extract_config_from_args(args, kwargs)
        if config.with_limited_features:
            from exceptions import NoTablesDefinedException
            raise NoTablesDefinedException(f)
        return f(*args, **kwargs)

    return _impl