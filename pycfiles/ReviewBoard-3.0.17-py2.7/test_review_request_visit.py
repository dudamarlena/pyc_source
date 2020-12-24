# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/reviewboard/accounts/tests/test_review_request_visit.py
# Compiled at: 2020-02-11 04:03:56
"""Unit tests for reviewboard.accounts.models.ReviewRequestVisit."""
from __future__ import unicode_literals
from reviewboard.accounts.models import ReviewRequestVisit
from reviewboard.testing import TestCase

class ReviewRequestVisitTests(TestCase):
    """Unit tests for reviewboard.accounts.models.ReviewRequestVisit."""
    fixtures = [
     b'test_users']

    def test_default_visibility(self):
        """Testing ReviewRequestVisit.visibility default value"""
        review_request = self.create_review_request(publish=True)
        self.client.login(username=b'admin', password=b'admin')
        self.client.get(review_request.get_absolute_url())
        visit = ReviewRequestVisit.objects.get(user__username=b'admin', review_request=review_request.id)
        self.assertEqual(visit.visibility, ReviewRequestVisit.VISIBLE)