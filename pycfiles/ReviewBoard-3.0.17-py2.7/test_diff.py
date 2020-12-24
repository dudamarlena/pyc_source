# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/reviewboard/webapi/tests/test_diff.py
# Compiled at: 2020-02-11 04:03:57
from __future__ import unicode_literals
import os
from django.utils import six
from djblets.webapi.errors import INVALID_ATTRIBUTE, INVALID_FORM_DATA, PERMISSION_DENIED
from reviewboard import scmtools
from reviewboard.diffviewer.models import DiffSet
from reviewboard.webapi.errors import DIFF_TOO_BIG
from reviewboard.webapi.resources import resources
from reviewboard.webapi.tests.base import BaseWebAPITestCase
from reviewboard.webapi.tests.mimetypes import diff_item_mimetype, diff_list_mimetype
from reviewboard.webapi.tests.mixins import BasicTestsMetaclass, ReviewRequestChildItemMixin, ReviewRequestChildListMixin
from reviewboard.webapi.tests.mixins_extra_data import ExtraDataItemMixin, ExtraDataListMixin
from reviewboard.webapi.tests.urls import get_diff_item_url, get_diff_list_url

@six.add_metaclass(BasicTestsMetaclass)
class ResourceListTests(ExtraDataListMixin, ReviewRequestChildListMixin, BaseWebAPITestCase):
    """Testing the DiffResource list APIs."""
    fixtures = [
     b'test_users', b'test_scmtools']
    sample_api_url = b'review-requests/<id>/diffs/'
    resource = resources.diff

    def setup_review_request_child_test(self, review_request):
        return (
         get_diff_list_url(review_request), diff_list_mimetype)

    def compare_item(self, item_rsp, diffset):
        self.assertEqual(item_rsp[b'id'], diffset.pk)
        self.assertEqual(item_rsp[b'name'], diffset.name)
        self.assertEqual(item_rsp[b'revision'], diffset.revision)
        self.assertEqual(item_rsp[b'basedir'], diffset.basedir)
        self.assertEqual(item_rsp[b'base_commit_id'], diffset.base_commit_id)
        self.assertEqual(item_rsp[b'extra_data'], diffset.extra_data)

    def setup_basic_get_test(self, user, with_local_site, local_site_name, populate_items):
        review_request = self.create_review_request(create_repository=True, with_local_site=with_local_site, submitter=user, publish=True)
        if populate_items:
            items = [
             self.create_diffset(review_request)]
        else:
            items = []
        return (
         get_diff_list_url(review_request, local_site_name),
         diff_list_mimetype,
         items)

    def setup_basic_post_test(self, user, with_local_site, local_site_name, post_valid_data):
        repository = self.create_repository(tool_name=b'Test')
        review_request = self.create_review_request(with_local_site=with_local_site, repository=repository, submitter=user)
        if post_valid_data:
            diff_filename = os.path.join(os.path.dirname(scmtools.__file__), b'testdata', b'git_readme.diff')
            post_data = {b'path': open(diff_filename, b'r'), 
               b'basedir': b'/trunk', 
               b'base_commit_id': b'1234'}
        else:
            post_data = {}
        return (
         get_diff_list_url(review_request, local_site_name),
         diff_item_mimetype,
         post_data,
         [
          review_request])

    def check_post_result(self, user, rsp, review_request):
        self.assertIn(b'diff', rsp)
        item_rsp = rsp[b'diff']
        draft = review_request.get_draft()
        self.assertIsNotNone(draft)
        diffset = DiffSet.objects.get(pk=item_rsp[b'id'])
        self.assertEqual(diffset, draft.diffset)
        self.compare_item(item_rsp, diffset)

    def test_post_with_missing_data(self):
        """Testing the POST review-requests/<id>/diffs/ API
        with Invalid Form Data
        """
        repository = self.create_repository(tool_name=b'Test')
        review_request = self.create_review_request(repository=repository, submitter=self.user)
        rsp = self.api_post(get_diff_list_url(review_request), expected_status=400)
        self.assertEqual(rsp[b'stat'], b'fail')
        self.assertEqual(rsp[b'err'][b'code'], INVALID_FORM_DATA.code)
        self.assertIn(b'path', rsp[b'fields'])
        review_request = self.create_review_request(repository=repository, submitter=self.user)
        diff_filename = os.path.join(os.path.dirname(scmtools.__file__), b'testdata', b'git_readme.diff')
        with open(diff_filename, b'r') as (f):
            rsp = self.api_post(get_diff_list_url(review_request), {b'path': f}, expected_status=400)
        self.assertEqual(rsp[b'stat'], b'fail')
        self.assertEqual(rsp[b'err'][b'code'], INVALID_FORM_DATA.code)
        self.assertIn(b'basedir', rsp[b'fields'])

    def test_post_too_big(self):
        """Testing the POST review-requests/<id>/diffs/ API
        with diff exceeding max size
        """
        repository = self.create_repository()
        review_request = self.create_review_request(repository=repository, submitter=self.user)
        diff_filename = os.path.join(os.path.dirname(scmtools.__file__), b'testdata', b'git_readme.diff')
        with self.siteconfig_settings({b'diffviewer_max_diff_size': 2}, reload_settings=False):
            with open(diff_filename, b'r') as (f):
                rsp = self.api_post(get_diff_list_url(review_request), {b'path': f, 
                   b'basedir': b'/trunk'}, expected_status=400)
        self.assertEqual(rsp[b'stat'], b'fail')
        self.assertEqual(rsp[b'err'][b'code'], DIFF_TOO_BIG.code)
        self.assertIn(b'reason', rsp)
        self.assertIn(b'max_size', rsp)
        self.assertEqual(rsp[b'max_size'], 2)

    def test_post_not_owner(self):
        """Testing the POST review-requests/<id>/diffs/ API
        without owner
        """
        repository = self.create_repository(tool_name=b'Test')
        review_request = self.create_review_request(repository=repository)
        diff_filename = os.path.join(os.path.dirname(scmtools.__file__), b'testdata', b'git_readme.diff')
        with open(diff_filename, b'r') as (f):
            rsp = self.api_post(get_diff_list_url(review_request), {b'path': f, 
               b'basedir': b'/trunk'}, expected_status=403)
        self.assertEqual(rsp[b'stat'], b'fail')
        self.assertEqual(rsp[b'err'][b'code'], PERMISSION_DENIED.code)

    def test_post_no_repository(self):
        """Testing the POST review-requests/<id>/diffs API
        with a ReviewRequest that has no repository
        """
        review_request = self.create_review_request(submitter=self.user)
        diff_filename = os.path.join(os.path.dirname(scmtools.__file__), b'testdata', b'git_readme.diff')
        with open(diff_filename, b'r') as (f):
            rsp = self.api_post(get_diff_list_url(review_request), {b'path': f, 
               b'basedir': b'/trunk'}, expected_status=400)
        self.assertEqual(rsp[b'stat'], b'fail')
        self.assertEqual(rsp[b'err'][b'code'], INVALID_ATTRIBUTE.code)


@six.add_metaclass(BasicTestsMetaclass)
class ResourceItemTests(ExtraDataItemMixin, ReviewRequestChildItemMixin, BaseWebAPITestCase):
    """Testing the DiffResource item APIs."""
    fixtures = [
     b'test_users', b'test_scmtools']
    sample_api_url = b'review-requests/<id>/diffs/<revision>/'
    resource = resources.diff

    def setup_review_request_child_test(self, review_request):
        if not review_request.repository:
            review_request.repository = self.create_repository()
            review_request.save()
        diffset = self.create_diffset(review_request)
        return (
         get_diff_item_url(review_request, diffset.revision),
         diff_item_mimetype)

    def setup_http_not_allowed_item_test(self, user):
        review_request = self.create_review_request(create_repository=True, publish=True)
        return get_diff_item_url(review_request, 1)

    def compare_item(self, item_rsp, diffset):
        self.assertEqual(item_rsp[b'id'], diffset.pk)
        self.assertEqual(item_rsp[b'name'], diffset.name)
        self.assertEqual(item_rsp[b'revision'], diffset.revision)
        self.assertEqual(item_rsp[b'basedir'], diffset.basedir)
        self.assertEqual(item_rsp[b'base_commit_id'], diffset.base_commit_id)
        self.assertEqual(item_rsp[b'extra_data'], diffset.extra_data)

    def setup_basic_get_test(self, user, with_local_site, local_site_name):
        review_request = self.create_review_request(create_repository=True, with_local_site=with_local_site, submitter=user)
        diffset = self.create_diffset(review_request)
        return (
         get_diff_item_url(review_request, diffset.revision, local_site_name),
         diff_item_mimetype,
         diffset)

    def test_get_not_modified(self):
        """Testing the GET review-requests/<id>/diffs/<revision>/ API
        with Not Modified response
        """
        review_request = self.create_review_request(create_repository=True, publish=True)
        diffset = self.create_diffset(review_request)
        self._testHttpCaching(get_diff_item_url(review_request, diffset.revision), check_etags=True)

    def setup_basic_put_test(self, user, with_local_site, local_site_name, put_valid_data):
        review_request = self.create_review_request(create_repository=True, with_local_site=with_local_site, submitter=user)
        diffset = self.create_diffset(review_request)
        return (
         get_diff_item_url(review_request, diffset.revision, local_site_name),
         diff_item_mimetype, {},
         diffset, [])

    def check_put_result(self, user, item_rsp, diffset):
        diffset = DiffSet.objects.get(pk=diffset.pk)
        self.compare_item(item_rsp, diffset)