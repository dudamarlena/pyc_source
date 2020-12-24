# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/chris/workspace/slothauth/slothauth/middleware.py
# Compiled at: 2016-03-10 18:18:24
from django.contrib.auth import authenticate, login
from django.contrib.auth import get_user_model
from . import settings
Account = get_user_model()

class PasswordlessUserMiddleware(object):

    def process_request(self, request):
        passwordless_key = request.GET.get(settings.PASSWORDLESS_GET_PARAM, None)
        if passwordless_key and not passwordless_key == '':
            user = authenticate(passwordless_key=passwordless_key, force=True)
            if user and user.is_active:
                login(request, user)
        return


class OneTimeAuthenticationKeyMiddleware(object):

    def process_request(self, request):
        one_time_authentication_key = request.GET.get(settings.ONE_TIME_AUTHENTICATION_KEY_GET_PARAM, None)
        if one_time_authentication_key and not one_time_authentication_key == '':
            user = authenticate(one_time_authentication_key=one_time_authentication_key)
            if user and user.is_active:
                login(request, user)
        return


class ImpersonateMiddleware(object):

    def process_request(self, request):
        impersonating = None
        if hasattr(request.user, 'can_impersonate') and request.user.can_impersonate and '__impersonate' in request.GET:
            request.session['impersonate_id'] = int(request.GET['__impersonate'])
        elif '__unimpersonate' in request.GET and 'impersonate_id' in request.session:
            del request.session['impersonate_id']
            impersonating = request.user
        if hasattr(request.user, 'can_impersonate') and request.user.can_impersonate and 'impersonate_id' in request.session:
            request.user = Account.objects.get(id=request.session['impersonate_id'])
            impersonating = request.user
        request.impersonating = impersonating
        return