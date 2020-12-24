# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/reviewboard/webapi/tests/test_review_screenshot_comment.py
# Compiled at: 2020-02-11 04:03:57
from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.utils import six
from djblets.webapi.errors import PERMISSION_DENIED
from reviewboard.reviews.models import ScreenshotComment
from reviewboard.webapi.resources import resources
from reviewboard.webapi.tests.base import BaseWebAPITestCase
from reviewboard.webapi.tests.mimetypes import screenshot_comment_item_mimetype, screenshot_comment_list_mimetype
from reviewboard.webapi.tests.mixins import BasicTestsMetaclass, ReviewRequestChildItemMixin, ReviewRequestChildListMixin
from reviewboard.webapi.tests.mixins_comment import CommentItemMixin, CommentListMixin
from reviewboard.webapi.tests.urls import get_review_screenshot_comment_item_url, get_review_screenshot_comment_list_url

class BaseTestCase(BaseWebAPITestCase):
    fixtures = [
     b'test_users']

    def _create_screenshot_review_with_issue(self, publish=False, comment_text=None):
        """Sets up a review for a screenshot that includes an open issue.

        If `publish` is True, the review is published. The review request is
        always published.

        Returns the response from posting the comment, the review object, and
        the review request object.
        """
        if not comment_text:
            comment_text = b'Test screenshot comment with an opened issue'
        review_request = self.create_review_request(publish=True, submitter=self.user)
        screenshot = self.create_screenshot(review_request)
        review = self.create_review(review_request, user=self.user, publish=publish)
        comment = self.create_screenshot_comment(review, screenshot, comment_text, issue_opened=True)
        return (
         comment, review, review_request)


@six.add_metaclass(BasicTestsMetaclass)
class ResourceListTests(CommentListMixin, ReviewRequestChildListMixin, BaseTestCase):
    """Testing the ReviewScreenshotCommentResource list APIs."""
    sample_api_url = b'review-requests/<id>/reviews/<id>/screenshot-comments/'
    resource = resources.review_screenshot_comment

    def setup_review_request_child_test(self, review_request):
        self.create_screenshot(review_request)
        review = self.create_review(review_request, user=self.user)
        return (
         get_review_screenshot_comment_list_url(review),
         screenshot_comment_list_mimetype)

    def compare_item(self, item_rsp, comment):
        self.assertEqual(item_rsp[b'id'], comment.pk)
        self.assertEqual(item_rsp[b'text'], comment.text)
        self.assertEqual(item_rsp[b'x'], comment.x)
        self.assertEqual(item_rsp[b'y'], comment.y)
        self.assertEqual(item_rsp[b'w'], comment.w)
        self.assertEqual(item_rsp[b'h'], comment.h)
        self.assertEqual(item_rsp[b'extra_data'], comment.extra_data)
        if comment.rich_text:
            self.assertEqual(item_rsp[b'text_type'], b'markdown')
        else:
            self.assertEqual(item_rsp[b'text_type'], b'plain')

    def setup_basic_get_test(self, user, with_local_site, local_site_name, populate_items):
        review_request = self.create_review_request(with_local_site=with_local_site, submitter=user, publish=True)
        screenshot = self.create_screenshot(review_request)
        review = self.create_review(review_request, user=user)
        if populate_items:
            items = [
             self.create_screenshot_comment(review, screenshot)]
        else:
            items = []
        return (
         get_review_screenshot_comment_list_url(review, local_site_name),
         screenshot_comment_list_mimetype,
         items)

    def setup_basic_post_test(self, user, with_local_site, local_site_name, post_valid_data):
        review_request = self.create_review_request(with_local_site=with_local_site, submitter=user, publish=True)
        screenshot = self.create_screenshot(review_request)
        review = self.create_review(review_request, user=user)
        return (
         get_review_screenshot_comment_list_url(review, local_site_name),
         screenshot_comment_item_mimetype,
         {b'screenshot_id': screenshot.pk, 
            b'text': b'Test comment', 
            b'x': 2, 
            b'y': 2, 
            b'w': 10, 
            b'h': 10},
         [
          review, screenshot])

    def check_post_result(self, user, rsp, review, screenshot):
        comment = ScreenshotComment.objects.get(pk=rsp[b'screenshot_comment'][b'id'])
        self.compare_item(rsp[b'screenshot_comment'], comment)

    def test_post_with_issue(self):
        """Testing the
        POST review-requests/<id>/reviews/<id>/screenshot-comments/ API
        with an issue
        """
        comment_text = b'Test screenshot comment with an opened issue'
        comment, review, review_request = self._create_screenshot_review_with_issue(publish=False, comment_text=comment_text)
        rsp = self.api_get(get_review_screenshot_comment_list_url(review), expected_mimetype=screenshot_comment_list_mimetype)
        self.assertEqual(rsp[b'stat'], b'ok')
        self.assertIn(b'screenshot_comments', rsp)
        self.assertEqual(len(rsp[b'screenshot_comments']), 1)
        self.assertEqual(rsp[b'screenshot_comments'][0][b'text'], comment_text)
        self.assertTrue(rsp[b'screenshot_comments'][0][b'issue_opened'])


@six.add_metaclass(BasicTestsMetaclass)
class ResourceItemTests(CommentItemMixin, ReviewRequestChildItemMixin, BaseTestCase):
    """Testing the ReviewScreenshotCommentResource item APIs."""
    fixtures = [
     b'test_users']
    sample_api_url = b'review-requests/<id>/reviews/<id>/screenshot-comments/<id>/'
    resource = resources.review_screenshot_comment

    def compare_item(self, item_rsp, comment):
        self.assertEqual(item_rsp[b'id'], comment.pk)
        self.assertEqual(item_rsp[b'text'], comment.text)
        self.assertEqual(item_rsp[b'x'], comment.x)
        self.assertEqual(item_rsp[b'y'], comment.y)
        self.assertEqual(item_rsp[b'w'], comment.w)
        self.assertEqual(item_rsp[b'h'], comment.h)
        self.assertEqual(item_rsp[b'extra_data'], comment.extra_data)
        if comment.rich_text:
            self.assertEqual(item_rsp[b'text_type'], b'markdown')
        else:
            self.assertEqual(item_rsp[b'text_type'], b'plain')

    def setup_review_request_child_test(self, review_request):
        screenshot = self.create_screenshot(review_request)
        review = self.create_review(review_request, user=self.user)
        comment = self.create_screenshot_comment(review, screenshot)
        return (
         get_review_screenshot_comment_item_url(review, comment.pk),
         screenshot_comment_item_mimetype)

    def setup_basic_delete_test(self, user, with_local_site, local_site_name):
        review_request = self.create_review_request(with_local_site=with_local_site, submitter=user, publish=True)
        screenshot = self.create_screenshot(review_request)
        review = self.create_review(review_request, user=user)
        comment = self.create_screenshot_comment(review, screenshot)
        return (
         get_review_screenshot_comment_item_url(review, comment.pk, local_site_name),
         [
          comment, review])

    def check_delete_result(self, user, comment, review):
        self.assertNotIn(comment, review.screenshot_comments.all())

    def test_delete_with_does_not_exist_error(self):
        """Testing the
        DELETE review-requests/<id>/reviews/<id>/screenshot-comments/<id>/ API
        with Does Not Exist error
        """
        review_request = self.create_review_request(publish=True)
        self.create_screenshot(review_request)
        review = self.create_review(review_request, user=self.user)
        self.api_delete(get_review_screenshot_comment_item_url(review, 123), expected_status=404)

    def setup_basic_get_test(self, user, with_local_site, local_site_name):
        review_request = self.create_review_request(with_local_site=with_local_site, submitter=user, publish=True)
        screenshot = self.create_screenshot(review_request)
        review = self.create_review(review_request, user=user)
        comment = self.create_screenshot_comment(review, screenshot)
        return (
         get_review_screenshot_comment_item_url(review, comment.pk, local_site_name),
         screenshot_comment_item_mimetype,
         comment)

    def setup_basic_put_test(self, user, with_local_site, local_site_name, put_valid_data):
        review_request = self.create_review_request(with_local_site=with_local_site, submitter=user, publish=True)
        screenshot = self.create_screenshot(review_request)
        review = self.create_review(review_request, user=user)
        comment = self.create_screenshot_comment(review, screenshot)
        return (
         get_review_screenshot_comment_item_url(review, comment.pk, local_site_name),
         screenshot_comment_item_mimetype, {b'text': b'Test comment'},
         comment, [])

    def check_put_result(self, user, item_rsp, comment, *args):
        comment = ScreenshotComment.objects.get(pk=comment.pk)
        self.assertEqual(item_rsp[b'text_type'], b'plain')
        self.assertEqual(item_rsp[b'text'], b'Test comment')
        self.compare_item(item_rsp, comment)

    def test_put_with_issue(self):
        """Testing the
        PUT review-requests/<id>/reviews/<id>/screenshot-comments/<id>/ API
        with an issue, removing issue_opened
        """
        comment, review, review_request = self._create_screenshot_review_with_issue()
        rsp = self.api_put(get_review_screenshot_comment_item_url(review, comment.pk), {b'issue_opened': False}, expected_mimetype=screenshot_comment_item_mimetype)
        self.assertEqual(rsp[b'stat'], b'ok')
        self.assertFalse(rsp[b'screenshot_comment'][b'issue_opened'])

    def test_put_issue_status_before_publish(self):
        """Testing the
        PUT review-requests/<id>/reviews/<id>/screenshot-comments/<id> API
        with an issue, before review is published
        """
        comment, review, review_request = self._create_screenshot_review_with_issue()
        rsp = self.api_put(get_review_screenshot_comment_item_url(review, comment.pk), {b'issue_status': b'resolved'}, expected_mimetype=screenshot_comment_item_mimetype)
        self.assertEqual(rsp[b'stat'], b'ok')
        self.assertEqual(rsp[b'screenshot_comment'][b'issue_status'], b'open')

    def test_put_issue_status_after_publish(self):
        """Testing the
        PUT review-requests/<id>/reviews/<id>/screenshot-comments/<id>/ API
        with an issue, after review is published
        """
        comment, review, review_request = self._create_screenshot_review_with_issue(publish=True)
        rsp = self.api_put(get_review_screenshot_comment_item_url(review, comment.pk), {b'issue_status': b'resolved'}, expected_mimetype=screenshot_comment_item_mimetype)
        self.assertEqual(rsp[b'stat'], b'ok')
        self.assertEqual(rsp[b'screenshot_comment'][b'issue_status'], b'resolved')

    def test_put_issue_status_by_issue_creator(self):
        """Testing the
        PUT review-requests/<id>/reviews/<id>/screenshot-comments/<id>/ API
        permissions for issue creator
        """
        comment, review, review_request = self._create_screenshot_review_with_issue(publish=True)
        review_request.submitter = User.objects.get(username=b'doc')
        review_request.save()
        rsp = self.api_put(get_review_screenshot_comment_item_url(review, comment.pk), {b'issue_status': b'dropped'}, expected_mimetype=screenshot_comment_item_mimetype)
        self.assertEqual(rsp[b'stat'], b'ok')
        self.assertEqual(rsp[b'screenshot_comment'][b'issue_status'], b'dropped')

    def test_put_issue_status_by_uninvolved_user(self):
        """Testing the
        PUT review-requests/<id>/reviews/<id>/screenshot-comments/<id>/ API
        permissions for an uninvolved user
        """
        comment, review, review_request = self._create_screenshot_review_with_issue(publish=True)
        new_owner = User.objects.get(username=b'doc')
        review_request.submitter = new_owner
        review_request.save()
        review.user = new_owner
        review.save()
        rsp = self.api_put(get_review_screenshot_comment_item_url(review, comment.pk), {b'issue_status': b'dropped'}, expected_status=403)
        self.assertEqual(rsp[b'stat'], b'fail')
        self.assertEqual(rsp[b'err'][b'code'], PERMISSION_DENIED.code)

    def test_put_deleted_screenshot_comment_issue_status(self):
        """Testing the
        PUT review-requests/<id>/reviews/<id>/screenshot-comments/<id>
        API with an issue and a deleted screenshot
        """
        comment_text = b'Test screenshot comment with an opened issue'
        x, y, w, h = (2, 2, 10, 10)
        review_request = self.create_review_request(publish=True, submitter=self.user, target_people=[
         self.user])
        screenshot = self.create_screenshot(review_request)
        review = self.create_review(review_request, user=self.user)
        comment = self.create_screenshot_comment(review, screenshot, comment_text, x, y, w, h, issue_opened=True)
        rsp = self.api_put(get_review_screenshot_comment_item_url(review, comment.pk), {b'issue_status': b'resolved'}, expected_mimetype=screenshot_comment_item_mimetype)
        self.assertEqual(rsp[b'stat'], b'ok')
        self.assertEqual(rsp[b'screenshot_comment'][b'issue_status'], b'open')
        review.public = True
        review.save()
        rsp = self.api_put(rsp[b'screenshot_comment'][b'links'][b'self'][b'href'], {b'issue_status': b'resolved'}, expected_mimetype=screenshot_comment_item_mimetype)
        self.assertEqual(rsp[b'stat'], b'ok')
        self.assertEqual(rsp[b'screenshot_comment'][b'issue_status'], b'resolved')
        self._delete_screenshot(review_request, screenshot)
        review_request.publish(review_request.submitter)
        rsp = self.api_put(rsp[b'screenshot_comment'][b'links'][b'self'][b'href'], {b'issue_status': b'open'}, expected_mimetype=screenshot_comment_item_mimetype)
        self.assertEqual(rsp[b'stat'], b'ok')
        self.assertEqual(rsp[b'screenshot_comment'][b'issue_status'], b'open')