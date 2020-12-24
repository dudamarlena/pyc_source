# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/src/sentry/src/sentry/web/frontend/reactivate_account.py
# Compiled at: 2019-08-16 17:27:46
from __future__ import absolute_import
from django.db import transaction
from django.views.decorators.cache import never_cache
from sentry.web.frontend.base import BaseView
from sentry.utils import auth

class ReactivateAccountView(BaseView):
    auth_required = False

    @never_cache
    @transaction.atomic
    def handle(self, request):
        if not request.user.is_authenticated():
            return self.handle_auth_required(request)
        if request.POST.get('op') == 'confirm':
            request.user.update(is_active=True)
            return self.redirect(auth.get_login_redirect(request))
        context = {}
        return self.respond('sentry/reactivate-account.html', context)