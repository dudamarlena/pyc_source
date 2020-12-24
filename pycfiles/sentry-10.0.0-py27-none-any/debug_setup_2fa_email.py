# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/src/sentry/src/sentry/web/frontend/debug/debug_setup_2fa_email.py
# Compiled at: 2019-08-16 17:27:46
from __future__ import absolute_import
from django.views.generic import View
from .mail import MailPreview
from sentry.models import Organization, OrganizationMember

class DebugSetup2faEmailView(View):

    def get(self, request):
        org = Organization(id=1, slug='organization', name='sentry corp')
        member = OrganizationMember(id=1, organization=org, email='test@gmail.com')
        context = {'url': member.get_invite_link(), 'organization': org}
        return MailPreview(html_template='sentry/emails/setup_2fa.html', text_template='sentry/emails/setup_2fa.txt', context=context).render(request)