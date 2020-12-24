# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/src/sentry/src/sentry/web/frontend/debug/debug_auth_views.py
# Compiled at: 2019-08-16 17:27:46
from __future__ import absolute_import
from django.views.generic import View
from sentry.models import User
from sentry.web.helpers import render_to_response

class DebugAuthConfirmIdentity(View):

    def get(self, request):
        auth_identity = {'id': 'bar@example.com', 'email': 'bar@example.com'}
        return render_to_response('sentry/auth-confirm-identity.html', {'existing_user': User(email='foo@example.com'), 
           'identity': auth_identity, 
           'login_form': None, 
           'request': request, 
           'identity_display_name': auth_identity['email'], 
           'identity_identifier': auth_identity['id']})


class DebugAuthConfirmLink(View):

    def get(self, request):
        auth_identity = {'id': 'bar@example.com', 'email': 'bar@example.com'}
        return render_to_response('sentry/auth-confirm-link.html', {'existing_user': User(email='foo@example.com'), 
           'identity': auth_identity, 
           'request': request, 
           'identity_display_name': auth_identity['email'], 
           'identity_identifier': auth_identity['id']})