# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/reviewboard/reviews/tests/test_review_request_detail_view.py
# Compiled at: 2020-02-11 04:03:56
"""Unit tests for reviewboard.reviews.views.ReviewRequestDetailView."""
from __future__ import unicode_literals
from datetime import timedelta
from django.contrib.auth.models import User
from django.test.html import parse_html
from django.utils import six
from djblets.extensions.hooks import TemplateHook
from djblets.extensions.models import RegisteredExtension
from djblets.siteconfig.models import SiteConfiguration
from kgb import SpyAgency
from reviewboard.extensions.base import Extension, get_extension_manager
from reviewboard.reviews.detail import InitialStatusUpdatesEntry, ReviewEntry
from reviewboard.reviews.fields import get_review_request_fieldsets
from reviewboard.reviews.models import Comment, GeneralComment, Review
from reviewboard.site.urlresolvers import local_site_reverse
from reviewboard.testing import TestCase

class ReviewRequestDetailViewTests(SpyAgency, TestCase):
    """Unit tests for reviewboard.reviews.views.ReviewRequestDetailView."""
    fixtures = [
     b'test_users', b'test_scmtools', b'test_site']

    def test_get(self):
        """Testing ReviewRequestDetailView.get"""
        review_request = self.create_review_request(publish=True)
        response = self.client.get(b'/r/%d/' % review_request.id)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context[b'review_request'].pk, review_request.pk)

    def test_context(self):
        """Testing ReviewRequestDetailView context variables"""
        self.client.login(username=b'admin', password=b'admin')
        username = b'admin'
        summary = b'This is a test summary'
        description = b'This is my description'
        testing_done = b'Some testing'
        review_request = self.create_review_request(publish=True, submitter=username, summary=summary, description=description, testing_done=testing_done)
        response = self.client.get(b'/r/%s/' % review_request.pk)
        self.assertEqual(response.status_code, 200)
        review_request = response.context[b'review_request']
        self.assertEqual(review_request.submitter.username, username)
        self.assertEqual(review_request.summary, summary)
        self.assertEqual(review_request.description, description)
        self.assertEqual(review_request.testing_done, testing_done)
        self.assertEqual(review_request.pk, review_request.pk)

    def test_diff_comment_ordering(self):
        """Testing ReviewRequestDetailView and ordering of diff comments on a
        review
        """
        comment_text_1 = b'Comment text 1'
        comment_text_2 = b'Comment text 2'
        comment_text_3 = b'Comment text 3'
        review_request = self.create_review_request(create_repository=True, publish=True)
        diffset = self.create_diffset(review_request)
        filediff = self.create_filediff(diffset)
        user1 = User.objects.get(username=b'doc')
        user2 = User.objects.get(username=b'dopey')
        main_review = self.create_review(review_request, user=user1)
        main_comment = self.create_diff_comment(main_review, filediff, text=comment_text_1)
        main_review.publish()
        reply1 = self.create_reply(main_review, user=user1, timestamp=main_review.timestamp + timedelta(days=1))
        self.create_diff_comment(reply1, filediff, text=comment_text_2, reply_to=main_comment)
        reply2 = self.create_reply(main_review, user=user2, timestamp=main_review.timestamp + timedelta(days=2))
        self.create_diff_comment(reply2, filediff, text=comment_text_3, reply_to=main_comment)
        reply2.publish()
        reply1.publish()
        self.assertTrue(reply1.timestamp > reply2.timestamp)
        comments = list(Comment.objects.filter(review__review_request=review_request).order_by(b'timestamp'))
        self.assertEqual(len(comments), 3)
        self.assertEqual(comments[0].text, comment_text_1)
        self.assertEqual(comments[1].text, comment_text_3)
        self.assertEqual(comments[2].text, comment_text_2)
        response = self.client.get(b'/r/%d/' % review_request.pk)
        self.assertEqual(response.status_code, 200)
        entries = response.context[b'entries']
        initial_entries = entries[b'initial']
        self.assertEqual(len(initial_entries), 1)
        self.assertIsInstance(initial_entries[0], InitialStatusUpdatesEntry)
        main_entries = entries[b'main']
        self.assertEqual(len(main_entries), 1)
        entry = main_entries[0]
        self.assertIsInstance(entry, ReviewEntry)
        comments = entry.comments[b'diff_comments']
        self.assertEqual(len(comments), 1)
        self.assertEqual(comments[0].text, comment_text_1)
        replies = comments[0].public_replies()
        self.assertEqual(len(replies), 2)
        self.assertEqual(replies[0].text, comment_text_3)
        self.assertEqual(replies[1].text, comment_text_2)

    def test_general_comment_ordering(self):
        """Testing ReviewRequestDetailView and ordering of general comments on
        a review
        """
        comment_text_1 = b'Comment text 1'
        comment_text_2 = b'Comment text 2'
        comment_text_3 = b'Comment text 3'
        review_request = self.create_review_request(create_repository=True, publish=True)
        user1 = User.objects.get(username=b'doc')
        user2 = User.objects.get(username=b'dopey')
        main_review = self.create_review(review_request, user=user1)
        main_comment = self.create_general_comment(main_review, text=comment_text_1)
        main_review.publish()
        reply1 = self.create_reply(main_review, user=user1, timestamp=main_review.timestamp + timedelta(days=1))
        self.create_general_comment(reply1, text=comment_text_2, reply_to=main_comment)
        reply2 = self.create_reply(main_review, user=user2, timestamp=main_review.timestamp + timedelta(days=2))
        self.create_general_comment(reply2, text=comment_text_3, reply_to=main_comment)
        reply2.publish()
        reply1.publish()
        self.assertTrue(reply1.timestamp > reply2.timestamp)
        comments = list(GeneralComment.objects.filter(review__review_request=review_request).order_by(b'timestamp'))
        self.assertEqual(len(comments), 3)
        self.assertEqual(comments[0].text, comment_text_1)
        self.assertEqual(comments[1].text, comment_text_3)
        self.assertEqual(comments[2].text, comment_text_2)

    def test_file_attachments_visibility(self):
        """Testing ReviewRequestDetailView default visibility of file
        attachments
        """
        caption_1 = b'File Attachment 1'
        caption_2 = b'File Attachment 2'
        caption_3 = b'File Attachment 3'
        comment_text_1 = b'Comment text 1'
        comment_text_2 = b'Comment text 2'
        user1 = User.objects.get(username=b'doc')
        review_request = self.create_review_request()
        file1 = self.create_file_attachment(review_request, caption=caption_1)
        file2 = self.create_file_attachment(review_request, caption=caption_2, active=False)
        review_request.publish(user1)
        self.create_file_attachment(review_request, caption=caption_3, draft=True)
        review = Review.objects.create(review_request=review_request, user=user1)
        review.file_attachment_comments.create(file_attachment=file1, text=comment_text_1)
        review.file_attachment_comments.create(file_attachment=file2, text=comment_text_2)
        review.publish()
        self.client.login(username=b'doc', password=b'doc')
        response = self.client.get(b'/r/%d/' % review_request.pk)
        self.assertEqual(response.status_code, 200)
        file_attachments = response.context[b'file_attachments']
        self.assertEqual(len(file_attachments), 2)
        self.assertEqual(file_attachments[0].caption, caption_1)
        self.assertEqual(file_attachments[1].caption, caption_3)
        self.client.logout()
        response = self.client.get(b'/r/%d/' % review_request.pk)
        self.assertEqual(response.status_code, 200)
        file_attachments = response.context[b'file_attachments']
        self.assertEqual(len(file_attachments), 1)
        self.assertEqual(file_attachments[0].caption, caption_1)
        entries = response.context[b'entries']
        initial_entries = entries[b'initial']
        self.assertEqual(len(initial_entries), 1)
        self.assertIsInstance(initial_entries[0], InitialStatusUpdatesEntry)
        main_entries = entries[b'main']
        self.assertEqual(len(main_entries), 1)
        entry = main_entries[0]
        self.assertIsInstance(entry, ReviewEntry)
        comments = entry.comments[b'file_attachment_comments']
        self.assertEqual(len(comments), 2)
        self.assertEqual(comments[0].text, comment_text_1)
        self.assertEqual(comments[1].text, comment_text_2)

    def test_screenshots_visibility(self):
        """Testing ReviewRequestDetailView default visibility of screenshots"""
        caption_1 = b'Screenshot 1'
        caption_2 = b'Screenshot 2'
        caption_3 = b'Screenshot 3'
        comment_text_1 = b'Comment text 1'
        comment_text_2 = b'Comment text 2'
        user1 = User.objects.get(username=b'doc')
        review_request = self.create_review_request()
        screenshot1 = self.create_screenshot(review_request, caption=caption_1)
        screenshot2 = self.create_screenshot(review_request, caption=caption_2, active=False)
        review_request.publish(user1)
        self.create_screenshot(review_request, caption=caption_3, draft=True)
        user1 = User.objects.get(username=b'doc')
        review = Review.objects.create(review_request=review_request, user=user1)
        review.screenshot_comments.create(screenshot=screenshot1, text=comment_text_1, x=10, y=10, w=20, h=20)
        review.screenshot_comments.create(screenshot=screenshot2, text=comment_text_2, x=0, y=0, w=10, h=10)
        review.publish()
        self.client.login(username=b'doc', password=b'doc')
        response = self.client.get(b'/r/%d/' % review_request.pk)
        self.assertEqual(response.status_code, 200)
        screenshots = response.context[b'screenshots']
        self.assertEqual(len(screenshots), 2)
        self.assertEqual(screenshots[0].caption, caption_1)
        self.assertEqual(screenshots[1].caption, caption_3)
        self.client.logout()
        response = self.client.get(b'/r/%d/' % review_request.pk)
        self.assertEqual(response.status_code, 200)
        screenshots = response.context[b'screenshots']
        self.assertEqual(len(screenshots), 1)
        self.assertEqual(screenshots[0].caption, caption_1)
        entries = response.context[b'entries']
        initial_entries = entries[b'initial']
        self.assertEqual(len(initial_entries), 1)
        self.assertIsInstance(initial_entries[0], InitialStatusUpdatesEntry)
        main_entries = entries[b'main']
        self.assertEqual(len(main_entries), 1)
        entry = main_entries[0]
        self.assertIsInstance(entry, ReviewEntry)
        comments = entry.comments[b'screenshot_comments']
        self.assertEqual(len(comments), 2)
        self.assertEqual(comments[0].text, comment_text_1)
        self.assertEqual(comments[1].text, comment_text_2)

    def test_with_anonymous_and_requires_site_wide_login(self):
        """Testing ReviewRequestDetailView with anonymous user and site-wide
        login required
        """
        with self.siteconfig_settings({b'auth_require_sitewide_login': True}, reload_settings=False):
            self.create_review_request(publish=True)
            response = self.client.get(b'/r/1/')
            self.assertEqual(response.status_code, 302)

    def test_etag_with_issues(self):
        """Testing ReviewRequestDetailView ETags with issue status toggling"""
        self.client.login(username=b'doc', password=b'doc')
        user = User.objects.get(username=b'doc')
        review_request = self.create_review_request(create_repository=True, publish=True)
        diffset = self.create_diffset(review_request)
        filediff = self.create_filediff(diffset)
        review = self.create_review(review_request, user=user)
        comment = self.create_diff_comment(review, filediff, issue_opened=True)
        review.publish()
        response = self.client.get(review_request.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        etag1 = response[b'ETag']
        self.assertNotEqual(etag1, b'')
        comment.issue_status = Comment.RESOLVED
        comment.save()
        response = self.client.get(review_request.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        etag2 = response[b'ETag']
        self.assertNotEqual(etag2, b'')
        self.assertNotEqual(etag1, etag2)

    def test_review_request_box_template_hooks(self):
        """Testing ReviewRequestDetailView template hooks for the review
        request box
        """

        class ContentTemplateHook(TemplateHook):

            def initialize(self, name, content):
                super(ContentTemplateHook, self).initialize(name)
                self.content = content

            def render_to_string(self, request, context):
                return self.content

        class TestExtension(Extension):
            registration = RegisteredExtension.objects.create(class_name=b'test-extension', name=b'test-extension', enabled=True, installed=True)

        extension = TestExtension(get_extension_manager())
        review_request = self.create_review_request(publish=True)
        hooks = []
        for name in ('before-review-request-summary', 'review-request-summary-pre',
                     'review-request-summary-post', 'after-review-request-summary-post',
                     'before-review-request-fields', 'after-review-request-fields',
                     'before-review-request-extra-panes', 'review-request-extra-panes-pre',
                     'review-request-extra-panes-post', 'after-review-request-extra-panes'):
            hooks.append(ContentTemplateHook(extension, name, b'[%s here]' % name))

        self.spy_on(get_review_request_fieldsets, call_fake=lambda *args, **kwargs: [])
        response = self.client.get(local_site_reverse(b'review-request-detail', args=[
         review_request.display_id]))
        self.assertEqual(response.status_code, 200)
        parsed_html = six.text_type(parse_html(response.content))
        self.assertIn(b'<div class="review-request-body">\n[before-review-request-summary here]', parsed_html)
        self.assertIn(b'<div class="review-request-section review-request-summary">\n[review-request-summary-pre here]', parsed_html)
        self.assertIn(b'</time>\n</p>[review-request-summary-post here]\n</div>', parsed_html)
        self.assertIn(b'[before-review-request-fields here]<table class="review-request-section" id="review-request-details">', parsed_html)
        self.assertIn(b'</div>[after-review-request-fields here] [before-review-request-extra-panes here]<div id="review-request-extra">\n[review-request-extra-panes-pre here]', parsed_html)
        self.assertIn(b'</div>[review-request-extra-panes-post here]\n</div>[after-review-request-extra-panes here]\n</div>', parsed_html)