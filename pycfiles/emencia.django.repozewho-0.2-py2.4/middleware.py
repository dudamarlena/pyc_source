# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/emencia/django/repozewho/middleware.py
# Compiled at: 2009-06-12 12:31:56
from django.contrib.auth.models import AnonymousUser
from django.contrib.auth.models import User
from django.conf import settings

class AuthMiddleware(object):
    __module__ = __name__

    def process_request(self, request):
        if request.environ.get('repoze.who.identity') is not None:
            repoze_who_user = None
            identity = request.environ['repoze.who.identity']
            if identity is not None:
                repoze_who_user = identity['repoze.who.userid']
            if repoze_who_user is not None:
                user = User.objects.get(**{settings.LOGIN_FIELD: repoze_who_user})
                request.user = user
        return