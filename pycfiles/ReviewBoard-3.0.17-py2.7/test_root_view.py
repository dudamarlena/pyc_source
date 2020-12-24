# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/reviewboard/reviews/tests/test_root_view.py
# Compiled at: 2020-02-11 04:03:56
"""Unit tests for reviewboard.reviews.views.RootView."""
from __future__ import unicode_literals
from djblets.testing.decorators import add_fixtures
from reviewboard.site.urlresolvers import local_site_reverse
from reviewboard.testing import TestCase

class RootViewTests(TestCase):
    """Unit tests for reviewboard.reviews.views.RootView."""
    fixtures = [
     b'test_users']

    def test_with_anonymous_with_private_access(self):
        """Testing RootView with anonymous user with anonymous access not
        allowed
        """
        with self.siteconfig_settings({b'auth_require_sitewide_login': True}, reload_settings=False):
            response = self.client.get(local_site_reverse(b'root'))
        self.assertRedirects(response, b'/account/login/?next=/')

    def test_with_anonymous_with_public_access(self):
        """Testing RootView with anonymous user with anonymous access allowed
        """
        response = self.client.get(local_site_reverse(b'root'))
        self.assertRedirects(response, b'/r/')

    def test_with_logged_in(self):
        """Testing RootView with authenticated user"""
        self.assertTrue(self.client.login(username=b'doc', password=b'doc'))
        response = self.client.get(local_site_reverse(b'root'))
        self.assertRedirects(response, b'/dashboard/')

    @add_fixtures([b'test_site'])
    def test_with_anonymous_with_local_site_private(self):
        """Testing RootView with anonymous user with private Local Site"""
        response = self.client.get(local_site_reverse(b'root', local_site_name=self.local_site_name))
        self.assertRedirects(response, b'/account/login/?next=/s/%s/' % self.local_site_name)

    @add_fixtures([b'test_site'])
    def test_with_anonymous_with_local_site_public(self):
        """Testing RootView with anonymous user with public Local Site"""
        local_site = self.get_local_site(name=self.local_site_name)
        local_site.public = True
        local_site.save()
        response = self.client.get(local_site_reverse(b'root', local_site=local_site))
        self.assertRedirects(response, b'/s/%s/r/' % self.local_site_name)

    @add_fixtures([b'test_site'])
    def test_with_logged_in_with_local_site(self):
        """Testing RootView with authenticated user with Local Site"""
        self.assertTrue(self.client.login(username=b'doc', password=b'doc'))
        response = self.client.get(local_site_reverse(b'root', local_site_name=self.local_site_name))
        self.assertRedirects(response, b'/s/%s/dashboard/' % self.local_site_name)