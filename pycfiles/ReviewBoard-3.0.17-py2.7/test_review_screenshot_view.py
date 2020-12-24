# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/reviewboard/reviews/tests/test_review_screenshot_view.py
# Compiled at: 2020-02-11 04:03:56
"""Unit tests for reviewboard.reviews.views.ReviewScreenshotView."""
from __future__ import unicode_literals
from reviewboard.site.urlresolvers import local_site_reverse
from reviewboard.testing import TestCase

class ReviewScreenshotViewTests(TestCase):
    """Unit tests for reviewboard.reviews.views.ReviewScreenshotView."""
    fixtures = [
     b'test_users']

    def test_access_with_valid_id(self):
        """Testing ReviewScreenshotView access with valid screenshot for review
        request
        """
        review_request = self.create_review_request(publish=True)
        screenshot = self.create_screenshot(review_request)
        response = self.client.get(local_site_reverse(b'screenshot', kwargs={b'review_request_id': review_request.pk, 
           b'screenshot_id': screenshot.pk}))
        self.assertEqual(response.status_code, 200)

    def test_access_with_valid_id_and_draft(self):
        """Testing ReviewScreenshotView access with valid screenshot for review
        request draft
        """
        review_request = self.create_review_request(publish=True)
        screenshot = self.create_screenshot(review_request, draft=True)
        username = review_request.submitter.username
        self.client.login(username=username, password=username)
        response = self.client.get(local_site_reverse(b'screenshot', kwargs={b'review_request_id': review_request.pk, 
           b'screenshot_id': screenshot.pk}))
        self.assertEqual(response.status_code, 200)

    def test_access_with_valid_inactive_id(self):
        """Testing ReviewScreenshotView access with valid inactive screenshot
        for review request
        """
        review_request = self.create_review_request(publish=True)
        screenshot = self.create_screenshot(review_request, active=False)
        response = self.client.get(local_site_reverse(b'screenshot', kwargs={b'review_request_id': review_request.pk, 
           b'screenshot_id': screenshot.pk}))
        self.assertEqual(response.status_code, 200)

    def test_access_with_valid_inactive_id_and_draft(self):
        """Testing ReviewScreenshotView access with valid inactive screenshot
        for review request draft
        """
        review_request = self.create_review_request(publish=True)
        screenshot = self.create_screenshot(review_request, draft=True, active=False)
        username = review_request.submitter.username
        self.client.login(username=username, password=username)
        response = self.client.get(local_site_reverse(b'screenshot', kwargs={b'review_request_id': review_request.pk, 
           b'screenshot_id': screenshot.pk}))
        self.assertEqual(response.status_code, 200)

    def test_access_with_invalid_id(self):
        """Testing ReviewScreenshotView access with invalid screenshot for
        review request
        """
        review_request = self.create_review_request(publish=True)
        screenshot = self.create_screenshot(review_request)
        review_request2 = self.create_review_request(publish=True)
        response = self.client.get(local_site_reverse(b'screenshot', kwargs={b'review_request_id': review_request2.pk, 
           b'screenshot_id': screenshot.pk}))
        self.assertEqual(response.status_code, 404)

    def test_access_with_invalid_id_and_draft(self):
        """Testing ReviewScreenshotView access with invalid screenshot for
        review request draft
        """
        review_request = self.create_review_request(publish=True)
        screenshot = self.create_screenshot(review_request, draft=True)
        review_request2 = self.create_review_request(publish=True)
        username = review_request.submitter.username
        self.client.login(username=username, password=username)
        response = self.client.get(local_site_reverse(b'screenshot', kwargs={b'review_request_id': review_request2.pk, 
           b'screenshot_id': screenshot.pk}))
        self.assertEqual(response.status_code, 404)

    def test_access_with_invalid_inactive_id(self):
        """Testing ReviewScreenshotView access with invalid inactive screenshot
        for review request
        """
        review_request = self.create_review_request(publish=True)
        screenshot = self.create_screenshot(review_request, active=False)
        review_request2 = self.create_review_request(publish=True)
        response = self.client.get(local_site_reverse(b'screenshot', kwargs={b'review_request_id': review_request2.pk, 
           b'screenshot_id': screenshot.pk}))
        self.assertEqual(response.status_code, 404)

    def test_access_with_invalid_inactive_id_and_draft(self):
        """Testing ReviewScreenshotView access with invalid inactive screenshot
        for review request draft
        """
        review_request = self.create_review_request(publish=True)
        screenshot = self.create_screenshot(review_request, draft=True, active=False)
        review_request2 = self.create_review_request(publish=True)
        username = review_request.submitter.username
        self.client.login(username=username, password=username)
        response = self.client.get(local_site_reverse(b'screenshot', kwargs={b'review_request_id': review_request2.pk, 
           b'screenshot_id': screenshot.pk}))
        self.assertEqual(response.status_code, 404)