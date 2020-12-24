# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/reviewboard/webapi/tests/test_file_attachment_comment.py
# Compiled at: 2020-02-11 04:03:57
from __future__ import unicode_literals
from django.utils import six
from reviewboard.webapi.resources import resources
from reviewboard.webapi.tests.base import BaseWebAPITestCase
from reviewboard.webapi.tests.mimetypes import file_attachment_comment_list_mimetype
from reviewboard.webapi.tests.mixins import BasicTestsMetaclass, ReviewRequestChildListMixin
from reviewboard.webapi.tests.urls import get_file_attachment_comment_list_url

@six.add_metaclass(BasicTestsMetaclass)
class ResourceListTests(ReviewRequestChildListMixin, BaseWebAPITestCase):
    """Testing the FileAttachmentCommentResource list APIs."""
    fixtures = [
     b'test_users']
    sample_api_url = b'review-requests/<id>/file-attachments/<id>/comments/'
    resource = resources.file_attachment_comment

    def setup_review_request_child_test(self, review_request):
        file_attachment = self.create_file_attachment(review_request)
        return (
         get_file_attachment_comment_list_url(file_attachment),
         file_attachment_comment_list_mimetype)

    def setup_http_not_allowed_list_test(self, user):
        review_request = self.create_review_request(submitter=user, publish=True)
        file_attachment = self.create_file_attachment(review_request)
        return get_file_attachment_comment_list_url(file_attachment)

    def compare_item(self, item_rsp, comment):
        self.assertEqual(item_rsp[b'id'], comment.pk)
        self.assertEqual(item_rsp[b'text'], comment.text)

    def setup_basic_get_test(self, user, with_local_site, local_site_name, populate_items):
        review_request = self.create_review_request(with_local_site=with_local_site, submitter=user, publish=True)
        file_attachment = self.create_file_attachment(review_request)
        if populate_items:
            review = self.create_review(review_request, publish=True)
            items = [
             self.create_file_attachment_comment(review, file_attachment)]
        else:
            items = []
        return (get_file_attachment_comment_list_url(file_attachment, local_site_name),
         file_attachment_comment_list_mimetype,
         items)


ResourceItemTests = None