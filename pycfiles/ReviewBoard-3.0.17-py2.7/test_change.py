# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/reviewboard/webapi/tests/test_change.py
# Compiled at: 2020-02-11 04:03:57
from __future__ import unicode_literals
from datetime import timedelta
from django.contrib.auth.models import User
from django.core.files import File
from django.utils import six, timezone
from djblets.testing.decorators import add_fixtures
from djblets.webapi.errors import PERMISSION_DENIED
from reviewboard.changedescs.models import ChangeDescription
from reviewboard.reviews.models import Group, ReviewRequest, ReviewRequestDraft, Screenshot
from reviewboard.webapi.tests.base import BaseWebAPITestCase
from reviewboard.webapi.tests.mimetypes import change_item_mimetype, change_list_mimetype
from reviewboard.webapi.tests.mixins import ReviewRequestChildItemMixin, ReviewRequestChildListMixin
from reviewboard.webapi.tests.urls import get_change_item_url, get_change_list_url

class ResourceListTests(ReviewRequestChildListMixin, BaseWebAPITestCase):
    """Testing the ChangeResource list APIs."""
    fixtures = [
     b'test_users']
    sample_api_url = b'review-requests/<id>/changes/'

    def setup_review_request_child_test(self, review_request):
        return (
         get_change_list_url(review_request), change_list_mimetype)

    @add_fixtures([b'test_scmtools'])
    def test_get(self):
        """Testing the GET review-requests/<id>/changes/ API"""
        review_request = self.create_review_request(publish=True)
        now = timezone.now()
        change1 = ChangeDescription(public=True, timestamp=now)
        change1.record_field_change(b'summary', b'foo', b'bar')
        change1.save()
        review_request.changedescs.add(change1)
        change2 = ChangeDescription(public=True, timestamp=now + timedelta(seconds=1))
        change2.record_field_change(b'description', b'foo', b'bar')
        change2.save()
        review_request.changedescs.add(change2)
        rsp = self.api_get(get_change_list_url(review_request), expected_mimetype=change_list_mimetype)
        self.assertEqual(rsp[b'stat'], b'ok')
        self.assertEqual(len(rsp[b'changes']), 2)
        self.assertEqual(rsp[b'changes'][0][b'id'], change2.pk)
        self.assertEqual(rsp[b'changes'][1][b'id'], change1.pk)

    @add_fixtures([b'test_scmtools'])
    def test_get_with_status_change(self):
        """Testing the GET review-requests/<id>/changes/ API
        with review request status changes.
        """
        review_request = self.create_review_request(publish=True)
        review_request.close(ReviewRequest.SUBMITTED, description=b'Closed!')
        rsp = self.api_get(get_change_list_url(review_request), expected_mimetype=change_list_mimetype)
        self.assertEqual(rsp[b'stat'], b'ok')
        self.assertEqual(len(rsp[b'changes']), 1)
        self.assertTrue(b'status' in rsp[b'changes'][0][b'fields_changed'])

    @add_fixtures([b'test_site'])
    def test_get_with_site(self):
        """Testing the GET review-requests/<id>/changes/ API
        with access to a local site
        """
        review_request = self.create_review_request(publish=True, with_local_site=True)
        self._login_user(local_site=True)
        now = timezone.now()
        change1 = ChangeDescription(public=True, timestamp=now)
        change1.record_field_change(b'summary', b'foo', b'bar')
        change1.save()
        review_request.changedescs.add(change1)
        change2 = ChangeDescription(public=True, timestamp=now + timedelta(seconds=1))
        change2.record_field_change(b'description', b'foo', b'bar')
        change2.save()
        review_request.changedescs.add(change2)
        rsp = self.api_get(get_change_list_url(review_request, self.local_site_name), expected_mimetype=change_list_mimetype)
        self.assertEqual(rsp[b'stat'], b'ok')
        self.assertEqual(len(rsp[b'changes']), 2)
        self.assertEqual(rsp[b'changes'][0][b'id'], change2.pk)
        self.assertEqual(rsp[b'changes'][1][b'id'], change1.pk)

    @add_fixtures([b'test_site'])
    def test_get_with_site_no_access(self):
        """Testing the GET review-requests/<id>/changes/ API
        without access to a local site
        """
        review_request = self.create_review_request(publish=True, with_local_site=True)
        rsp = self.api_get(get_change_list_url(review_request, self.local_site_name), expected_status=403)
        self.assertEqual(rsp[b'stat'], b'fail')
        self.assertEqual(rsp[b'err'][b'code'], PERMISSION_DENIED.code)

    def test_post_method_not_allowed(self):
        """Testing the POST review-requests/<id>/changes/ API
        gives Method Not Allowed
        """
        review_request = self.create_review_request()
        self.api_post(get_change_list_url(review_request), expected_status=405)


class ResourceItemTests(ReviewRequestChildItemMixin, BaseWebAPITestCase):
    """Testing the ChangeResource item APIs."""
    fixtures = [
     b'test_users']
    sample_api_url = b'review-requests/<id>/changes/<id>/'

    def setup_review_request_child_test(self, review_request):
        change = ChangeDescription.objects.create(public=True)
        review_request.changedescs.add(change)
        return (
         get_change_item_url(change), change_item_mimetype)

    def test_delete_method_not_allowed(self):
        """Testing the DELETE review-requests/<id>/changes/ API
        gives Method Not Allowed
        """
        review_request = self.create_review_request()
        change = ChangeDescription.objects.create(public=True)
        review_request.changedescs.add(change)
        self.api_delete(get_change_item_url(change), expected_status=405)

    @add_fixtures([b'test_scmtools'])
    def test_get(self):
        """Testing the GET review-requests/<id>/changes/<id>/ API"""

        def write_fields(obj, index):
            for field, data in six.iteritems(test_data):
                value = data[index]
                if isinstance(value, list) and field not in model_fields:
                    value = (b',').join(value)
                if field == b'diff':
                    field = b'diffset'
                setattr(obj, field, value)

        changedesc_text = b'Change description text'
        user1, user2 = User.objects.all()[:2]
        group1 = Group.objects.create(name=b'group1')
        group2 = Group.objects.create(name=b'group2')
        repository = self.create_repository()
        diff1 = self.create_diffset(revision=1, repository=repository)
        diff2 = self.create_diffset(revision=2, repository=repository)
        old_screenshot_caption = b'old screenshot'
        new_screenshot_caption = b'new screenshot'
        screenshot1 = Screenshot.objects.create()
        screenshot2 = Screenshot.objects.create()
        screenshot3 = Screenshot.objects.create(caption=old_screenshot_caption)
        for screenshot in [screenshot1, screenshot2, screenshot3]:
            with open(self.get_sample_image_filename(), b'rb') as (f):
                screenshot.image.save(b'foo.png', File(f), save=True)

        test_data = {b'summary': ('old summary', 'new summary', None, None), b'description': ('old description', 'new description', None, None), 
           b'testing_done': ('old testing done', 'new testing done', None, None), 
           b'branch': ('old branch', 'new branch', None, None), 
           b'bugs_closed': (
                          [
                           b'1', b'2', b'3'], [b'2', b'3', b'4'], [b'1'], [b'4']), 
           b'target_people': (
                            [
                             user1], [user2], [user1], [user2]), 
           b'target_groups': (
                            [
                             group1], [group2], [group1], [group2]), 
           b'screenshots': (
                          [
                           screenshot1, screenshot3],
                          [
                           screenshot2, screenshot3],
                          [
                           screenshot1],
                          [
                           screenshot2]), 
           b'diff': (
                   diff1, diff2, None, diff2)}
        model_fields = ('target_people', 'target_groups', 'screenshots', 'diff')
        r = self.create_review_request(submitter=self.user)
        write_fields(r, 0)
        r.publish(self.user)
        draft = ReviewRequestDraft.create(r)
        write_fields(draft, 1)
        draft.inactive_screenshots = test_data[b'screenshots'][2]
        screenshot3.draft_caption = new_screenshot_caption
        screenshot3.save()
        draft.changedesc.text = changedesc_text
        draft.changedesc.save()
        draft.save()
        r.publish(self.user)
        self.assertEqual(r.changedescs.count(), 1)
        change = r.changedescs.get()
        self.assertEqual(change.text, changedesc_text)
        for field, data in six.iteritems(test_data):
            old, new, removed, added = data
            field_data = change.fields_changed[field]
            if field == b'diff':
                self.assertEqual(len(field_data[b'added']), 1)
                self.assertEqual(field_data[b'added'][0][2], added.pk)
            elif field in model_fields:
                self.assertEqual([ item[2] for item in field_data[b'old'] ], [ obj.pk for obj in old ])
                self.assertEqual([ item[2] for item in field_data[b'new'] ], [ obj.pk for obj in new ])
                self.assertEqual([ item[2] for item in field_data[b'removed'] ], [ obj.pk for obj in removed ])
                self.assertEqual([ item[2] for item in field_data[b'added'] ], [ obj.pk for obj in added ])
            elif isinstance(old, list):
                self.assertEqual(field_data[b'old'], [ [value] for value in old ])
                self.assertEqual(field_data[b'new'], [ [value] for value in new ])
                self.assertEqual(field_data[b'removed'], [ [value] for value in removed ])
                self.assertEqual(field_data[b'added'], [ [value] for value in added ])
            else:
                self.assertEqual(field_data[b'old'], [old])
                self.assertEqual(field_data[b'new'], [new])
                self.assertNotIn(b'removed', field_data)
                self.assertNotIn(b'added', field_data)

        self.assertIn(b'screenshot_captions', change.fields_changed)
        field_data = change.fields_changed[b'screenshot_captions']
        screenshot_id = six.text_type(screenshot3.pk)
        self.assertIn(screenshot_id, field_data)
        self.assertIn(b'old', field_data[screenshot_id])
        self.assertIn(b'new', field_data[screenshot_id])
        self.assertEqual(field_data[screenshot_id][b'old'][0], old_screenshot_caption)
        self.assertEqual(field_data[screenshot_id][b'new'][0], new_screenshot_caption)
        rsp = self.api_get(get_change_list_url(r), expected_mimetype=change_list_mimetype)
        self.assertEqual(rsp[b'stat'], b'ok')
        self.assertEqual(len(rsp[b'changes']), 1)
        self.assertEqual(rsp[b'changes'][0][b'id'], change.pk)
        rsp = self.api_get(rsp[b'changes'][0][b'links'][b'self'][b'href'], expected_mimetype=change_item_mimetype)
        self.assertEqual(rsp[b'stat'], b'ok')
        self.assertEqual(rsp[b'change'][b'text'], changedesc_text)
        fields_changed = rsp[b'change'][b'fields_changed']
        for field, data in six.iteritems(test_data):
            old, new, removed, added = data
            self.assertIn(field, fields_changed)
            field_data = fields_changed[field]
            if field == b'diff':
                self.assertIn(b'added', field_data)
                self.assertEqual(field_data[b'added'][b'id'], added.pk)
            elif field in model_fields:
                self.assertIn(b'old', field_data)
                self.assertIn(b'new', field_data)
                self.assertIn(b'added', field_data)
                self.assertIn(b'removed', field_data)
                self.assertEqual([ item[b'id'] for item in field_data[b'old'] ], [ obj.pk for obj in old ])
                self.assertEqual([ item[b'id'] for item in field_data[b'new'] ], [ obj.pk for obj in new ])
                self.assertEqual([ item[b'id'] for item in field_data[b'removed'] ], [ obj.pk for obj in removed ])
                self.assertEqual([ item[b'id'] for item in field_data[b'added'] ], [ obj.pk for obj in added ])
            else:
                self.assertIn(b'old', field_data)
                self.assertIn(b'new', field_data)
                self.assertEqual(field_data[b'old'], old)
                self.assertEqual(field_data[b'new'], new)
                if isinstance(old, list):
                    self.assertIn(b'added', field_data)
                    self.assertIn(b'removed', field_data)
                    self.assertEqual(field_data[b'added'], added)
                    self.assertEqual(field_data[b'removed'], removed)

        self.assertIn(b'screenshot_captions', fields_changed)
        field_data = fields_changed[b'screenshot_captions']
        self.assertEqual(len(field_data), 1)
        screenshot_data = field_data[0]
        self.assertIn(b'old', screenshot_data)
        self.assertIn(b'new', screenshot_data)
        self.assertIn(b'screenshot', screenshot_data)
        self.assertEqual(screenshot_data[b'old'], old_screenshot_caption)
        self.assertEqual(screenshot_data[b'new'], new_screenshot_caption)
        self.assertEqual(screenshot_data[b'screenshot'][b'id'], screenshot3.pk)
        return

    @add_fixtures([b'test_site'])
    def test_get_with_site(self):
        """Testing the GET review-requests/<id>/changes/<id>/ API
        with access to a local site
        """
        review_request = self.create_review_request(publish=True, with_local_site=True)
        self._login_user(local_site=True)
        now = timezone.now()
        change = ChangeDescription(public=True, timestamp=now)
        change.record_field_change(b'summary', b'foo', b'bar')
        change.save()
        review_request.changedescs.add(change)
        rsp = self.api_get(get_change_item_url(change, self.local_site_name), expected_mimetype=change_item_mimetype)
        self.assertEqual(rsp[b'stat'], b'ok')
        self.assertEqual(rsp[b'change'][b'id'], change.pk)

    @add_fixtures([b'test_site'])
    def test_get_with_site_no_access(self):
        """Testing the GET review-requests/<id>/changes/<id>/ API
        without access to a local site
        """
        review_request = self.create_review_request(publish=True, with_local_site=True)
        now = timezone.now()
        change = ChangeDescription(public=True, timestamp=now)
        change.record_field_change(b'summary', b'foo', b'bar')
        change.save()
        review_request.changedescs.add(change)
        rsp = self.api_get(get_change_item_url(change, self.local_site_name), expected_status=403)
        self.assertEqual(rsp[b'stat'], b'fail')
        self.assertEqual(rsp[b'err'][b'code'], PERMISSION_DENIED.code)

    def test_get_not_modified(self):
        """Testing the GET review-requests/<id>/changes/<id>/ API
        with Not Modified response
        """
        review_request = self.create_review_request(publish=True)
        changedesc = ChangeDescription.objects.create(public=True)
        review_request.changedescs.add(changedesc)
        self._testHttpCaching(get_change_item_url(changedesc), check_etags=True)

    def test_put_method_not_allowed(self):
        """Testing the PUT review-requests/<id>/changes/ API
        gives Method Not Allowed
        """
        review_request = self.create_review_request()
        change = ChangeDescription.objects.create(public=True)
        review_request.changedescs.add(change)
        self.api_put(get_change_item_url(change), {}, expected_status=405)