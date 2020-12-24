# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/cleber/.pyenv/versions/3.6.2/lib/python3.6/site-packages/powerlibs/django/restless/auth.py
# Compiled at: 2017-04-19 16:07:32
# Size of source mod 2**32: 3770 bytes
from django.contrib import auth
from django.utils.encoding import DjangoUnicodeDecodeError
import base64
try:
    from django.utils.encoding import smart_text
except ImportError:
    from django.utils.encoding import smart_unicode as smart_text

from .views import Endpoint
from .http import Http200, Http401, Http403
from .models import serialize
__all__ = ['UsernamePasswordAuthMixin', 'BasicHttpAuthMixin',
 'AuthenticateEndpoint', 'login_required']

class UsernamePasswordAuthMixin(object):
    __doc__ = '\n    :py:class:`restless.views.Endpoint` mixin providing user authentication\n    based on username and password (as specified in "username" and "password"\n    request GET params).\n    '

    def authenticate(self, request):
        if request.method == 'POST':
            self.username = request.data.get('username')
            self.password = request.data.get('password')
        else:
            self.username = request.params.get('username')
            self.password = request.params.get('password')
        user = auth.authenticate(username=(self.username), password=(self.password))
        if user is not None:
            if user.is_active:
                auth.login(request, user)


class BasicHttpAuthMixin(object):
    __doc__ = '\n    :py:class:`restless.views.Endpoint` mixin providing user authentication\n    based on HTTP Basic authentication.\n    '

    def authenticate(self, request):
        if 'HTTP_AUTHORIZATION' in request.META:
            authdata = request.META['HTTP_AUTHORIZATION'].split()
            if len(authdata) == 2:
                if authdata[0].lower() == 'basic':
                    try:
                        raw = authdata[1].encode('ascii')
                        auth_parts = base64.b64decode(raw).split(b':')
                    except:
                        return

                    try:
                        uname, passwd = smart_text(auth_parts[0]), smart_text(auth_parts[1])
                    except DjangoUnicodeDecodeError:
                        return
                    else:
                        user = auth.authenticate(username=uname, password=passwd)
                        if user is not None:
                            if user.is_active:
                                request.user = user


def login_required(fn):
    """
    Decorator for :py:class:`restless.views.Endpoint` methods to require
    authenticated, active user. If the user isn't authenticated, HTTP 403 is
    returned immediately (HTTP 401 if Basic HTTP authentication is used).
    """

    def wrapper(self, request, *args, **kwargs):
        if request.user is None or not request.user.is_active:
            if isinstance(self, BasicHttpAuthMixin):
                return Http401()
            return Http403('forbidden')
        else:
            return fn(self, request, *args, **kwargs)

    wrapper.__name__ = fn.__name__
    wrapper.__doc__ = fn.__doc__
    return wrapper


class AuthenticateEndpoint(Endpoint, UsernamePasswordAuthMixin):
    __doc__ = '\n    Session-based authentication API endpoint. Provides a GET method for\n    authenticating the user based on passed-in "username" and "password"\n    request params. On successful authentication, the method returns\n    authenticated user details.\n\n    Uses :py:class:`UsernamePasswordAuthMixin` to actually implement the\n    Authentication API endpoint.\n\n    On success, the user will get a response with their serialized User\n    object, containing id, username, first_name, last_name and email fields.\n    '
    user_fields = ('id', 'username', 'first_name', 'last_name', 'email')

    @login_required
    def get(self, request):
        return Http200(serialize((request.user), fields=(self.user_fields)))