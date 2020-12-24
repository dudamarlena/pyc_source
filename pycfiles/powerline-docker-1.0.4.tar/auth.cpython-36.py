# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
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
    """UsernamePasswordAuthMixin"""

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
    """BasicHttpAuthMixin"""

    def authenticate(self, request):
        if 'HTTP_AUTHORIZATION' in request.META:
            authdata = request.META['HTTP_AUTHORIZATION'].split()
            if len(authdata) == 2:
                if authdata[0].lower() == 'basic':
                    try:
                        raw = authdata[1].encode('ascii')
                        auth_parts = base64.b64decode(raw).split(':')
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
    """AuthenticateEndpoint"""
    user_fields = ('id', 'username', 'first_name', 'last_name', 'email')

    @login_required
    def get(self, request):
        return Http200(serialize((request.user), fields=(self.user_fields)))