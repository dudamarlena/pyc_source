# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/reviewboard/reviews/tests/test_bug_url_redirect_view.py
# Compiled at: 2020-02-11 04:03:56
"""Unit tests for reviewboard.reviews.views.BugURLRedirectView."""
from __future__ import unicode_literals
from django.core.urlresolvers import reverse
from reviewboard.testing import TestCase

class BugURLRedirectViewTests(TestCase):
    """Unit tests for reviewboard.reviews.views.BugURLRedirectView."""
    fixtures = [
     b'test_users', b'test_scmtools']

    def test_with_custom_scheme(self):
        """Testing BugURLRedirectView with non-HTTP scheme loads correctly"""
        repository = self.create_repository(public=True, bug_tracker=b'scheme://bugid=%s')
        review_request = self.create_review_request(repository=repository, publish=True)
        url = reverse(b'bug_url', args=(review_request.pk, b'1'))
        response = self.client.get(url)
        self.assertEqual(response[b'Location'], b'scheme://bugid=1')