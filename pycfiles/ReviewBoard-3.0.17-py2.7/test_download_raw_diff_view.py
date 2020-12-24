# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/reviewboard/reviews/tests/test_download_raw_diff_view.py
# Compiled at: 2020-02-11 04:03:56
"""Unit tests for reviewboard.reviews.views.DownloadRawDiffView."""
from __future__ import unicode_literals
from reviewboard.testing import TestCase

class DownloadRawDiffViewTests(TestCase):
    """Unit tests for reviewboard.reviews.views.DownloadRawDiffView."""
    fixtures = [
     b'test_users', b'test_scmtools']

    def test_sends_correct_content_disposition(self):
        """Testing DownloadRawDiffView sends correct Content-Disposition"""
        review_request = self.create_review_request(create_repository=True, publish=True)
        self.create_diffset(review_request=review_request)
        response = self.client.get(b'/r/%d/diff/raw/' % review_request.pk)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response[b'Content-Disposition'], b'attachment; filename=diffset')

    def test_normalize_commas_in_filename(self):
        """Testing DownloadRawDiffView removes commas in filename"""
        review_request = self.create_review_request(create_repository=True, publish=True)
        self.create_diffset(review_request=review_request, name=b'test, comma')
        response = self.client.get(b'/r/%d/diff/raw/' % review_request.pk)
        content_disposition = response[b'Content-Disposition']
        filename = content_disposition[len(b'attachment; filename='):]
        self.assertFalse(b',' in filename)