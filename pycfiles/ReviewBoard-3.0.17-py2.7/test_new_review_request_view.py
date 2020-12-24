# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/reviewboard/reviews/tests/test_new_review_request_view.py
# Compiled at: 2020-02-11 04:03:56
"""Unit tests for reviewboard.reviews.views.NewReviewRequestView."""
from __future__ import unicode_literals
from djblets.siteconfig.models import SiteConfiguration
from reviewboard.testing import TestCase

class NewReviewRequestViewTests(TestCase):
    """Unit tests for reviewboard.reviews.views.NewReviewRequestView."""
    fixtures = [
     b'test_users']

    def test_get(self):
        """Testing NewReviewRequestView.get"""
        with self.siteconfig_settings({b'auth_require_sitewide_login': False}, reload_settings=False):
            response = self.client.get(b'/r/new')
            self.assertEqual(response.status_code, 301)
            response = self.client.get(b'/r/new/')
            self.assertEqual(response.status_code, 302)
            self.client.login(username=b'grumpy', password=b'grumpy')
        self.client.login(username=b'grumpy', password=b'grumpy')
        response = self.client.get(b'/r/new/')
        self.assertEqual(response.status_code, 200)