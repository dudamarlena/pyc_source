# uncompyle6 version 3.7.4
# Python bytecode 3.3 (3230)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/tomchristie/GitHub/api-star/api_star/authentication.py
# Compiled at: 2016-04-14 11:45:08
# Size of source mod 2**32: 2264 bytes
from api_star.compat import Base64DecodeError
from api_star.exceptions import Unauthorized
import base64

def basic_auth(lookup_username):
    """
    HTTP Basic Authentication.

    `lookup_username` - A `function(username, password)` that returns a
                        user instance of some kind, or `None`.
    """
    errors = {'invalid-header': 'Invalid basic authorization header.', 
     'incorrect-credentials': 'Incorrect username or password.'}

    def authenticator(request):
        header = request.headers.get('Authorization', '').split()
        if not header or header[0].lower() != b'basic':
            return
        else:
            if len(header) != 2:
                raise Unauthorized(errors['invalid-header'])
            try:
                decoded = base64.b64decode(header[1]).decode('iso-8859-1')
            except Base64DecodeError:
                raise Unauthorized(errors['invalid-header'])

            username, delimiter, password = decoded.partition(':')
            if not delimiter:
                raise Unauthorized(errors['invalid-header'])
            auth = lookup_username(username=username, password=password)
            if auth is None:
                raise Unauthorized(errors['incorrect-credentials'])
            return auth

    return authenticator


def token_auth(lookup_token):
    """
    A simple token-based authentication scheme.

    `lookup_token` - A `function(token)` that returns a user instance of some
                     kind, or `None`.
    """
    errors = {'invalid-header': 'Invalid token authorization header.', 
     'incorrect-credentials': 'Incorrect token.'}

    def authenticator(request):
        header = request.headers.get('Authorization', '').split()
        if not header or header[0].lower() != b'token':
            return
        else:
            if len(header) != 2:
                raise Unauthorized(errors['invalid-header'])
            token = header[1].decode('iso-8859-1')
            auth = lookup_token(token)
            if auth is None:
                raise Unauthorized(errors['incorrect-credentials'])
            return auth

    return authenticator