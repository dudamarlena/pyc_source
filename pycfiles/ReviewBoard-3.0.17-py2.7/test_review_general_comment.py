# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/reviewboard/webapi/tests/test_review_general_comment.py
# Compiled at: 2020-02-11 04:03:57
from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.utils import six
from djblets.webapi.errors import PERMISSION_DENIED
from reviewboard.reviews.models import GeneralComment
from reviewboard.webapi.resources import resources
from reviewboard.webapi.tests.base import BaseWebAPITestCase
from reviewboard.webapi.tests.mimetypes import general_comment_item_mimetype, general_comment_list_mimetype
from reviewboard.webapi.tests.mixins import BasicTestsMetaclass, ReviewRequestChildItemMixin, ReviewRequestChildListMixin
from reviewboard.webapi.tests.mixins_comment import CommentItemMixin, CommentListMixin
from reviewboard.webapi.tests.urls import get_review_general_comment_item_url, get_review_general_comment_list_url

class BaseTestCase(BaseWebAPITestCase):
    fixtures = [
     b'test_users']

    def _create_general_review_with_issue(self, publish=False, comment_text=None):
        """Sets up a review for a general comment that includes an open issue.

        If `publish` is True, the review is published. The review request is
        always published.

        Returns the response from posting the comment, the review object, and
        the review request object.
        """
        if not comment_text:
            comment_text = b'Test general comment with an opened issue'
        review_request = self.create_review_request(publish=True, submitter=self.user)
        review = self.create_review(review_request, user=self.user, publish=publish)
        comment = self.create_general_comment(review, comment_text, issue_opened=True)
        return (
         comment, review, review_request)


@six.add_metaclass(BasicTestsMetaclass)
class ResourceListTests(CommentListMixin, ReviewRequestChildListMixin, BaseTestCase):
    """Testing the ReviewGeneralCommentResource list APIs."""
    sample_api_url = b'review-requests/<id>/reviews/<id>/general-comments/'
    resource = resources.review_general_comment

    def setup_review_request_child_test(self, review_request):
        review = self.create_review(review_request, user=self.user)
        return (
         get_review_general_comment_list_url(review),
         general_comment_list_mimetype)

    def compare_item(self, item_rsp, comment):
        self.assertEqual(item_rsp[b'id'], comment.pk)
        self.assertEqual(item_rsp[b'text'], comment.text)
        self.assertEqual(item_rsp[b'extra_data'], comment.extra_data)
        if comment.rich_text:
            self.assertEqual(item_rsp[b'text_type'], b'markdown')
        else:
            self.assertEqual(item_rsp[b'text_type'], b'plain')

    def setup_basic_get_test(self, user, with_local_site, local_site_name, populate_items):
        review_request = self.create_review_request(with_local_site=with_local_site, submitter=user, publish=True)
        review = self.create_review(review_request, user=user)
        if populate_items:
            items = [
             self.create_general_comment(review)]
        else:
            items = []
        return (
         get_review_general_comment_list_url(review, local_site_name),
         general_comment_list_mimetype,
         items)

    def setup_basic_post_test(self, user, with_local_site, local_site_name, post_valid_data):
        review_request = self.create_review_request(with_local_site=with_local_site, submitter=user, publish=True)
        review = self.create_review(review_request, user=user)
        return (
         get_review_general_comment_list_url(review, local_site_name),
         general_comment_item_mimetype,
         {b'text': b'Test comment'},
         [
          review])

    def check_post_result(self, user, rsp, review):
        comment = GeneralComment.objects.get(pk=rsp[b'general_comment'][b'id'])
        self.compare_item(rsp[b'general_comment'], comment)

    def test_post_with_issue(self):
        """Testing the
        POST review-requests/<id>/reviews/<id>/general-comments/ API
        with an issue
        """
        comment_text = b'Test general comment with an opened issue'
        comment, review, review_request = self._create_general_review_with_issue(publish=False, comment_text=comment_text)
        rsp = self.api_get(get_review_general_comment_list_url(review), expected_mimetype=general_comment_list_mimetype)
        self.assertEqual(rsp[b'stat'], b'ok')
        self.assertIn(b'general_comments', rsp)
        self.assertEqual(len(rsp[b'general_comments']), 1)
        self.assertEqual(rsp[b'general_comments'][0][b'text'], comment_text)
        self.assertTrue(rsp[b'general_comments'][0][b'issue_opened'])


@six.add_metaclass(BasicTestsMetaclass)
class ResourceItemTests(CommentItemMixin, ReviewRequestChildItemMixin, BaseTestCase):
    """Testing the ReviewGeneralCommentResource item APIs."""
    fixtures = [
     b'test_users']
    sample_api_url = b'review-requests/<id>/reviews/<id>/general-comments/<id>/'
    resource = resources.review_general_comment

    def compare_item(self, item_rsp, comment):
        self.assertEqual(item_rsp[b'id'], comment.pk)
        self.assertEqual(item_rsp[b'text'], comment.text)
        self.assertEqual(item_rsp[b'extra_data'], comment.extra_data)
        if comment.rich_text:
            self.assertEqual(item_rsp[b'text_type'], b'markdown')
        else:
            self.assertEqual(item_rsp[b'text_type'], b'plain')

    def setup_review_request_child_test(self, review_request):
        review = self.create_review(review_request, user=self.user)
        comment = self.create_general_comment(review)
        return (
         get_review_general_comment_item_url(review, comment.pk),
         general_comment_item_mimetype)

    def setup_basic_delete_test(self, user, with_local_site, local_site_name):
        review_request = self.create_review_request(with_local_site=with_local_site, submitter=user, publish=True)
        review = self.create_review(review_request, user=user)
        comment = self.create_general_comment(review)
        return (
         get_review_general_comment_item_url(review, comment.pk, local_site_name),
         [
          comment, review])

    def check_delete_result(self, user, comment, review):
        self.assertNotIn(comment, review.general_comments.all())

    def test_delete_with_does_not_exist_error(self):
        """Testing the
        DELETE review-requests/<id>/reviews/<id>/general-comments/<id>/ API
        with Does Not Exist error
        """
        review_request = self.create_review_request(publish=True)
        review = self.create_review(review_request, user=self.user)
        self.api_delete(get_review_general_comment_item_url(review, 123), expected_status=404)

    def setup_basic_get_test(self, user, with_local_site, local_site_name):
        review_request = self.create_review_request(with_local_site=with_local_site, submitter=user, publish=True)
        review = self.create_review(review_request, user=user)
        comment = self.create_general_comment(review)
        return (
         get_review_general_comment_item_url(review, comment.pk, local_site_name),
         general_comment_item_mimetype,
         comment)

    def setup_basic_put_test(self, user, with_local_site, local_site_name, put_valid_data):
        review_request = self.create_review_request(with_local_site=with_local_site, submitter=user, publish=True)
        review = self.create_review(review_request, user=user)
        comment = self.create_general_comment(review)
        return (
         get_review_general_comment_item_url(review, comment.pk, local_site_name),
         general_comment_item_mimetype,
         {b'text': b'Test comment'},
         comment, [])

    def check_put_result(self, user, item_rsp, comment, *args):
        comment = GeneralComment.objects.get(pk=comment.pk)
        self.assertEqual(item_rsp[b'text_type'], b'plain')
        self.assertEqual(item_rsp[b'text'], b'Test comment')
        self.compare_item(item_rsp, comment)

    def test_put_with_issue(self):
        """Testing the
        PUT review-requests/<id>/reviews/<id>/general-comments/<id>/ API
        with an issue, removing issue_opened
        """
        comment, review, review_request = self._create_general_review_with_issue()
        rsp = self.api_put(get_review_general_comment_item_url(review, comment.pk), {b'issue_opened': False}, expected_mimetype=general_comment_item_mimetype)
        self.assertEqual(rsp[b'stat'], b'ok')
        self.assertFalse(rsp[b'general_comment'][b'issue_opened'])

    def test_put_issue_status_before_publish(self):
        """Testing the
        PUT review-requests/<id>/reviews/<id>/general-comments/<id> API
        with an issue, before review is published
        """
        comment, review, review_request = self._create_general_review_with_issue()
        rsp = self.api_put(get_review_general_comment_item_url(review, comment.pk), {b'issue_status': b'resolved'}, expected_mimetype=general_comment_item_mimetype)
        self.assertEqual(rsp[b'stat'], b'ok')
        self.assertEqual(rsp[b'general_comment'][b'issue_status'], b'open')

    def test_put_issue_status_after_publish(self):
        """Testing the
        PUT review-requests/<id>/reviews/<id>/general-comments/<id>/ API
        with an issue, after review is published
        """
        comment, review, review_request = self._create_general_review_with_issue(publish=True)
        rsp = self.api_put(get_review_general_comment_item_url(review, comment.pk), {b'issue_status': b'resolved'}, expected_mimetype=general_comment_item_mimetype)
        self.assertEqual(rsp[b'stat'], b'ok')
        self.assertEqual(rsp[b'general_comment'][b'issue_status'], b'resolved')

    def test_put_issue_status_by_issue_creator(self):
        """Testing the
        PUT review-requests/<id>/reviews/<id>/general-comments/<id>/ API
        permissions for issue creator
        """
        comment, review, review_request = self._create_general_review_with_issue(publish=True)
        review_request.submitter = User.objects.get(username=b'doc')
        review_request.save()
        rsp = self.api_put(get_review_general_comment_item_url(review, comment.pk), {b'issue_status': b'dropped'}, expected_mimetype=general_comment_item_mimetype)
        self.assertEqual(rsp[b'stat'], b'ok')
        self.assertEqual(rsp[b'general_comment'][b'issue_status'], b'dropped')

    def test_put_issue_status_by_uninvolved_user(self):
        """Testing the
        PUT review-requests/<id>/reviews/<id>/general-comments/<id>/ API
        permissions for an uninvolved user
        """
        comment, review, review_request = self._create_general_review_with_issue(publish=True)
        new_owner = User.objects.get(username=b'doc')
        review_request.submitter = new_owner
        review_request.save()
        review.user = new_owner
        review.save()
        rsp = self.api_put(get_review_general_comment_item_url(review, comment.pk), {b'issue_status': b'dropped'}, expected_status=403)
        self.assertEqual(rsp[b'stat'], b'fail')
        self.assertEqual(rsp[b'err'][b'code'], PERMISSION_DENIED.code)