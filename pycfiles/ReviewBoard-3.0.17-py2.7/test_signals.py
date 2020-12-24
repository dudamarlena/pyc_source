# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/reviewboard/reviews/tests/test_signals.py
# Compiled at: 2020-02-11 04:03:56
"""Tests for reviewboard.review.signals."""
from __future__ import unicode_literals
from django.utils import six
from djblets.testing.decorators import add_fixtures
from kgb import SpyAgency
from reviewboard.deprecation import RemovedInReviewBoard40Warning
from reviewboard.reviews.models import ReviewRequest
from reviewboard.reviews.signals import review_request_closed, review_request_closing
from reviewboard.testing import TestCase

class DeprecatedSignalArgsTests(SpyAgency, TestCase):
    """Tests for deprecated signal arguments."""

    @add_fixtures([b'test_users'])
    def test_review_request_closed(self):
        """Testing review_request_closing signal has deprecated type argument
        """

        def review_request_closed_cb(close_type, **kwargs):
            self.assertIn(b'type', kwargs)
            type_ = kwargs[b'type']
            message = b'The "type" argument for "review_request_closed" has been deprecated and will be removed in a future version. Use "close_type" instead.'
            with self.assert_warns(RemovedInReviewBoard40Warning, message):
                self.assertEqual(six.text_type(type_), close_type)

        self.spy_on(review_request_closed_cb)
        review_request_closed.connect(review_request_closed_cb, sender=ReviewRequest)
        review_request = self.create_review_request(publish=True)
        try:
            review_request.close(ReviewRequest.SUBMITTED)
        finally:
            review_request_closed.disconnect(review_request_closed_cb)

        self.assertTrue(review_request_closed_cb.spy.called)

    @add_fixtures([b'test_users'])
    def test_review_request_closing(self):
        """Testing review_request_closing signal has deprecated type argument
        """

        def review_request_closing_cb(close_type, **kwargs):
            self.assertIn(b'type', kwargs)
            type_ = kwargs[b'type']
            message = b'The "type" argument for "review_request_closing" has been deprecated and will be removed in a future version. Use "close_type" instead.'
            with self.assert_warns(RemovedInReviewBoard40Warning, message):
                self.assertEqual(six.text_type(type_), close_type)

        self.spy_on(review_request_closing_cb)
        review_request_closing.connect(review_request_closing_cb, sender=ReviewRequest)
        review_request = self.create_review_request(publish=True)
        try:
            review_request.close(ReviewRequest.SUBMITTED)
        finally:
            review_request_closing.disconnect(review_request_closing_cb)

        self.assertTrue(review_request_closing_cb.spy.called)