# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/reviewboard/webapi/tests/test_draft_filediff.py
# Compiled at: 2020-02-11 04:03:57
from __future__ import unicode_literals
import os
from django.utils import six
from djblets.webapi.errors import INVALID_FORM_DATA
from reviewboard import scmtools
from reviewboard.attachments.models import FileAttachment
from reviewboard.diffviewer.models import DiffSet, FileDiff
from reviewboard.webapi.resources import resources
from reviewboard.webapi.tests.base import BaseWebAPITestCase
from reviewboard.webapi.tests.mimetypes import diff_item_mimetype, filediff_item_mimetype, filediff_list_mimetype
from reviewboard.webapi.tests.mixins import BasicTestsMetaclass
from reviewboard.webapi.tests.mixins_extra_data import ExtraDataItemMixin
from reviewboard.webapi.tests.urls import get_diff_list_url, get_draft_filediff_item_url, get_draft_filediff_list_url

@six.add_metaclass(BasicTestsMetaclass)
class ResourceListTests(BaseWebAPITestCase):
    """Testing the DraftFileDiffResource list APIs."""
    fixtures = [
     b'test_users', b'test_scmtools']
    sample_api_url = b'review-requests/<id>/draft/diffs/<revision>/files/'
    resource = resources.draft_filediff

    def compare_item(self, item_rsp, filediff):
        self.assertEqual(item_rsp[b'id'], filediff.pk)
        self.assertEqual(item_rsp[b'source_file'], filediff.source_file)
        self.assertEqual(item_rsp[b'extra_data'], filediff.extra_data)

    def setup_http_not_allowed_list_test(self, user):
        review_request = self.create_review_request(create_repository=True, submitter=user)
        diffset = self.create_diffset(review_request, draft=True)
        return get_draft_filediff_list_url(diffset, review_request)

    def setup_basic_get_test(self, user, with_local_site, local_site_name, populate_items):
        review_request = self.create_review_request(create_repository=True, with_local_site=with_local_site, submitter=user)
        diffset = self.create_diffset(review_request, draft=True)
        if populate_items:
            items = [
             self.create_filediff(diffset)]
        else:
            items = []
        return (
         get_draft_filediff_list_url(diffset, review_request, local_site_name),
         filediff_list_mimetype,
         items)

    def test_get_not_owner(self):
        """Testing the
        GET review-requests/<id>/draft/diffs/<revision>/files/ API
        without owner with Permission Denied error
        """
        review_request = self.create_review_request(create_repository=True)
        self.assertNotEqual(review_request.submitter, self.user)
        diffset = self.create_diffset(review_request, draft=True)
        self.api_get(get_draft_filediff_list_url(diffset, review_request), expected_status=403)


@six.add_metaclass(BasicTestsMetaclass)
class ResourceItemTests(ExtraDataItemMixin, BaseWebAPITestCase):
    """Testing the DraftFileDiffResource item APIs."""
    fixtures = [
     b'test_users', b'test_scmtools']
    sample_api_url = b'review-requests/<id>/draft/diffs/<revision>/files/<id>/'
    resource = resources.draft_filediff
    test_http_methods = ('DELETE', 'GET', 'PUT')

    def setup_http_not_allowed_item_test(self, user):
        review_request = self.create_review_request(create_repository=True, submitter=user)
        diffset = self.create_diffset(review_request, draft=True)
        filediff = self.create_filediff(diffset)
        return get_draft_filediff_item_url(filediff, review_request)

    def compare_item(self, item_rsp, filediff):
        self.assertEqual(item_rsp[b'id'], filediff.pk)
        self.assertEqual(item_rsp[b'source_file'], filediff.source_file)
        self.assertEqual(item_rsp[b'extra_data'], filediff.extra_data)

    def setup_basic_get_test(self, user, with_local_site, local_site_name):
        review_request = self.create_review_request(create_repository=True, with_local_site=with_local_site, submitter=user)
        diffset = self.create_diffset(review_request, draft=True)
        filediff = self.create_filediff(diffset)
        return (
         get_draft_filediff_item_url(filediff, review_request, local_site_name),
         filediff_item_mimetype,
         filediff)

    def test_get_not_owner(self):
        """Testing the
        GET review-requests/<id>/draft/diffs/<revision>/files/<id>/ API
        without owner with Permission Denied error
        """
        review_request = self.create_review_request(create_repository=True)
        self.assertNotEqual(review_request.submitter, self.user)
        diffset = self.create_diffset(review_request, draft=True)
        filediff = self.create_filediff(diffset)
        self.api_get(get_draft_filediff_item_url(filediff, review_request), expected_status=403)

    def setup_basic_put_test(self, user, with_local_site, local_site_name, put_valid_data):
        review_request = self.create_review_request(submitter=user, with_local_site=with_local_site, create_repository=True)
        diffset = self.create_diffset(review_request, draft=True)
        filediff = self.create_filediff(diffset)
        return (
         get_draft_filediff_item_url(filediff, review_request, local_site_name),
         filediff_item_mimetype, {},
         filediff, [])

    def check_put_result(self, user, item_rsp, filediff):
        filediff = FileDiff.objects.get(pk=filediff.pk)
        self.compare_item(item_rsp, filediff)

    def test_put_with_new_file_and_dest_attachment_file(self):
        """Testing the PUT review-requests/<id>/diffs/<id>/files/<id>/ API
        with new file and dest_attachment_file
        """
        review_request = self.create_review_request(create_repository=True, submitter=self.user)
        diff_filename = os.path.join(os.path.dirname(scmtools.__file__), b'testdata', b'git_binary_image_new.diff')
        with open(diff_filename, b'rb') as (f):
            rsp = self.api_post(get_diff_list_url(review_request), {b'path': f, 
               b'base_commit_id': b'1234'}, expected_mimetype=diff_item_mimetype)
        self.assertEqual(rsp[b'stat'], b'ok')
        diffset = DiffSet.objects.get(pk=rsp[b'diff'][b'id'])
        filediffs = diffset.files.all()
        self.assertEqual(len(filediffs), 1)
        filediff = filediffs[0]
        self.assertEqual(filediff.source_file, b'logo.png')
        with open(self.get_sample_image_filename(), b'rb') as (f):
            rsp = self.api_put(get_draft_filediff_item_url(filediff, review_request) + b'?expand=dest_attachment', {b'dest_attachment_file': f}, expected_mimetype=filediff_item_mimetype)
        self.assertEqual(rsp[b'stat'], b'ok')
        self.assertIn(b'dest_attachment', rsp[b'file'])
        attachment = FileAttachment.objects.get(pk=rsp[b'file'][b'dest_attachment'][b'id'])
        self.assertTrue(attachment.is_from_diff)
        self.assertEqual(attachment.orig_filename, b'logo.png')
        self.assertEqual(attachment.added_in_filediff, filediff)
        self.assertEqual(attachment.repo_path, None)
        self.assertEqual(attachment.repo_revision, None)
        self.assertEqual(attachment.repository, None)
        return

    def test_put_with_modified_file_and_dest_attachment_file(self):
        """Testing the PUT review-requests/<id>/diffs/<id>/files/<id>/ API
        with modified file and dest_attachment_file
        """
        review_request = self.create_review_request(create_repository=True, submitter=self.user)
        diff_filename = os.path.join(os.path.dirname(scmtools.__file__), b'testdata', b'git_binary_image_modified.diff')
        with open(diff_filename, b'r') as (f):
            rsp = self.api_post(get_diff_list_url(review_request), {b'path': f, 
               b'base_commit_id': b'1234'}, expected_mimetype=diff_item_mimetype)
        self.assertEqual(rsp[b'stat'], b'ok')
        diffset = DiffSet.objects.get(pk=rsp[b'diff'][b'id'])
        filediffs = diffset.files.all()
        self.assertEqual(len(filediffs), 1)
        filediff = filediffs[0]
        self.assertEqual(filediff.source_file, b'logo.png')
        with open(self.get_sample_image_filename(), b'rb') as (f):
            rsp = self.api_put(get_draft_filediff_item_url(filediff, review_request) + b'?expand=dest_attachment', {b'dest_attachment_file': f}, expected_mimetype=filediff_item_mimetype)
        self.assertEqual(rsp[b'stat'], b'ok')
        self.assertIn(b'dest_attachment', rsp[b'file'])
        attachment = FileAttachment.objects.get(pk=rsp[b'file'][b'dest_attachment'][b'id'])
        self.assertTrue(attachment.is_from_diff)
        self.assertEqual(attachment.orig_filename, b'logo.png')
        self.assertEqual(attachment.added_in_filediff, None)
        self.assertEqual(attachment.repo_path, b'logo.png')
        self.assertEqual(attachment.repo_revision, b'86b520d')
        self.assertEqual(attachment.repository, review_request.repository)
        return

    def test_put_second_dest_attachment_file_disallowed(self):
        """Testing the PUT review-requests/<id>/diffs/<id>/files/<id>/ API
        disallows setting dest_attachment_file twice
        """
        review_request = self.create_review_request(create_repository=True, submitter=self.user)
        diff_filename = os.path.join(os.path.dirname(scmtools.__file__), b'testdata', b'git_binary_image_modified.diff')
        with open(diff_filename, b'r') as (f):
            rsp = self.api_post(get_diff_list_url(review_request), {b'path': f, 
               b'base_commit_id': b'1234'}, expected_mimetype=diff_item_mimetype)
        diffset = DiffSet.objects.get(pk=rsp[b'diff'][b'id'])
        filediff = diffset.files.all()[0]
        url = get_draft_filediff_item_url(filediff, review_request)
        trophy_filename = self.get_sample_image_filename()
        with open(trophy_filename, b'rb') as (f):
            self.api_put(url, {b'dest_attachment_file': f}, expected_mimetype=filediff_item_mimetype)
        with open(trophy_filename, b'rb') as (f):
            rsp = self.api_put(url, {b'dest_attachment_file': f}, expected_status=400)
            self.assertEqual(rsp[b'stat'], b'fail')
            self.assertEqual(rsp[b'err'][b'code'], INVALID_FORM_DATA.code)
            self.assertIn(b'fields', rsp)
            self.assertIn(b'dest_attachment_file', rsp[b'fields'])