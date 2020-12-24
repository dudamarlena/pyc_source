# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/api/auth/backend/default.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 1207 bytes
__doc__ = 'Default authentication backend - everything is allowed'
from functools import wraps
CLIENT_AUTH = None

def init_app(_):
    """Initializes authentication backend"""
    pass


def requires_authentication(function):
    """Decorator for functions that require authentication"""

    @wraps(function)
    def decorated(*args, **kwargs):
        return function(*args, **kwargs)

    return decorated