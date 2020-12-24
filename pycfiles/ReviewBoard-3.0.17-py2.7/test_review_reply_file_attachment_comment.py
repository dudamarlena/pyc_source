# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/reviewboard/webapi/tests/test_review_reply_file_attachment_comment.py
# Compiled at: 2020-02-11 04:03:57
from __future__ import unicode_literals
from django.utils import six
from reviewboard.reviews.models import FileAttachmentComment
from reviewboard.webapi.resources import resources
from reviewboard.webapi.tests.base import BaseWebAPITestCase
from reviewboard.webapi.tests.mimetypes import review_reply_file_attachment_comment_item_mimetype, review_reply_file_attachment_comment_list_mimetype
from reviewboard.webapi.tests.mixins import BasicTestsMetaclass, ReviewRequestChildItemMixin, ReviewRequestChildListMixin
from reviewboard.webapi.tests.mixins_comment import CommentReplyItemMixin, CommentReplyListMixin
from reviewboard.webapi.tests.urls import get_review_reply_file_attachment_comment_item_url, get_review_reply_file_attachment_comment_list_url

@six.add_metaclass(BasicTestsMetaclass)
class ResourceListTests(CommentReplyListMixin, ReviewRequestChildListMixin, BaseWebAPITestCase):
    """Testing the ReviewReplyFileAttachmentCommentResource list APIs."""
    fixtures = [
     b'test_users']
    sample_api_url = b'review-requests/<id>/reviews/<id>/replies/<id>/file-attachment-comments/'
    resource = resources.review_reply_file_attachment_comment

    def setup_review_request_child_test(self, review_request):
        file_attachment = self.create_file_attachment(review_request)
        review = self.create_review(review_request, user=self.user, publish=True)
        self.create_file_attachment_comment(review, file_attachment)
        reply = self.create_reply(review, user=self.user)
        return (
         get_review_reply_file_attachment_comment_list_url(reply),
         review_reply_file_attachment_comment_list_mimetype)

    def compare_item(self, item_rsp, comment):
        self.assertEqual(item_rsp[b'id'], comment.pk)
        self.assertEqual(item_rsp[b'text'], comment.text)
        if comment.rich_text:
            self.assertEqual(item_rsp[b'text_type'], b'markdown')
        else:
            self.assertEqual(item_rsp[b'text_type'], b'plain')

    def setup_basic_get_test(self, user, with_local_site, local_site_name, populate_items):
        review_request = self.create_review_request(with_local_site=with_local_site, submitter=user, publish=True)
        file_attachment = self.create_file_attachment(review_request)
        review = self.create_review(review_request, user=user)
        comment = self.create_file_attachment_comment(review, file_attachment)
        reply = self.create_reply(review, user=user)
        if populate_items:
            items = [
             self.create_file_attachment_comment(reply, file_attachment, reply_to=comment)]
        else:
            items = []
        return (
         get_review_reply_file_attachment_comment_list_url(reply, local_site_name),
         review_reply_file_attachment_comment_list_mimetype,
         items)

    def setup_basic_post_test(self, user, with_local_site, local_site_name, post_valid_data):
        review_request = self.create_review_request(with_local_site=with_local_site, submitter=user, publish=True)
        file_attachment = self.create_file_attachment(review_request)
        review = self.create_review(review_request, user=user, publish=True)
        comment = self.create_file_attachment_comment(review, file_attachment)
        reply = self.create_reply(review, user=user)
        return (
         get_review_reply_file_attachment_comment_list_url(reply, local_site_name),
         review_reply_file_attachment_comment_item_mimetype,
         {b'reply_to_id': comment.pk, 
            b'text': b'Test comment'},
         [
          reply, comment, file_attachment])

    def check_post_result(self, user, rsp, reply, comment, file_attachment):
        reply_comment = FileAttachmentComment.objects.get(pk=rsp[b'file_attachment_comment'][b'id'])
        self.assertEqual(reply_comment.text, b'Test comment')
        self.assertEqual(reply_comment.reply_to, comment)
        self.assertFalse(reply_comment.rich_text)
        self.compare_item(rsp[b'file_attachment_comment'], reply_comment)

    def test_post_with_inactive_file_attachment(self):
        """Testing the POST
        review-requests/<id>/reviews/<id>/replies/<id>/file-attachment-comments/
        API with inactive file attachment
        """
        review_request = self.create_review_request(submitter=self.user)
        file_attachment = self.create_file_attachment(review_request)
        review_request.publish(review_request.submitter)
        review = self.create_review(review_request, user=b'doc')
        comment = self.create_file_attachment_comment(review, file_attachment)
        reply = self.create_reply(review, user=self.user)
        comments_url = get_review_reply_file_attachment_comment_list_url(reply)
        file_attachment = comment.file_attachment
        review_request = file_attachment.review_request.get()
        review_request.inactive_file_attachments.add(file_attachment)
        review_request.file_attachments.remove(file_attachment)
        rsp = self.api_post(comments_url, {b'reply_to_id': comment.id, 
           b'text': b'Test comment'}, expected_mimetype=review_reply_file_attachment_comment_item_mimetype)
        self.assertEqual(rsp[b'stat'], b'ok')
        self.check_post_result(self.user, rsp, reply, comment, file_attachment)

    def test_post_with_http_303(self):
        """Testing the POST
        review-requests/<id>/reviews/<id>/replies/<id>/file-attachment-comments/
        API with second instance of same reply
        """
        review_request = self.create_review_request(submitter=self.user, publish=True)
        file_attachment = self.create_file_attachment(review_request)
        review = self.create_review(review_request)
        comment = self.create_file_attachment_comment(review, file_attachment)
        reply = self.create_reply(review, user=self.user)
        self.create_file_attachment_comment(reply, file_attachment, reply_to=comment)
        rsp = self.api_post(get_review_reply_file_attachment_comment_list_url(reply), {b'reply_to_id': comment.pk, 
           b'text': b'Test comment'}, expected_status=303, expected_mimetype=review_reply_file_attachment_comment_item_mimetype)
        self.assertEqual(rsp[b'stat'], b'ok')
        self.check_post_result(self.user, rsp, reply, comment, file_attachment)


@six.add_metaclass(BasicTestsMetaclass)
class ResourceItemTests(CommentReplyItemMixin, ReviewRequestChildItemMixin, BaseWebAPITestCase):
    """Testing the ReviewReplyFileAttachmentCommentResource item APIs."""
    fixtures = [
     b'test_users']
    sample_api_url = b'review-requests/<id>/reviews/<id>/replies/<id>/file-attachment-comments/<id>/'
    resource = resources.review_reply_file_attachment_comment

    def setup_review_request_child_test(self, review_request):
        file_attachment = self.create_file_attachment(review_request)
        review = self.create_review(review_request, user=self.user, publish=True)
        comment = self.create_file_attachment_comment(review, file_attachment)
        reply = self.create_reply(review, user=self.user)
        reply_comment = self.create_file_attachment_comment(reply, file_attachment, reply_to=comment)
        return (
         get_review_reply_file_attachment_comment_item_url(reply, reply_comment.pk),
         review_reply_file_attachment_comment_item_mimetype)

    def compare_item(self, item_rsp, comment):
        self.assertEqual(item_rsp[b'id'], comment.pk)
        self.assertEqual(item_rsp[b'text'], comment.text)
        if comment.rich_text:
            self.assertEqual(item_rsp[b'text_type'], b'markdown')
        else:
            self.assertEqual(item_rsp[b'text_type'], b'plain')

    def setup_basic_delete_test(self, user, with_local_site, local_site_name):
        review_request = self.create_review_request(with_local_site=with_local_site, submitter=user, publish=True)
        file_attachment = self.create_file_attachment(review_request)
        review = self.create_review(review_request, user=user, publish=True)
        comment = self.create_file_attachment_comment(review, file_attachment)
        reply = self.create_reply(review, user=user)
        reply_comment = self.create_file_attachment_comment(reply, file_attachment, reply_to=comment)
        return (
         get_review_reply_file_attachment_comment_item_url(reply, reply_comment.pk, local_site_name),
         [
          reply_comment, reply])

    def check_delete_result(self, user, reply_comment, reply):
        self.assertNotIn(reply_comment, reply.file_attachment_comments.all())

    def setup_basic_get_test(self, user, with_local_site, local_site_name):
        review_request = self.create_review_request(with_local_site=with_local_site, submitter=user, publish=True)
        file_attachment = self.create_file_attachment(review_request)
        review = self.create_review(review_request, user=user, publish=True)
        comment = self.create_file_attachment_comment(review, file_attachment)
        reply = self.create_reply(review, user=user)
        reply_comment = self.create_file_attachment_comment(reply, file_attachment, reply_to=comment)
        return (
         get_review_reply_file_attachment_comment_item_url(reply, reply_comment.pk, local_site_name),
         review_reply_file_attachment_comment_item_mimetype,
         reply_comment)

    def setup_basic_put_test(self, user, with_local_site, local_site_name, put_valid_data):
        review_request = self.create_review_request(with_local_site=with_local_site, submitter=user, publish=True)
        file_attachment = self.create_file_attachment(review_request)
        review = self.create_review(review_request, user=user, publish=True)
        comment = self.create_file_attachment_comment(review, file_attachment)
        reply = self.create_reply(review, user=user)
        reply_comment = self.create_file_attachment_comment(reply, file_attachment, reply_to=comment)
        return (
         get_review_reply_file_attachment_comment_item_url(reply, reply_comment.pk, local_site_name),
         review_reply_file_attachment_comment_item_mimetype,
         {b'text': b'Test comment'},
         reply_comment, [])

    def check_put_result(self, user, item_rsp, comment, *args):
        comment = FileAttachmentComment.objects.get(pk=comment.pk)
        self.assertEqual(item_rsp[b'id'], comment.pk)
        self.assertEqual(item_rsp[b'text'], b'Test comment')
        self.assertFalse(comment.rich_text)
        self.compare_item(item_rsp, comment)