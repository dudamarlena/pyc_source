# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/src/sentry/src/sentry/web/frontend/debug/debug_invalid_identity_email.py
# Compiled at: 2019-08-16 17:27:46
from __future__ import absolute_import, print_function
from django.views.generic import View
from social_auth.models import UserSocialAuth
from sentry.tasks.commits import generate_invalid_identity_email
from .mail import MailPreview

class DebugInvalidIdentityEmailView(View):

    def get(self, request):
        identity = UserSocialAuth(user=request.user, provider='dummy')
        email = generate_invalid_identity_email(identity=identity)
        return MailPreview(html_template=email.html_template, text_template=email.template, context=email.context).render(request)