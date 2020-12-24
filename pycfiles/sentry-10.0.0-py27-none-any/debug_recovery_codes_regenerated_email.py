# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/src/sentry/src/sentry/web/frontend/debug/debug_recovery_codes_regenerated_email.py
# Compiled at: 2019-08-16 17:27:46
from __future__ import absolute_import, print_function
import datetime
from django.views.generic import View
from sentry.models import Authenticator
from sentry.security.emails import generate_security_email
from .mail import MailPreview

class DebugRecoveryCodesRegeneratedEmailView(View):

    def get(self, request):
        authenticator = Authenticator(id=0, type=3, user=request.user)
        email = generate_security_email(account=request.user, actor=request.user, type='recovery-codes-regenerated', ip_address=request.META['REMOTE_ADDR'], context={'authenticator': authenticator}, current_datetime=datetime.datetime(2017, 1, 20, 21, 39, 23, 30723))
        return MailPreview(html_template=email.html_template, text_template=email.template, context=email.context).render(request)