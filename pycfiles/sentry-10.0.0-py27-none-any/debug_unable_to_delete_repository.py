# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/src/sentry/src/sentry/web/frontend/debug/debug_unable_to_delete_repository.py
# Compiled at: 2019-08-16 17:27:46
from __future__ import absolute_import, print_function
import types
from django.views.generic import View
from sentry.models import Repository
from sentry.plugins.providers.dummy import DummyRepositoryProvider
from .mail import MailPreview

class DebugUnableToDeleteRepository(View):

    def get(self, request):

        def mock_get_provider(self):
            return DummyRepositoryProvider('dummy')

        repo = Repository(name='getsentry/sentry', provider='dummy')
        repo.get_provider = types.MethodType(mock_get_provider, repo)
        email = repo.generate_delete_fail_email('An internal server error occurred')
        return MailPreview(html_template=email.html_template, text_template=email.template, context=email.context).render(request)