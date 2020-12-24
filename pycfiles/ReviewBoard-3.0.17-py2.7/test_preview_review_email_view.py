# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/reviewboard/reviews/tests/test_preview_review_email_view.py
# Compiled at: 2020-02-11 04:03:56
"""Unit tests for reviewboard.reviews.views.PreviewReviewEmailView."""
from __future__ import unicode_literals
from reviewboard.site.urlresolvers import local_site_reverse
from reviewboard.testing import TestCase

class PreviewReviewEmailViewTests(TestCase):
    """Unit tests for reviewboard.reviews.views.PreviewReviewEmailView."""
    fixtures = [
     b'test_users', b'test_scmtools']

    def test_access_with_debug(self):
        """Testing PreviewReviewEmailView access with DEBUG=True"""
        review_request = self.create_review_request(publish=True)
        review = self.create_review(review_request, publish=True)
        with self.settings(DEBUG=True):
            response = self.client.get(local_site_reverse(b'preview-review-email', kwargs={b'review_request_id': review_request.pk, 
               b'review_id': review.pk, 
               b'message_format': b'text'}))
        self.assertEqual(response.status_code, 200)

    def test_access_without_debug(self):
        """Testing PreviewReviewEmailView access with DEBUG=False"""
        review_request = self.create_review_request(publish=True)
        review = self.create_review(review_request, publish=True)
        with self.settings(DEBUG=False):
            response = self.client.get(local_site_reverse(b'preview-review-email', kwargs={b'review_request_id': review_request.pk, 
               b'review_id': review.pk, 
               b'message_format': b'text'}))
        self.assertEqual(response.status_code, 404)

    def test_reply_access_with_debug(self):
        """Testing PreviewReviewEmailView with reply access and DEBUG=True"""
        review_request = self.create_review_request(publish=True)
        review = self.create_review(review_request, publish=True)
        reply = self.create_reply(review, publish=True)
        with self.settings(DEBUG=True):
            response = self.client.get(local_site_reverse(b'preview-review-reply-email', kwargs={b'review_request_id': review_request.pk, 
               b'review_id': review.pk, 
               b'reply_id': reply.pk, 
               b'message_format': b'text'}))
        self.assertEqual(response.status_code, 200)

    def test_reply_access_without_debug(self):
        """Testing PreviewReviewEmailView with reply access and DEBUG=False"""
        review_request = self.create_review_request(publish=True)
        review = self.create_review(review_request, publish=True)
        reply = self.create_reply(review, publish=True)
        with self.settings(DEBUG=False):
            response = self.client.get(local_site_reverse(b'preview-review-reply-email', kwargs={b'review_request_id': review_request.pk, 
               b'review_id': review.pk, 
               b'reply_id': reply.pk, 
               b'message_format': b'text'}))
        self.assertEqual(response.status_code, 404)