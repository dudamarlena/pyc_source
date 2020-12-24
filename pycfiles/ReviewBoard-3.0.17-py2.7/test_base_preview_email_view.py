# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/reviewboard/notifications/tests/test_base_preview_email_view.py
# Compiled at: 2020-02-11 04:03:56
from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.http import Http404
from django.test.client import RequestFactory
from django.test.utils import override_settings
from reviewboard.notifications.email.message import EmailMessage
from reviewboard.notifications.email.views import BasePreviewEmailView
from reviewboard.testing import TestCase

class BasePreviewEmailViewTests(TestCase):
    """Unit tests for BasePreviewEmailView."""

    @override_settings(DEBUG=True)
    def test_get_with_classmethod(self):
        """Testing BasePreviewEmailView.get with build_email as classmethod"""

        class MyPreviewEmailView(BasePreviewEmailView):

            @classmethod
            def build_email(cls, test_var):
                self.assertEqual(test_var, b'test')
                return EmailMessage(subject=b'Test Subject', text_body=b'Test Body')

            def get_email_data(view, request, test_var=None, *args, **kwargs):
                self.assertEqual(test_var, b'test')
                return {b'test_var': test_var}

        request = RequestFactory().request()
        request.user = User.objects.create_user(username=b'test-user', email=b'user@example.com')
        view = MyPreviewEmailView.as_view()
        response = view(request, test_var=b'test', message_format=b'text')
        self.assertEqual(response.status_code, 200)

    @override_settings(DEBUG=True)
    def test_get_with_staticmethod(self):
        """Testing BasePreviewEmailView.get with build_email as staticmethod"""

        class MyPreviewEmailView(BasePreviewEmailView):

            @staticmethod
            def build_email(test_var):
                self.assertEqual(test_var, b'test')
                return EmailMessage(subject=b'Test Subject', text_body=b'Test Body')

            def get_email_data(view, request, test_var=None, *args, **kwargs):
                self.assertEqual(test_var, b'test')
                return {b'test_var': test_var}

        request = RequestFactory().request()
        request.user = User.objects.create_user(username=b'test-user', email=b'user@example.com')
        view = MyPreviewEmailView.as_view()
        response = view(request, test_var=b'test', message_format=b'text')
        self.assertEqual(response.status_code, 200)

    @override_settings(DEBUG=False)
    def test_get_with_debug_false(self):
        """Testing BasePreviewEmailView.get with DEBUG=False"""

        class MyPreviewEmailView(BasePreviewEmailView):

            @classmethod
            def build_email(cls, test_var):
                self.fail(b'build_email should not be reached')
                return EmailMessage(subject=b'Test Subject', text_body=b'Test Body')

            def get_email_data(view, request, test_var=None, *args, **kwargs):
                self.fail(b'get_email_data should not be reached')

        request = RequestFactory().request()
        request.user = User.objects.create_user(username=b'test-user', email=b'user@example.com')
        view = MyPreviewEmailView.as_view()
        with self.assertRaises(Http404):
            view(request, test_var=b'test', message_format=b'text')