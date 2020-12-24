# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\django_auth_pubtkt\middleware.py
# Compiled at: 2018-03-10 14:38:40
from django.contrib.auth.models import User, Group, AnonymousUser
from django.conf import settings
import urllib, six
from django.utils.deprecation import MiddlewareMixin
from .auth_pubtkt import Authpubtkt

class DjangoAuthPubtkt(MiddlewareMixin):
    """ Django middleware for mod_auth_pubtkt SSO """

    def __init__(self, get_response=None):
        super(DjangoAuthPubtkt, self).__init__(get_response)
        try:
            self.authpubtkt = Authpubtkt(settings.TKT_AUTH_PUBLIC_KEY)
        except AttributeError:
            raise AttributeError('[django-auth-pubtkt] Please specify TKT_AUTH_PUBLIC_KEY in settings.py')

        self.TKT_AUTH_COOKIE_NAME = getattr(settings, 'TKT_AUTH_COOKIE_NAME', 'auth_pubtkt')
        self.TKT_AUTH_USE_GROUPS = getattr(settings, 'TKT_AUTH_USE_GROUPS', False)
        self.TKT_AUTH_ANONYMOUS_USER = getattr(settings, 'TKT_AUTH_ANONYMOUS_USER', True)

    def add_user_to_group(self, user, group_name):
        """ Add user to a group
        """
        group, _ = Group.objects.get_or_create(name=group_name)
        group.user_set.add(user)

    def process_request(self, request):
        cookie = request.COOKIES.get(self.TKT_AUTH_COOKIE_NAME, None)
        if self.TKT_AUTH_ANONYMOUS_USER:
            request.user = AnonymousUser()
        if cookie is None:
            return
        else:
            if six.PY2:
                cookie = urllib.unquote(cookie)
            else:
                cookie = urllib.parse.unquote(cookie)
            params = self.authpubtkt.verify_cookie(cookie)
            if params is not None:
                username = params['uid']
                user, _ = User.objects.get_or_create(username=username)
                request.user = user
                if self.TKT_AUTH_USE_GROUPS:
                    user.groups.clear()
                    for token in params['tokens'].split(','):
                        self.add_user_to_group(user, token)

            return