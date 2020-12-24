# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/reviewboard/reviews/tests/test_comment_diff_fragments_view.py
# Compiled at: 2020-02-11 04:03:56
"""Unit tests for reviewboard.reviews.views.CommentDiffFragmentsView."""
from __future__ import unicode_literals
import struct
from django.contrib.auth.models import User
from django.utils import six
from djblets.testing.decorators import add_fixtures
from reviewboard.site.urlresolvers import local_site_reverse
from reviewboard.testing import TestCase

class CommentDiffFragmentsViewTests(TestCase):
    """Unit tests for reviewboard.reviews.views.CommentDiffFragmentsView."""
    fixtures = [
     b'test_users', b'test_scmtools']

    def test_get_with_unpublished_review_request_not_owner(self):
        """Testing CommentDiffFragmentsView with unpublished review request and
        user is not the owner
        """
        user = User.objects.create_user(username=b'reviewer', password=b'reviewer', email=b'reviewer@example.com')
        review_request = self.create_review_request(create_repository=True)
        diffset = self.create_diffset(review_request)
        filediff = self.create_filediff(diffset)
        review = self.create_review(review_request, user=user)
        comment1 = self.create_diff_comment(review, filediff)
        comment2 = self.create_diff_comment(review, filediff)
        review.publish()
        self.assertTrue(self.client.login(username=b'reviewer', password=b'reviewer'))
        self._get_fragments(review_request, [
         comment1.pk, comment2.pk], expected_status=403)

    def test_get_with_unpublished_review_request_owner(self):
        """Testing CommentDiffFragmentsView with unpublished review request and
        user is the owner
        """
        user = User.objects.create_user(username=b'test-user', password=b'test-user', email=b'user@example.com')
        review_request = self.create_review_request(create_repository=True, submitter=user)
        diffset = self.create_diffset(review_request)
        filediff = self.create_filediff(diffset)
        review = self.create_review(review_request, user=user)
        comment1 = self.create_diff_comment(review, filediff)
        comment2 = self.create_diff_comment(review, filediff)
        review.publish()
        self.assertTrue(self.client.login(username=b'test-user', password=b'test-user'))
        fragments = self._get_fragments(review_request, [
         comment1.pk, comment2.pk])
        self.assertEqual(len(fragments), 2)
        self.assertEqual(fragments[0][0], comment1.pk)
        self.assertEqual(fragments[1][0], comment2.pk)

    @add_fixtures([b'test_site'])
    def test_get_with_published_review_request_local_site_access(self):
        """Testing CommentDiffFragmentsView with published review request on
        a Local Site the user has access to
        """
        user = User.objects.create_user(username=b'test-user', password=b'test-user', email=b'user@example.com')
        review_request = self.create_review_request(create_repository=True, with_local_site=True, publish=True)
        diffset = self.create_diffset(review_request)
        filediff = self.create_filediff(diffset)
        review = self.create_review(review_request)
        comment1 = self.create_diff_comment(review, filediff)
        comment2 = self.create_diff_comment(review, filediff)
        review.publish()
        review_request.local_site.users.add(user)
        self.assertTrue(self.client.login(username=b'test-user', password=b'test-user'))
        fragments = self._get_fragments(review_request, [
         comment1.pk, comment2.pk], local_site_name=b'local-site-1')
        self.assertEqual(len(fragments), 2)
        self.assertEqual(fragments[0][0], comment1.pk)
        self.assertEqual(fragments[1][0], comment2.pk)

    @add_fixtures([b'test_site'])
    def test_get_with_published_review_request_local_site_no_access(self):
        """Testing CommentDiffFragmentsView with published review request on
        a Local Site the user does not have access to
        """
        User.objects.create_user(username=b'test-user', password=b'test-user', email=b'user@example.com')
        review_request = self.create_review_request(create_repository=True, with_local_site=True, publish=True)
        diffset = self.create_diffset(review_request)
        filediff = self.create_filediff(diffset)
        review = self.create_review(review_request)
        comment1 = self.create_diff_comment(review, filediff)
        comment2 = self.create_diff_comment(review, filediff)
        review.publish()
        self.assertTrue(self.client.login(username=b'test-user', password=b'test-user'))
        self._get_fragments(review_request, [
         comment1.pk, comment2.pk], local_site_name=b'local-site-1', expected_status=403)

    def test_get_with_unicode(self):
        """Testing CommentDiffFragmentsView with Unicode content"""
        user = User.objects.create(username=b'reviewer')
        repository = self.create_repository(tool_name=b'Test')
        review_request = self.create_review_request(repository=repository, publish=True)
        diffset = self.create_diffset(review_request)
        filediff = self.create_filediff(diffset, source_file=b'/data:áéíóú🔥', dest_file=b'/data:ÄËÏÖÜŸ', diff=(b'diff --git a/data b/data\nindex abcd123..abcd124 100644\n--- a/data\n+++ b/data\n@@ -1,1 +1,1 @@\n-áéíóú🔥\n+ÄËÏÖÜŸ\n').encode(b'utf-8'))
        review = self.create_review(review_request, user=user)
        comment1 = self.create_diff_comment(review, filediff)
        comment2 = self.create_diff_comment(review, filediff)
        review.publish()
        fragments = self._get_fragments(review_request, [
         comment1.pk, comment2.pk])
        self.assertEqual(len(fragments), 2)
        comment_id, html = fragments[0]
        self.assertEqual(comment_id, comment1.pk)
        self.assertTrue(html.startswith(b'<table class="sidebyside'))
        self.assertTrue(html.endswith(b'</table>'))
        self.assertIn(b'áéíóú🔥', html)
        comment_id, html = fragments[1]
        self.assertEqual(comment_id, comment2.pk)
        self.assertTrue(html.startswith(b'<table class="sidebyside'))
        self.assertTrue(html.endswith(b'</table>'))
        self.assertIn(b'ÄËÏÖÜŸ', html)

    def test_get_with_valid_comment_ids(self):
        """Testing CommentDiffFragmentsView with valid comment ID"""
        user = User.objects.create_user(username=b'reviewer', email=b'reviewer@example.com')
        review_request = self.create_review_request(create_repository=True, publish=True)
        diffset = self.create_diffset(review_request)
        filediff = self.create_filediff(diffset)
        review = self.create_review(review_request, user=user)
        comment1 = self.create_diff_comment(review, filediff)
        comment2 = self.create_diff_comment(review, filediff)
        review.publish()
        fragments = self._get_fragments(review_request, [
         comment1.pk, comment2.pk])
        self.assertEqual(len(fragments), 2)
        self.assertEqual(fragments[0][0], comment1.pk)
        self.assertEqual(fragments[1][0], comment2.pk)

    def test_get_with_valid_and_invalid_comment_ids(self):
        """Testing CommentDiffFragmentsView with mix of valid comment IDs and
        comment IDs not found in database
        """
        user = User.objects.create_user(username=b'reviewer', email=b'reviewer@example.com')
        review_request = self.create_review_request(create_repository=True, publish=True)
        diffset = self.create_diffset(review_request)
        filediff = self.create_filediff(diffset)
        review = self.create_review(review_request, user=user)
        comment = self.create_diff_comment(review, filediff)
        review.publish()
        fragments = self._get_fragments(review_request, [999, comment.pk])
        self.assertEqual(len(fragments), 1)
        self.assertEqual(fragments[0][0], comment.pk)

    def test_get_with_no_valid_comment_ids(self):
        """Testing CommentDiffFragmentsView with no valid comment IDs"""
        review_request = self.create_review_request(create_repository=True, publish=True)
        self._get_fragments(review_request, [
         100, 200, 300], expected_status=404)

    def test_get_with_comment_ids_from_other_review_request(self):
        """Testing CommentDiffFragmentsView with comment ID from another review
        request
        """
        user = User.objects.create_user(username=b'reviewer', email=b'reviewer@example.com')
        review_request1 = self.create_review_request(create_repository=True, publish=True)
        diffset = self.create_diffset(review_request1)
        filediff = self.create_filediff(diffset)
        review = self.create_review(review_request1, user=user)
        comment1 = self.create_diff_comment(review, filediff)
        review.publish()
        review_request2 = self.create_review_request(create_repository=True, publish=True)
        diffset = self.create_diffset(review_request2)
        filediff = self.create_filediff(diffset)
        review = self.create_review(review_request2, user=user)
        comment2 = self.create_diff_comment(review, filediff)
        review.publish()
        fragments = self._get_fragments(review_request1, [
         comment1.pk, comment2.pk])
        self.assertEqual(len(fragments), 1)
        self.assertEqual(fragments[0][0], comment1.pk)

    def test_get_with_comment_ids_from_draft_review_owner(self):
        """Testing CommentDiffFragmentsView with comment ID from draft review,
        accessed by the review's owner
        """
        user = User.objects.create_user(username=b'reviewer', password=b'reviewer', email=b'reviewer@example.com')
        review_request1 = self.create_review_request(create_repository=True, publish=True)
        diffset = self.create_diffset(review_request1)
        filediff = self.create_filediff(diffset)
        review = self.create_review(review_request1, user=user)
        comment = self.create_diff_comment(review, filediff)
        self.assertTrue(self.client.login(username=b'reviewer', password=b'reviewer'))
        fragments = self._get_fragments(review_request1, [comment.pk])
        self.assertEqual(len(fragments), 1)
        self.assertEqual(fragments[0][0], comment.pk)

    def test_get_with_comment_ids_from_draft_review_not_owner(self):
        """Testing CommentDiffFragmentsView with comment ID from draft review,
        accessed by someone other than the review's owner
        """
        user = User.objects.create_user(username=b'reviewer', email=b'reviewer@example.com')
        review_request1 = self.create_review_request(create_repository=True, publish=True)
        diffset = self.create_diffset(review_request1)
        filediff = self.create_filediff(diffset)
        review = self.create_review(review_request1, user=user)
        comment = self.create_diff_comment(review, filediff)
        self._get_fragments(review_request1, [
         comment.pk], expected_status=404)

    def _get_fragments(self, review_request, comment_ids, local_site_name=None, expected_status=200):
        """Load and return fragments from the server.

        Args:
            review_request (reviewboard.reviews.models.review_request.
                            ReviewRequest):
                The review request the comments were made on.

            comment_ids (list of int):
                The list of comment IDs to load.

            local_site_name (unicode, optional):
                The name of the Local Site for the URL.

            expected_status (int, optional):
                The expected HTTP status code. By default, this is a
                successful 200.

        Returns:
            list of tuple:
            A list of ``(comment_id, html)`` from the parsed payload, if
            the status code was 200.
        """
        response = self.client.get(local_site_reverse(b'diff-comment-fragments', kwargs={b'review_request_id': review_request.display_id, 
           b'comment_ids': (b',').join(six.text_type(comment_id) for comment_id in comment_ids)}, local_site_name=local_site_name))
        self.assertEqual(response.status_code, expected_status)
        if expected_status != 200:
            return None
        else:
            content = response.content
            self.assertIs(type(content), bytes)
            i = 0
            results = []
            while i < len(content):
                comment_id = struct.unpack_from(b'<L', content, i)[0]
                i += 4
                html_len = struct.unpack_from(b'<L', content, i)[0]
                i += 4
                html = content[i:i + html_len].decode(b'utf-8')
                i += html_len
                results.append((comment_id, html))

            return results