# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/reviewboard/webapi/tests/test_review_reply_screenshot_comment.py
# Compiled at: 2020-02-11 04:03:57
from __future__ import unicode_literals
from django.utils import six
from reviewboard.reviews.models import ScreenshotComment
from reviewboard.webapi.resources import resources
from reviewboard.webapi.tests.base import BaseWebAPITestCase
from reviewboard.webapi.tests.mimetypes import review_reply_screenshot_comment_item_mimetype, review_reply_screenshot_comment_list_mimetype
from reviewboard.webapi.tests.mixins import BasicTestsMetaclass, ReviewRequestChildItemMixin, ReviewRequestChildListMixin
from reviewboard.webapi.tests.mixins_comment import CommentReplyItemMixin, CommentReplyListMixin
from reviewboard.webapi.tests.urls import get_review_reply_screenshot_comment_item_url, get_review_reply_screenshot_comment_list_url

@six.add_metaclass(BasicTestsMetaclass)
class ResourceListTests(CommentReplyListMixin, ReviewRequestChildListMixin, BaseWebAPITestCase):
    """Testing the ReviewReplyScreenshotCommentResource list APIs."""
    fixtures = [
     b'test_users']
    sample_api_url = b'review-requests/<id>/reviews/<id>/replies/<id>/screenshot-comments/'
    resource = resources.review_reply_screenshot_comment

    def setup_review_request_child_test(self, review_request):
        screenshot = self.create_screenshot(review_request)
        review = self.create_review(review_request, user=self.user, publish=True)
        self.create_screenshot_comment(review, screenshot)
        reply = self.create_reply(review, user=self.user)
        return (
         get_review_reply_screenshot_comment_list_url(reply),
         review_reply_screenshot_comment_list_mimetype)

    def compare_item(self, item_rsp, comment):
        self.assertEqual(item_rsp[b'id'], comment.pk)
        self.assertEqual(item_rsp[b'text'], comment.text)
        if comment.rich_text:
            self.assertEqual(item_rsp[b'text_type'], b'markdown')
        else:
            self.assertEqual(item_rsp[b'text_type'], b'plain')

    def setup_basic_get_test(self, user, with_local_site, local_site_name, populate_items):
        review_request = self.create_review_request(with_local_site=with_local_site, submitter=user, publish=True)
        screenshot = self.create_screenshot(review_request)
        review = self.create_review(review_request, user=user)
        comment = self.create_screenshot_comment(review, screenshot)
        reply = self.create_reply(review, user=user)
        if populate_items:
            items = [
             self.create_screenshot_comment(reply, screenshot, reply_to=comment)]
        else:
            items = []
        return (get_review_reply_screenshot_comment_list_url(reply, local_site_name),
         review_reply_screenshot_comment_list_mimetype,
         items)

    def setup_basic_post_test(self, user, with_local_site, local_site_name, post_valid_data):
        review_request = self.create_review_request(with_local_site=with_local_site, submitter=user, publish=True)
        screenshot = self.create_screenshot(review_request)
        review = self.create_review(review_request, user=user, publish=True)
        comment = self.create_screenshot_comment(review, screenshot)
        reply = self.create_reply(review, user=user)
        return (
         get_review_reply_screenshot_comment_list_url(reply, local_site_name),
         review_reply_screenshot_comment_item_mimetype,
         {b'reply_to_id': comment.pk, 
            b'text': b'Test comment'},
         [
          reply, comment, screenshot])

    def check_post_result(self, user, rsp, reply, comment, screenshot):
        reply_comment = ScreenshotComment.objects.get(pk=rsp[b'screenshot_comment'][b'id'])
        self.assertEqual(reply_comment.text, b'Test comment')
        self.assertEqual(reply_comment.reply_to, comment)
        self.assertEqual(reply_comment.rich_text, False)
        self.compare_item(rsp[b'screenshot_comment'], reply_comment)

    def test_post_with_http_303(self):
        """Testing the POST
        review-requests/<id>/reviews/<id>/replies/<id>/screenshot-comments/ API
        with second instance of same reply
        """
        comment_text = b'My Comment Text'
        review_request = self.create_review_request(publish=True)
        screenshot = self.create_screenshot(review_request)
        review = self.create_review(review_request, user=self.user, publish=True)
        comment = self.create_screenshot_comment(review, screenshot)
        reply = self.create_reply(review, user=self.user)
        reply_comment = self.create_screenshot_comment(reply, screenshot, reply_to=comment)
        rsp = self.api_post(get_review_reply_screenshot_comment_list_url(reply), {b'reply_to_id': comment.pk, 
           b'text': comment_text}, expected_status=303, expected_mimetype=review_reply_screenshot_comment_item_mimetype)
        self.assertEqual(rsp[b'stat'], b'ok')
        reply_comment = ScreenshotComment.objects.get(pk=rsp[b'screenshot_comment'][b'id'])
        self.assertEqual(reply_comment.text, comment_text)


@six.add_metaclass(BasicTestsMetaclass)
class ResourceItemTests(CommentReplyItemMixin, ReviewRequestChildItemMixin, BaseWebAPITestCase):
    """Testing the ReviewReplyScreenshotCommentResource item APIs."""
    fixtures = [
     b'test_users']
    sample_api_url = b'review-requests/<id>/reviews/<id>/replies/<id>/screenshot-comments/<id>/'
    resource = resources.review_reply_screenshot_comment

    def setup_review_request_child_test(self, review_request):
        screenshot = self.create_screenshot(review_request)
        review = self.create_review(review_request, user=self.user, publish=True)
        comment = self.create_screenshot_comment(review, screenshot)
        reply = self.create_reply(review, user=self.user)
        reply_comment = self.create_screenshot_comment(reply, screenshot, reply_to=comment)
        return (
         get_review_reply_screenshot_comment_item_url(reply, reply_comment.pk),
         review_reply_screenshot_comment_item_mimetype)

    def compare_item(self, item_rsp, comment):
        self.assertEqual(item_rsp[b'id'], comment.pk)
        self.assertEqual(item_rsp[b'text'], comment.text)
        if comment.rich_text:
            self.assertEqual(item_rsp[b'text_type'], b'markdown')
        else:
            self.assertEqual(item_rsp[b'text_type'], b'plain')

    def setup_basic_delete_test(self, user, with_local_site, local_site_name):
        review_request = self.create_review_request(with_local_site=with_local_site, submitter=user, publish=True)
        screenshot = self.create_screenshot(review_request)
        review = self.create_review(review_request, user=user, publish=True)
        comment = self.create_screenshot_comment(review, screenshot)
        reply = self.create_reply(review, user=user)
        reply_comment = self.create_screenshot_comment(reply, screenshot, reply_to=comment)
        return (
         get_review_reply_screenshot_comment_item_url(reply, reply_comment.pk, local_site_name),
         [
          reply_comment, reply])

    def check_delete_result(self, user, reply_comment, reply):
        self.assertNotIn(reply_comment, reply.screenshot_comments.all())

    def setup_basic_get_test(self, user, with_local_site, local_site_name):
        review_request = self.create_review_request(with_local_site=with_local_site, submitter=user, publish=True)
        screenshot = self.create_screenshot(review_request)
        review = self.create_review(review_request, user=user, publish=True)
        comment = self.create_screenshot_comment(review, screenshot)
        reply = self.create_reply(review, user=user)
        reply_comment = self.create_screenshot_comment(reply, screenshot, reply_to=comment)
        return (
         get_review_reply_screenshot_comment_item_url(reply, reply_comment.pk, local_site_name),
         review_reply_screenshot_comment_item_mimetype,
         reply_comment)

    def setup_basic_put_test(self, user, with_local_site, local_site_name, put_valid_data):
        review_request = self.create_review_request(with_local_site=with_local_site, submitter=user, publish=True)
        screenshot = self.create_screenshot(review_request)
        review = self.create_review(review_request, user=user, publish=True)
        comment = self.create_screenshot_comment(review, screenshot)
        reply = self.create_reply(review, user=user)
        reply_comment = self.create_screenshot_comment(reply, screenshot, reply_to=comment)
        return (
         get_review_reply_screenshot_comment_item_url(reply, reply_comment.pk, local_site_name),
         review_reply_screenshot_comment_item_mimetype,
         {b'text': b'Test comment'},
         reply_comment, [])

    def check_put_result(self, user, item_rsp, comment, *args):
        comment = ScreenshotComment.objects.get(pk=comment.pk)
        self.assertEqual(item_rsp[b'id'], comment.pk)
        self.assertEqual(item_rsp[b'text'], b'Test comment')
        self.assertEqual(comment.text, b'Test comment')