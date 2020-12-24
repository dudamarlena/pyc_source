# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/authorize_middleware/auth.py
# Compiled at: 2009-10-17 15:11:18
from errors import *

def authorize_request(environ, function=None):
    """
    This function can be used within a controller action to ensure that no code 
    after the function call is executed if the user doesn't pass the permission
    check in function ``function``.
    """
    if 'REMOTE_USER' not in environ:
        raise NotAuthenticatedError('Not Authenticated')
    elif function is not None and not function(environ):
        raise NotAuthorizedError('Not Authorized')
    return