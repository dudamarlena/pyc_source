# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/reviewboard/webapi/tests/test_diff_file_attachment.py
# Compiled at: 2020-02-11 04:03:57
from __future__ import unicode_literals
from django.utils import six
from djblets.webapi.errors import PERMISSION_DENIED
from reviewboard.webapi.resources import resources
from reviewboard.webapi.tests.base import BaseWebAPITestCase
from reviewboard.webapi.tests.mimetypes import diff_file_attachment_item_mimetype, diff_file_attachment_list_mimetype
from reviewboard.webapi.tests.mixins import BasicTestsMetaclass
from reviewboard.webapi.tests.urls import get_diff_file_attachment_item_url, get_diff_file_attachment_list_url

@six.add_metaclass(BasicTestsMetaclass)
class ResourceListTests(BaseWebAPITestCase):
    """Testing the DiffFileAttachmentResource list APIs."""
    fixtures = [
     b'test_users', b'test_scmtools']
    sample_api_url = b'repositories/<id>/diff-file-attachments/'
    resource = resources.diff_file_attachment

    def compare_item(self, item_rsp, attachment):
        self.assertEqual(item_rsp[b'id'], attachment.pk)
        self.assertEqual(item_rsp[b'filename'], attachment.filename)
        self.assertEqual(item_rsp[b'caption'], attachment.caption)
        self.assertEqual(item_rsp[b'mimetype'], attachment.mimetype)

    def setup_http_not_allowed_list_test(self, user):
        repository = self.create_repository()
        return get_diff_file_attachment_list_url(repository)

    def setup_basic_get_test(self, user, with_local_site, local_site_name, populate_items):
        repository = self.create_repository(with_local_site=with_local_site)
        if populate_items:
            diffset = self.create_diffset(repository=repository)
            filediff = self.create_filediff(diffset)
            items = [self.create_diff_file_attachment(filediff)]
        else:
            items = []
        return (
         get_diff_file_attachment_list_url(repository, local_site_name),
         diff_file_attachment_list_mimetype,
         items)

    def test_get_with_mimetype(self):
        """Testing the GET repositories/<id>/diff-file-attachments/ API
        with ?mimetype=
        """
        repository = self.create_repository()
        diffset = self.create_diffset(repository=repository)
        filediff = self.create_filediff(diffset)
        attachment = self.create_diff_file_attachment(filediff, caption=b'Image', orig_filename=b'image.png', mimetype=b'image/png')
        self.create_diff_file_attachment(filediff, caption=b'Text', orig_filename=b'text.txt', mimetype=b'text/plain')
        rsp = self.api_get(get_diff_file_attachment_list_url(repository) + b'?mimetype=image/png', expected_mimetype=diff_file_attachment_list_mimetype)
        self.assertEqual(rsp[b'stat'], b'ok')
        self.assertIn(b'diff_file_attachments', rsp)
        attachments_rsp = rsp[b'diff_file_attachments']
        self.assertEqual(len(attachments_rsp), 1)
        attachment_rsp = attachments_rsp[0]
        self.assertEqual(attachment_rsp[b'id'], attachment.pk)
        self.assertEqual(attachment_rsp[b'filename'], b'image.png')
        self.assertEqual(attachment_rsp[b'caption'], b'Image')
        self.assertEqual(attachment_rsp[b'mimetype'], b'image/png')

    def test_get_with_repository_file_path(self):
        """Testing the GET repositories/<id>/diff-file-attachments/ API
        with ?repository-file-path=
        """
        repository = self.create_repository()
        diffset = self.create_diffset(repository=repository)
        filediff1 = self.create_filediff(diffset, source_file=b'/test-file-1.png', dest_file=b'/test-file-1.png')
        filediff2 = self.create_filediff(diffset, source_file=b'/test-file-2.png', dest_file=b'/test-file-2.png')
        attachment = self.create_diff_file_attachment(filediff1, caption=b'File 1', orig_filename=b'/test-file-1.png')
        self.create_diff_file_attachment(filediff2, caption=b'File 2', orig_filename=b'/test-file-2.png')
        rsp = self.api_get(get_diff_file_attachment_list_url(repository) + b'?repository-file-path=/test-file-1.png', expected_mimetype=diff_file_attachment_list_mimetype)
        self.assertEqual(rsp[b'stat'], b'ok')
        self.assertIn(b'diff_file_attachments', rsp)
        attachments_rsp = rsp[b'diff_file_attachments']
        self.assertEqual(len(attachments_rsp), 1)
        attachment_rsp = attachments_rsp[0]
        self.assertEqual(attachment_rsp[b'id'], attachment.pk)
        self.assertEqual(attachment_rsp[b'filename'], b'/test-file-1.png')
        self.assertEqual(attachment_rsp[b'caption'], b'File 1')
        self.assertEqual(attachment_rsp[b'mimetype'], b'image/png')

    def test_get_with_repository_revision(self):
        """Testing the GET repositories/<id>/diff-file-attachments/ API
        with ?repository-revision=
        """
        repository = self.create_repository()
        diffset = self.create_diffset(repository=repository)
        filediff1 = self.create_filediff(diffset, source_file=b'/test-file-1.png', dest_file=b'/test-file-1.png', source_revision=b'4', dest_detail=b'5')
        filediff2 = self.create_filediff(diffset, source_file=b'/test-file-2.png', dest_file=b'/test-file-2.png', source_revision=b'9', dest_detail=b'10')
        attachment = self.create_diff_file_attachment(filediff1, caption=b'File 1', orig_filename=b'/test-file-1.png')
        self.create_diff_file_attachment(filediff2, caption=b'File 2', orig_filename=b'/test-file-2.png')
        rsp = self.api_get(get_diff_file_attachment_list_url(repository) + b'?repository-revision=5', expected_mimetype=diff_file_attachment_list_mimetype)
        self.assertEqual(rsp[b'stat'], b'ok')
        self.assertIn(b'diff_file_attachments', rsp)
        attachments_rsp = rsp[b'diff_file_attachments']
        self.assertEqual(len(attachments_rsp), 1)
        attachment_rsp = attachments_rsp[0]
        self.assertEqual(attachment_rsp[b'id'], attachment.pk)
        self.assertEqual(attachment_rsp[b'filename'], b'/test-file-1.png')
        self.assertEqual(attachment_rsp[b'caption'], b'File 1')
        self.assertEqual(attachment_rsp[b'mimetype'], b'image/png')


@six.add_metaclass(BasicTestsMetaclass)
class ResourceItemTests(BaseWebAPITestCase):
    """Testing the DiffFileAttachmentResource item APIs."""
    fixtures = [
     b'test_users', b'test_scmtools']
    sample_api_url = b'repositories/<id>/diff-file-attachments/<id>/'
    resource = resources.diff_file_attachment

    def compare_item(self, item_rsp, attachment):
        self.assertEqual(item_rsp[b'id'], attachment.pk)
        self.assertEqual(item_rsp[b'filename'], attachment.filename)
        self.assertEqual(item_rsp[b'caption'], attachment.caption)
        self.assertEqual(item_rsp[b'mimetype'], attachment.mimetype)

    def setup_http_not_allowed_item_test(self, user):
        repository = self.create_repository()
        diffset = self.create_diffset(repository=repository)
        filediff = self.create_filediff(diffset)
        attachment = self.create_diff_file_attachment(filediff)
        return get_diff_file_attachment_item_url(repository, attachment)

    def setup_basic_get_test(self, user, with_local_site, local_site_name):
        repository = self.create_repository(with_local_site=with_local_site)
        diffset = self.create_diffset(repository=repository)
        filediff = self.create_filediff(diffset)
        attachment = self.create_diff_file_attachment(filediff)
        return (
         get_diff_file_attachment_item_url(attachment, repository, local_site_name),
         diff_file_attachment_item_mimetype,
         attachment)

    def test_get_with_invite_only_repo(self):
        """Testing the GET repositories/<id>/diff-file-attachments/<id>/ API
        with access to an invite-only repository
        """
        repository = self.create_repository(public=False)
        repository.users.add(self.user)
        diffset = self.create_diffset(repository=repository)
        filediff = self.create_filediff(diffset)
        attachment = self.create_diff_file_attachment(filediff)
        rsp = self.api_get(get_diff_file_attachment_item_url(attachment, repository), expected_mimetype=diff_file_attachment_item_mimetype)
        self.assertEqual(rsp[b'stat'], b'ok')
        self.assertIn(b'diff_file_attachment', rsp)
        attachment_rsp = rsp[b'diff_file_attachment']
        self.assertEqual(attachment_rsp[b'id'], attachment.pk)
        self.assertEqual(attachment_rsp[b'filename'], attachment.filename)
        self.assertEqual(attachment_rsp[b'caption'], attachment.caption)
        self.assertEqual(attachment_rsp[b'mimetype'], attachment.mimetype)

    def test_get_with_invite_only_repo_no_access(self):
        """Testing the GET repositories/<id>/diff-file-attachments/<id>/ API
        without access to an invite-only repository
        """
        repository = self.create_repository(public=False)
        diffset = self.create_diffset(repository=repository)
        filediff = self.create_filediff(diffset)
        attachment = self.create_diff_file_attachment(filediff)
        rsp = self.api_get(get_diff_file_attachment_item_url(attachment, repository), expected_status=403)
        self.assertEqual(rsp[b'stat'], b'fail')
        self.assertEqual(rsp[b'err'][b'code'], PERMISSION_DENIED.code)