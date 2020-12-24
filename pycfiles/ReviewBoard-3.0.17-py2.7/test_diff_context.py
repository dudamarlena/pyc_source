# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/reviewboard/webapi/tests/test_diff_context.py
# Compiled at: 2020-02-11 04:03:57
"""Tests for the DiffContextResource."""
from __future__ import unicode_literals
from django.utils import six
from djblets.webapi.testing.decorators import webapi_test_template
from reviewboard.webapi.resources import resources
from reviewboard.webapi.tests.base import BaseWebAPITestCase
from reviewboard.webapi.tests.mimetypes import diff_context_mimetype
from reviewboard.webapi.tests.mixins import BaseReviewRequestChildMixin, BasicTestsMetaclass
from reviewboard.webapi.tests.urls import get_diff_context_url

@six.add_metaclass(BasicTestsMetaclass)
class ResourceTests(BaseWebAPITestCase, BaseReviewRequestChildMixin):
    """Testing the DiffContextResource APIs."""
    resource = resources.diff_context
    test_http_methods = ('GET', )
    sample_api_url = b'review-requests/<id>/diff-context/'
    fixtures = [
     b'test_scmtools', b'test_users']

    def compare_item(self, item_rsp, obj):
        review_request, diffset, interdiffset = obj
        self.assertIn(b'revision', item_rsp)
        revision_info = item_rsp[b'revision']
        self.assertIn(b'interdiff_revision', revision_info)
        self.assertIn(b'is_draft_diff', revision_info)
        self.assertIn(b'is_draft_interdiff', revision_info)
        self.assertIn(b'is_interdiff', revision_info)
        self.assertIn(b'latest_revision', revision_info)
        self.assertIn(b'revision', revision_info)
        self.assertEqual(revision_info[b'is_draft_diff'], None)
        self.assertEqual(revision_info[b'is_draft_interdiff'], None)
        self.assertEqual(revision_info[b'is_interdiff'], interdiffset is not None)
        self.assertEqual(revision_info[b'latest_revision'], review_request.get_latest_diffset().revision)
        self.assertEqual(revision_info[b'revision'], diffset.revision)
        self.assertIn(b'num_diffs', item_rsp)
        if interdiffset:
            self.assertEqual(revision_info[b'interdiff_revision'], interdiffset.revision)
            self.assertEqual(item_rsp[b'num_diffs'], 2)
        else:
            self.assertEqual(revision_info[b'interdiff_revision'], None)
            self.assertEqual(item_rsp[b'num_diffs'], 1)
        return

    def setup_basic_get_test(self, user, with_local_site, local_site_name, with_interdiff=False):
        repository = self.create_repository(with_local_site=with_local_site)
        review_request = self.create_review_request(with_local_site=with_local_site, repository=repository, public=True, submitter=user)
        diffset = self.create_diffset(review_request=review_request, repository=repository)
        self.create_filediff(diffset)
        if with_interdiff:
            interdiffset = diffset
            diffset = self.create_diffset(review_request, repository=repository, revision=2)
            self.create_filediff(diffset)
        else:
            interdiffset = None
        return (
         get_diff_context_url(review_request_id=review_request.display_id, local_site_name=local_site_name),
         diff_context_mimetype,
         (
          review_request, diffset, interdiffset))

    def setup_review_request_child_test(self, review_request):
        """Set up the review request child tests.

        Args:
            review_request (reviewboard.reviews.models.review_request.
                            ReviewRequest):
                The test review request.

        Returns:
            tuple:
            A tuple of the API list URL and list mimetype to run tests on.
        """
        review_request.repository = self.create_repository()
        diffset = self.create_diffset(review_request)
        self.create_filediff(diffset)
        return (
         get_diff_context_url(review_request_id=review_request.display_id),
         diff_context_mimetype)

    @webapi_test_template
    def test_get_interdiff(self):
        """Testing the GET <URL> API with an interdiff"""
        url, mimetype, (review_request, diffset, interdiffset) = self.setup_basic_get_test(user=self.user, with_local_site=False, local_site_name=None, with_interdiff=True)
        rsp = self.api_get(url, {b'revision': diffset.revision, 
           b'interdiff-revision': interdiffset.revision}, expected_mimetype=mimetype)
        self.assertIn(b'stat', rsp)
        self.assertEqual(rsp[b'stat'], b'ok')
        self.assertIn(self.resource.item_result_key, rsp)
        self.compare_item(rsp[self.resource.item_result_key], (
         review_request, diffset, interdiffset))
        return