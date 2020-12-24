# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/reviewboard/webapi/tests/test_user_file_attachment.py
# Compiled at: 2020-02-11 04:03:57
from __future__ import unicode_literals
from django.utils import six
from djblets.webapi.errors import DUPLICATE_ITEM
from reviewboard.attachments.models import FileAttachment
from reviewboard.site.models import LocalSite
from reviewboard.webapi.resources import resources
from reviewboard.webapi.tests.base import BaseWebAPITestCase
from reviewboard.webapi.tests.mimetypes import user_file_attachment_item_mimetype, user_file_attachment_list_mimetype
from reviewboard.webapi.tests.mixins import BasicTestsMetaclass
from reviewboard.webapi.tests.urls import get_user_file_attachment_item_url, get_user_file_attachment_list_url

@six.add_metaclass(BasicTestsMetaclass)
class ResourceListTests(BaseWebAPITestCase):
    """Testing the UserFileAttachmentResource list APIs."""
    fixtures = [
     b'test_users', b'test_site']
    resource = resources.user_file_attachment
    sample_api_url = b'users/<username>/file-attachments/'

    def compare_item(self, item_rsp, attachment):
        self.assertEqual(item_rsp[b'id'], attachment.pk)
        self.assertEqual(item_rsp[b'filename'], attachment.filename)

    def setup_basic_get_test(self, user, with_local_site, local_site_name, populate_items):
        if populate_items:
            local_site = LocalSite.objects.get(name=b'local-site-1')
            if with_local_site:
                self.create_user_file_attachment(user, has_file=True, orig_filename=b'Trophy1.png', mimetype=b'image/png')
                self.create_user_file_attachment(user)
                items = [
                 self.create_user_file_attachment(user, local_site=local_site)]
            else:
                self.create_user_file_attachment(user, local_site=local_site)
                items = [
                 self.create_user_file_attachment(user, has_file=True, orig_filename=b'Trph.png', mimetype=b'image/png'),
                 self.create_user_file_attachment(user)]
        else:
            items = []
        return (
         get_user_file_attachment_list_url(user, local_site_name),
         user_file_attachment_list_mimetype,
         items)

    def setup_basic_post_test(self, user, with_local_site, local_site_name, post_valid_data):
        caption = b'My initial caption.'
        return (
         get_user_file_attachment_list_url(user, local_site_name),
         user_file_attachment_item_mimetype,
         {b'path': open(self.get_sample_image_filename(), b'rb'), 
            b'caption': caption},
         [
          caption])

    def check_post_result(self, user, rsp, caption):
        self.assertIn(b'user_file_attachment', rsp)
        item_rsp = rsp[b'user_file_attachment']
        attachment = FileAttachment.objects.get(pk=item_rsp[b'id'])
        self.compare_item(item_rsp, attachment)
        self.assertEqual(attachment.caption, caption)

    def test_post_no_file_attachment(self):
        """Testing the POST users/<username>/file-attachments/ API without a
        file attached
        """
        caption = b'My initial caption.'
        rsp = self.api_post(get_user_file_attachment_list_url(self.user), {b'caption': caption}, expected_status=201, expected_mimetype=user_file_attachment_item_mimetype)
        self.check_post_result(None, rsp, caption)
        return


@six.add_metaclass(BasicTestsMetaclass)
class ResourceItemTests(BaseWebAPITestCase):
    """Testing the UserFileAttachmentResource item APIs."""
    fixtures = [
     b'test_users']
    sample_api_url = b'users/<username>/file-attachments/<id>/'
    resource = resources.user_file_attachment

    def compare_item(self, item_rsp, attachment):
        self.assertEqual(item_rsp[b'id'], attachment.pk)
        self.assertEqual(item_rsp[b'filename'], attachment.filename)

    def setup_basic_delete_test(self, user, with_local_site, local_site_name):
        file_attachment = self.create_user_file_attachment(user, with_local_site=with_local_site, local_site_name=local_site_name)
        return (
         get_user_file_attachment_item_url(user, file_attachment, local_site_name),
         [
          file_attachment])

    def check_delete_result(self, user, file_attachment):
        file_attachments = FileAttachment.objects.all()
        self.assertNotIn(file_attachment, file_attachments)

    def setup_basic_get_test(self, user, with_local_site, local_site_name):
        file_attachment = self.create_user_file_attachment(user, with_local_site=with_local_site, local_site_name=local_site_name)
        return (
         get_user_file_attachment_item_url(user, file_attachment, local_site_name),
         user_file_attachment_item_mimetype,
         file_attachment)

    def setup_basic_put_test(self, user, with_local_site, local_site_name, put_valid_data):
        file_attachment = self.create_user_file_attachment(user, with_local_site=with_local_site, local_site_name=local_site_name)
        return (
         get_user_file_attachment_item_url(user, file_attachment, local_site_name),
         user_file_attachment_item_mimetype, {b'caption': b'My new caption'},
         file_attachment, [])

    def check_put_result(self, user, item_rsp, file_attachment):
        file_attachment = FileAttachment.objects.get(pk=file_attachment.pk)
        self.assertEqual(item_rsp[b'id'], file_attachment.pk)
        self.assertEqual(file_attachment.caption, b'My new caption')
        self.assertEqual(file_attachment.user, user)
        self.compare_item(item_rsp, file_attachment)

    def test_put_file_already_exists(self):
        """Testing the PUT users/<username>/file-attachments/<id>/ API
        attaching file to object that already has a file attached to it
        """
        file_attachment = self.create_user_file_attachment(self.user, has_file=True, orig_filename=b'Trophy1.png', mimetype=b'image/png')
        with open(self.get_sample_image_filename(), b'rb') as (f):
            self.assertTrue(f)
            rsp = self.api_put(get_user_file_attachment_item_url(self.user, file_attachment), {b'caption': b'My new caption.', 
               b'path': f}, expected_status=409)
        self.assertEqual(rsp[b'stat'], b'fail')
        self.assertEqual(rsp[b'err'][b'code'], DUPLICATE_ITEM.code)