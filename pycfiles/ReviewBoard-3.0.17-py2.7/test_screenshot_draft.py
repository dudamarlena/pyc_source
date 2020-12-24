# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/reviewboard/webapi/tests/test_screenshot_draft.py
# Compiled at: 2020-02-11 04:03:57
from __future__ import unicode_literals
from django.utils import six
from djblets.webapi.errors import PERMISSION_DENIED
from reviewboard.reviews.models import ReviewRequestDraft, Screenshot
from reviewboard.webapi.resources import resources
from reviewboard.webapi.tests.base import BaseWebAPITestCase
from reviewboard.webapi.tests.mimetypes import screenshot_draft_item_mimetype, screenshot_draft_list_mimetype
from reviewboard.webapi.tests.mixins import BasicTestsMetaclass
from reviewboard.webapi.tests.urls import get_screenshot_draft_item_url, get_screenshot_draft_list_url

@six.add_metaclass(BasicTestsMetaclass)
class ResourceListTests(BaseWebAPITestCase):
    """Testing the DraftScreenshotResource list APIs."""
    fixtures = [
     b'test_users']
    sample_api_url = b'review-requests/<id>/draft/screenshots/'
    resource = resources.draft_screenshot

    def compare_item(self, item_rsp, screenshot):
        self.assertEqual(item_rsp[b'id'], screenshot.pk)
        self.assertEqual(item_rsp[b'caption'], screenshot.caption)

    def setup_basic_get_test(self, user, with_local_site, local_site_name, populate_items):
        review_request = self.create_review_request(with_local_site=with_local_site, submitter=user, publish=True)
        if populate_items:
            items = [
             self.create_screenshot(review_request)]
            ReviewRequestDraft.create(review_request)
            items.append(self.create_screenshot(review_request, draft=True))
        else:
            items = []
        return (
         get_screenshot_draft_list_url(review_request, local_site_name),
         screenshot_draft_list_mimetype,
         items)

    def setup_basic_post_test(self, user, with_local_site, local_site_name, post_valid_data):
        review_request = self.create_review_request(with_local_site=with_local_site, submitter=user, publish=True)
        return (
         get_screenshot_draft_list_url(review_request, local_site_name),
         screenshot_draft_item_mimetype,
         {b'caption': b'Trophy', 
            b'path': open(self.get_sample_image_filename(), b'rb')},
         [
          review_request])

    def check_post_result(self, user, rsp, review_request):
        draft = review_request.get_draft()
        screenshots = list(draft.screenshots.all())
        self.assertEqual(len(screenshots), 1)
        self.assertEqual(draft.screenshots_count, 1)
        screenshot = screenshots[0]
        self.assertEqual(screenshot.draft_caption, b'Trophy')
        self.assertEqual(screenshot.caption, b'')

    def test_post_with_permission_denied_error(self):
        """Testing the POST review-requests/<id>/draft/screenshots/ API
        with Permission Denied error
        """
        review_request = self.create_review_request()
        self.assertNotEqual(review_request.submitter, self.user)
        with open(self.get_sample_image_filename(), b'rb') as (f):
            rsp = self.api_post(get_screenshot_draft_list_url(review_request), {b'caption': b'Trophy', 
               b'path': f}, expected_status=403)
        self.assertEqual(rsp[b'stat'], b'fail')
        self.assertEqual(rsp[b'err'][b'code'], PERMISSION_DENIED.code)


@six.add_metaclass(BasicTestsMetaclass)
class ResourceItemTests(BaseWebAPITestCase):
    """Testing the DraftScreenshotResource item APIs."""
    fixtures = [
     b'test_users']
    sample_api_url = b'review-requests/<id>/draft/screenshots/<id>/'
    resource = resources.draft_screenshot

    def compare_item(self, item_rsp, screenshot):
        self.assertEqual(item_rsp[b'id'], screenshot.pk)
        self.assertEqual(item_rsp[b'caption'], screenshot.caption)

    def setup_basic_delete_test(self, user, with_local_site, local_site_name):
        review_request = self.create_review_request(with_local_site=with_local_site, submitter=user, publish=True)
        screenshot = self.create_screenshot(review_request, draft=True)
        return (
         get_screenshot_draft_item_url(review_request, screenshot.pk, local_site_name),
         [
          screenshot, review_request])

    def check_delete_result(self, user, screenshot, review_request):
        self.assertNotIn(screenshot, review_request.get_draft().screenshots.all())

    def setup_basic_get_test(self, user, with_local_site, local_site_name):
        review_request = self.create_review_request(with_local_site=with_local_site, submitter=user, publish=True)
        screenshot = self.create_screenshot(review_request, draft=True)
        return (
         get_screenshot_draft_item_url(review_request, screenshot.pk, local_site_name),
         screenshot_draft_item_mimetype,
         screenshot)

    def setup_basic_put_test(self, user, with_local_site, local_site_name, put_valid_data):
        review_request = self.create_review_request(with_local_site=with_local_site, submitter=user, publish=True)
        screenshot = self.create_screenshot(review_request, draft=True)
        if put_valid_data:
            put_data = {b'caption': b'The new caption'}
        else:
            put_data = {}
        return (get_screenshot_draft_item_url(review_request, screenshot.pk, local_site_name),
         screenshot_draft_item_mimetype,
         put_data,
         screenshot,
         [
          review_request])

    def check_put_result(self, user, item_rsp, screenshot, review_request):
        screenshot = Screenshot.objects.get(pk=screenshot.pk)
        self.assertEqual(screenshot.draft_caption, b'The new caption')
        self.assertNotIn(screenshot, review_request.screenshots.all())
        self.assertIn(screenshot, review_request.get_draft().screenshots.all())