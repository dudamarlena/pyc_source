# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ali/ownCloud/Project/python/django-aparnik-framework-project/testandbuildprojectframework/aparnik/middlewares/token_auth.py
# Compiled at: 2020-03-03 06:09:02
# Size of source mod 2**32: 3775 bytes
import django
import django.utils.translation as _
import rest_framework.authtoken.models, rest_framework.exceptions
from rest_framework_jwt.serializers import VerifyJSONWebTokenSerializer
from urllib import parse
from channels.auth import AuthMiddlewareStack

class TokenAuthMiddleware:
    __doc__ = "Token authorization middleware for Channels.\n\n    Authenticate the connection by the header 'Authorization: Token...'\n    using Django REST framework token-based authentication.\n    "

    def __init__(self, inner):
        """Save given inner middleware to invoke in the `__call__`."""
        self._inner = inner

    def __call__(self, scope):
        """Add user to the scope by 'Authorization: Token...' header."""
        headers = dict(scope['headers'])
        if b'authorization' not in headers:
            query_string = parse.parse_qs(scope['query_string'].decode('utf-8', 'replace'))
            if 'token' in query_string:
                if query_string['token'][0]:
                    split_token = query_string['token'][0].split()
                    if not split_token or len(split_token) != 2:
                        return self._inner(scope)
                    data = {'token': split_token[1]}
                    valid_data = VerifyJSONWebTokenSerializer().validate(data)
                    user = valid_data['user']
                    return self._inner(dict(scope, user=user))
            return self._inner(scope)
        auth_header = headers[b'authorization'].split()
        if not auth_header or len(auth_header) != 2:
            return self._inner(scope)
        data = {'token': auth_header[1]}
        valid_data = VerifyJSONWebTokenSerializer().validate(data)
        user = valid_data['user']
        return self._inner(dict(scope, user=user))


TokenAuthMiddlewareStack = lambda inner: TokenAuthMiddleware(AuthMiddlewareStack(inner))