# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/michael/Projects/dj-rest-auth/dj_rest_auth/utils.py
# Compiled at: 2020-03-22 07:38:27
# Size of source mod 2**32: 1842 bytes
from importlib import import_module

def import_callable(path_or_callable):
    if hasattr(path_or_callable, '__call__'):
        return path_or_callable
    assert isinstance(path_or_callable, str)
    package, attr = path_or_callable.rsplit('.', 1)
    return getattr(import_module(package), attr)


def default_create_token(token_model, user, serializer):
    token, _ = token_model.objects.get_or_create(user=user)
    return token


def jwt_encode(user):
    try:
        from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
    except ImportError:
        raise ImportError('rest-framework-simplejwt needs to be installed')
    else:
        refresh = TokenObtainPairSerializer.get_token(user)
        return (refresh.access_token, refresh)


try:
    from rest_framework_simplejwt.authentication import JWTAuthentication

    class JWTCookieAuthentication(JWTAuthentication):
        __doc__ = '\n        An authentication plugin that hopefully authenticates requests through a JSON web\n        token provided in a request cookie (and through the header as normal, with a\n        preference to the header).\n        '

        def authenticate(self, request):
            from django.conf import settings
            cookie_name = getattr(settings, 'JWT_AUTH_COOKIE', None)
            header = self.get_header(request)
            if header is None:
                if cookie_name:
                    raw_token = request.COOKIES.get(cookie_name)
                else:
                    return
            else:
                raw_token = self.get_raw_token(header)
            if raw_token is None:
                return
            validated_token = self.get_validated_token(raw_token)
            return (self.get_user(validated_token), validated_token)


except ImportError:
    pass