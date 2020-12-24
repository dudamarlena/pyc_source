# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/reviewboard/webapi/tests/test_screenshot_comment.py
# Compiled at: 2020-02-11 04:03:57
from __future__ import unicode_literals
from django.utils import six
from reviewboard.webapi.resources import resources
from reviewboard.webapi.tests.base import BaseWebAPITestCase
from reviewboard.webapi.tests.mimetypes import screenshot_comment_list_mimetype
from reviewboard.webapi.tests.mixins import BasicTestsMetaclass, ReviewRequestChildListMixin
from reviewboard.webapi.tests.urls import get_screenshot_comment_list_url

@six.add_metaclass(BasicTestsMetaclass)
class ResourceListTests(ReviewRequestChildListMixin, BaseWebAPITestCase):
    """Testing the ScreenshotCommentResource list APIs."""
    fixtures = [
     b'test_users']
    sample_api_url = b'review-requests/<id>/screenshots/<id>/comments/'
    resource = resources.screenshot_comment

    def setup_review_request_child_test(self, review_request):
        screenshot = self.create_screenshot(review_request)
        return (
         get_screenshot_comment_list_url(screenshot),
         screenshot_comment_list_mimetype)

    def setup_http_not_allowed_list_test(self, user):
        review_request = self.create_review_request(submitter=user, publish=True)
        screenshot = self.create_screenshot(review_request)
        return get_screenshot_comment_list_url(screenshot)

    def compare_item(self, item_rsp, comment):
        self.assertEqual(item_rsp[b'id'], comment.pk)
        self.assertEqual(item_rsp[b'text'], comment.text)
        self.assertEqual(item_rsp[b'issue_opened'], comment.issue_opened)
        self.assertEqual(item_rsp[b'x'], comment.x)
        self.assertEqual(item_rsp[b'y'], comment.y)
        self.assertEqual(item_rsp[b'w'], comment.w)
        self.assertEqual(item_rsp[b'h'], comment.h)

    def setup_basic_get_test(self, user, with_local_site, local_site_name, populate_items):
        review_request = self.create_review_request(with_local_site=with_local_site, submitter=user, publish=True)
        screenshot = self.create_screenshot(review_request)
        if populate_items:
            review = self.create_review(review_request, publish=True)
            items = [self.create_screenshot_comment(review, screenshot)]
        else:
            items = []
        return (
         get_screenshot_comment_list_url(screenshot, local_site_name),
         screenshot_comment_list_mimetype,
         items)


ResourceItemTests = None