# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/reviewboard/accounts/tests/test_privacy_form.py
# Compiled at: 2020-02-11 04:03:56
"""Unit tests for reviewboard.accounts.forms.pages.PrivacyForm."""
from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.test.client import RequestFactory
from reviewboard.accounts.forms.pages import PrivacyForm
from reviewboard.accounts.pages import PrivacyPage
from reviewboard.accounts.views import MyAccountView
from reviewboard.testing import TestCase

class PrivacyFormTests(TestCase):
    """Unit tests for reviewboard.accounts.forms.pages.PrivacyForm."""

    def setUp(self):
        super(PrivacyFormTests, self).setUp()
        self.user = User.objects.create(username=b'test-user')
        self.request = RequestFactory().get(b'/account/preferences/')
        self.request.user = self.user
        self.page = PrivacyPage(config_view=MyAccountView(), request=self.request, user=self.user)

    def test_init_with_privacy_enable_user_consent_true(self):
        """Testing PrivacyForm with privacy_enable_user_consent=True"""
        with self.siteconfig_settings({b'privacy_enable_user_consent': True}):
            form = PrivacyForm(page=self.page, request=self.request, user=self.user)
            self.assertIn(b'consent', form.fields)
            self.assertEqual(form.save_label, b'Save')

    def test_init_with_privacy_enable_user_consent_false(self):
        """Testing PrivacyForm with privacy_enable_user_consent=False"""
        with self.siteconfig_settings({b'privacy_enable_user_consent': False}):
            form = PrivacyForm(page=self.page, request=self.request, user=self.user)
            self.assertNotIn(b'consent', form.fields)
            self.assertIsNone(form.save_label)

    def test_is_visible_with_no_privacy(self):
        """Testing PrivacyForm.is_visible with no privacy details"""
        settings = {b'privacy_enable_user_consent': False, 
           b'privacy_info_html': b''}
        with self.siteconfig_settings(settings):
            form = PrivacyForm(page=self.page, request=self.request, user=self.user)
            self.assertFalse(form.is_visible())

    def test_is_visible_with_consent(self):
        """Testing PrivacyForm.is_visible with consent option enabled"""
        settings = {b'privacy_enable_user_consent': True, 
           b'privacy_info_html': b''}
        with self.siteconfig_settings(settings):
            form = PrivacyForm(page=self.page, request=self.request, user=self.user)
            self.assertTrue(form.is_visible())

    def test_is_visible_with_privacy_info(self):
        """Testing PrivacyForm.is_visible with privacy_info_html set"""
        settings = {b'privacy_enable_user_consent': False, 
           b'privacy_info_html': b'Test.'}
        with self.siteconfig_settings(settings):
            form = PrivacyForm(page=self.page, request=self.request, user=self.user)
            self.assertTrue(form.is_visible())