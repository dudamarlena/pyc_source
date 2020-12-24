# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/authorize_middleware/errors.py
# Compiled at: 2009-10-17 15:11:18
from paste import httpexceptions

class NotAuthenticatedError(httpexceptions.HTTPClientError):
    """
    Raised when a permission check fails because the user is not authenticated.

    The exception is caught by the ``httpexceptions`` middleware and converted into
    a ``401`` HTTP response which is intercepted by the authentication middleware
    triggering a sign in.
    """
    required_headers = ()
    code = 401
    title = 'Not Authenticated'


class NotAuthorizedError(httpexceptions.HTTPClientError):
    """
    Raised when a permission check fails because the user is not authorized.

    The exception is caught by the ``httpexceptions`` middleware and converted into
    a ``403`` HTTP response which is intercepted by the authentication middleware
    triggering a sign in.
    """
    code = 403
    title = 'Forbidden'
    explanation = 'Access was denied to this resource.'