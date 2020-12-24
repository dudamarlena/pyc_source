# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/src/sentry/src/sentry/web/frontend/auth_provider_login.py
# Compiled at: 2019-08-16 17:27:46
from __future__ import absolute_import, print_function
from django.core.urlresolvers import reverse
from sentry.auth.helper import AuthHelper
from sentry.web.frontend.base import BaseView

class AuthProviderLoginView(BaseView):
    auth_required = False

    def handle(self, request):
        helper = AuthHelper.get_for_request(request)
        if helper is None:
            return self.redirect(reverse('sentry-login'))
        else:
            if not helper.pipeline_is_valid():
                return helper.error('Something unexpected happened during authentication.')
            return helper.current_step()