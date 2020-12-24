# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/api/auth/backend/deny_all.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 1289 bytes
"""Authentication backend that denies all requests"""
from functools import wraps
from flask import Response
CLIENT_AUTH = None

def init_app(_):
    """Initializes authentication"""
    pass


def requires_authentication(function):
    """Decorator for functions that require authentication"""

    @wraps(function)
    def decorated(*args, **kwargs):
        return Response('Forbidden', 403)

    return decorated