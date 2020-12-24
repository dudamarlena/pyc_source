# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/reviewboard/webapi/tests/test_review.py
# Compiled at: 2020-02-11 04:03:57
from __future__ import unicode_literals
from datetime import datetime, timedelta
from django.core import mail
from django.utils import six, timezone
from djblets.util.dates import get_tz_aware_utcnow
from djblets.testing.decorators import add_fixtures
from djblets.webapi.errors import DOES_NOT_EXIST, INVALID_FORM_DATA, PERMISSION_DENIED
from djblets.webapi.testing.decorators import webapi_test_template
from kgb import SpyAgency, spy_on
from reviewboard.reviews.models import Review, ReviewRequest
from reviewboard.reviews.signals import review_ship_it_revoking
from reviewboard.webapi.errors import REVOKE_SHIP_IT_ERROR
from reviewboard.webapi.resources import resources
from reviewboard.webapi.tests.base import BaseWebAPITestCase
from reviewboard.webapi.tests.mimetypes import review_list_mimetype, review_item_mimetype
from reviewboard.webapi.tests.mixins import BasicTestsMetaclass, ReviewRequestChildItemMixin, ReviewRequestChildListMixin
from reviewboard.webapi.tests.mixins_review import ReviewItemMixin, ReviewListMixin
from reviewboard.webapi.tests.urls import get_review_item_url, get_review_list_url

@six.add_metaclass(BasicTestsMetaclass)
class ResourceListTests(ReviewListMixin, ReviewRequestChildListMixin, BaseWebAPITestCase):
    """Testing the ReviewResource list APIs."""
    fixtures = [
     b'test_users']
    sample_api_url = b'review-requests/<id>/reviews/'
    resource = resources.review

    def setup_review_request_child_test(self, review_request):
        return (
         get_review_list_url(review_request),
         review_list_mimetype)

    def compare_item(self, item_rsp, review):
        self.assertEqual(item_rsp[b'id'], review.pk)
        self.assertEqual(item_rsp[b'ship_it'], review.ship_it)
        self.assertEqual(item_rsp[b'body_top'], review.body_top)
        self.assertEqual(item_rsp[b'body_bottom'], review.body_bottom)
        if review.body_top_rich_text:
            self.assertEqual(item_rsp[b'body_top_text_type'], b'markdown')
        else:
            self.assertEqual(item_rsp[b'body_top_text_type'], b'plain')
        if review.body_bottom_rich_text:
            self.assertEqual(item_rsp[b'body_bottom_text_type'], b'markdown')
        else:
            self.assertEqual(item_rsp[b'body_bottom_text_type'], b'plain')
        self.assertEqual(item_rsp[b'absolute_url'], self.base_url + review.get_absolute_url())

    def setup_basic_get_test(self, user, with_local_site, local_site_name, populate_items):
        review_request = self.create_review_request(with_local_site=with_local_site, submitter=user, publish=True)
        if populate_items:
            items = [
             self.create_review(review_request, publish=True)]
        else:
            items = []
        return (
         get_review_list_url(review_request, local_site_name),
         review_list_mimetype,
         items)

    def test_get_with_counts_only(self):
        """Testing the GET review-requests/<id>/reviews/?counts-only=1 API"""
        review_request = self.create_review_request(publish=True)
        self.create_review(review_request, publish=True)
        self.create_review(review_request, publish=True)
        rsp = self.api_get(get_review_list_url(review_request), {b'counts-only': 1}, expected_mimetype=review_list_mimetype)
        self.assertEqual(rsp[b'stat'], b'ok')
        self.assertEqual(rsp[b'count'], 2)

    def test_get_with_invite_only_group_and_permission_denied_error(self):
        """Testing the GET review-requests/<id>/reviews/ API
        with invite-only group and Permission Denied error
        """
        review_request = self.create_review_request(publish=True)
        self.assertNotEqual(review_request.submitter, self.user)
        group = self.create_review_group(invite_only=True)
        review_request.target_groups.add(group)
        review_request.save()
        rsp = self.api_get(get_review_list_url(review_request), expected_status=403)
        self.assertEqual(rsp[b'stat'], b'fail')
        self.assertEqual(rsp[b'err'][b'code'], PERMISSION_DENIED.code)

    def setup_basic_post_test(self, user, with_local_site, local_site_name, post_valid_data):
        review_request = self.create_review_request(with_local_site=with_local_site, submitter=user, publish=True)
        return (
         get_review_list_url(review_request, local_site_name),
         review_item_mimetype,
         {b'ship_it': True, 
            b'body_top': b'My body top', 
            b'body_bottom': b'My body bottom'},
         [
          review_request])

    def check_post_result(self, user, rsp, review_request):
        review = Review.objects.get(pk=rsp[b'review'][b'id'])
        self.assertFalse(review.rich_text)
        self.compare_item(rsp[b'review'], review)


@six.add_metaclass(BasicTestsMetaclass)
class ResourceItemTests(SpyAgency, ReviewItemMixin, ReviewRequestChildItemMixin, BaseWebAPITestCase):
    """Testing the ReviewResource item APIs."""
    fixtures = [
     b'test_users']
    sample_api_url = b'review-requests/<id>/reviews/<id>/'
    resource = resources.review

    def setup_review_request_child_test(self, review_request):
        review = self.create_review(review_request, publish=True)
        return (
         get_review_item_url(review_request, review.pk),
         review_item_mimetype)

    def compare_item(self, item_rsp, review):
        self.assertEqual(item_rsp[b'id'], review.pk)
        self.assertEqual(item_rsp[b'ship_it'], review.ship_it)
        self.assertEqual(item_rsp[b'body_top'], review.body_top)
        self.assertEqual(item_rsp[b'body_bottom'], review.body_bottom)
        if review.body_top_rich_text:
            self.assertEqual(item_rsp[b'body_top_text_type'], b'markdown')
        else:
            self.assertEqual(item_rsp[b'body_top_text_type'], b'plain')
        if review.body_bottom_rich_text:
            self.assertEqual(item_rsp[b'body_bottom_text_type'], b'markdown')
        else:
            self.assertEqual(item_rsp[b'body_bottom_text_type'], b'plain')

    def setup_basic_delete_test(self, user, with_local_site, local_site_name):
        review_request = self.create_review_request(with_local_site=with_local_site, submitter=user, publish=True)
        review = self.create_review(review_request, user=user)
        return (
         get_review_item_url(review_request, review.pk, local_site_name),
         [
          review, review_request])

    def check_delete_result(self, user, review, review_request):
        self.assertNotIn(review, review_request.reviews.all())

    def test_delete_with_published_review(self):
        """Testing the DELETE review-requests/<id>/reviews/<id>/ API
        with pre-published review
        """
        review_request = self.create_review_request(publish=True)
        review = self.create_review(review_request, user=self.user, publish=True)
        self.api_delete(get_review_item_url(review_request, review.id), expected_status=403)
        self.assertEqual(review_request.reviews.count(), 1)

    def test_delete_with_does_not_exist(self):
        """Testing the DELETE review-requests/<id>/reviews/<id>/ API
        with Does Not Exist error
        """
        review_request = self.create_review_request(publish=True)
        rsp = self.api_delete(get_review_item_url(review_request, 919239), expected_status=404)
        self.assertEqual(rsp[b'stat'], b'fail')
        self.assertEqual(rsp[b'err'][b'code'], DOES_NOT_EXIST.code)

    def setup_basic_get_test(self, user, with_local_site, local_site_name):
        review_request = self.create_review_request(with_local_site=with_local_site, submitter=user, publish=True)
        review = self.create_review(review_request, user=user)
        return (
         get_review_item_url(review_request, review.pk, local_site_name),
         review_item_mimetype,
         review)

    def test_get_not_modified(self):
        """Testing the GET review-requests/<id>/reviews/<id>/ API
        with Not Modified response
        """
        review_request = self.create_review_request(publish=True)
        review = self.create_review(review_request, publish=True)
        self._testHttpCaching(get_review_item_url(review_request, review.pk), check_etags=True)

    def setup_basic_put_test(self, user, with_local_site, local_site_name, put_valid_data):
        review_request = self.create_review_request(with_local_site=with_local_site, submitter=user, publish=True)
        review = self.create_review(review_request, user=user)
        return (
         get_review_item_url(review_request, review.pk, local_site_name),
         review_item_mimetype, {b'body_top': b'New body top'},
         review, [])

    def check_put_result(self, user, item_rsp, review, *args):
        self.assertEqual(item_rsp[b'id'], review.pk)
        self.assertEqual(item_rsp[b'body_top'], b'New body top')
        self.assertEqual(item_rsp[b'body_top_text_type'], b'plain')
        self.assertEqual(item_rsp[b'body_bottom_text_type'], b'plain')
        review = Review.objects.get(pk=review.pk)
        self.compare_item(item_rsp, review)

    def test_put_with_published_review(self):
        """Testing the PUT review-requests/<id>/reviews/<id>/ API
        with pre-published review
        """
        review_request = self.create_review_request(publish=True)
        review = self.create_review(review_request, user=self.user, publish=True)
        self.api_put(get_review_item_url(review_request, review.id), {b'body_top': b'foo'}, expected_status=403)

    @webapi_test_template
    def test_put_with_public_and_ship_it_true(self):
        """Testing the PUT <URL> API with pre-published review and
        ship_it=true
        """
        review_request = self.create_review_request(publish=True)
        review = self.create_review(review_request, user=self.user, publish=True)
        rsp = self.api_put(get_review_item_url(review_request, review.pk), {b'ship_it': True}, expected_status=400)
        self.assertEqual(rsp[b'err'][b'code'], INVALID_FORM_DATA.code)
        self.assertEqual(rsp[b'fields'], {b'ship_it': b'Published reviews cannot be updated with ship_it=true'})

    @webapi_test_template
    def test_put_with_revoke_ship_it(self):
        """Testing the PUT <URL> API with revoking Ship It
        """
        review_request = self.create_review_request(publish=True)
        review = self.create_review(review_request, user=self.user, body_top=Review.SHIP_IT_TEXT, ship_it=True, publish=True)
        rsp = self.api_put(get_review_item_url(review_request, review.pk), {b'ship_it': False}, expected_mimetype=review_item_mimetype)
        self.assertEqual(rsp[b'stat'], b'ok')
        self.assertEqual(rsp[b'review'][b'body_top'], Review.REVOKED_SHIP_IT_TEXT)
        self.assertFalse(rsp[b'review'][b'ship_it'])
        self.assertTrue(rsp[b'review'][b'extra_data'].get(b'revoked_ship_it'))

    @webapi_test_template
    def test_put_with_revoke_ship_it_and_no_permission(self):
        """Testing the PUT <URL> API with revoking Ship It and no permission"""
        review_request = self.create_review_request(publish=True)
        review = self.create_review(review_request, ship_it=True, publish=True)
        self.assertNotEqual(review.user, self.user)
        rsp = self.api_put(get_review_item_url(review_request, review.pk), {b'ship_it': False}, expected_status=403)
        self.assertEqual(rsp[b'err'][b'code'], PERMISSION_DENIED.code)

    @webapi_test_template
    def test_put_with_revoke_ship_it_and_not_ship_it(self):
        """Testing the PUT <URL> API with revoking Ship It on a review not
        marked Ship It
        """
        review_request = self.create_review_request(publish=True)
        review = self.create_review(review_request, user=self.user, publish=True)
        rsp = self.api_put(get_review_item_url(review_request, review.pk), {b'ship_it': False}, expected_status=400)
        self.assertEqual(rsp[b'err'][b'code'], INVALID_FORM_DATA.code)
        self.assertEqual(rsp[b'fields'], {b'ship_it': b'This review is not marked Ship It!'})

    @webapi_test_template
    def test_put_with_revoke_ship_it_and_revoke_error(self):
        """Testing the PUT <URL> API with revoking Ship It and handling a
        revocation error
        """

        def on_revoking(**kwargs):
            raise Exception(b'oh no')

        review_request = self.create_review_request(publish=True)
        review = self.create_review(review_request, user=self.user, ship_it=True, publish=True)
        try:
            review_ship_it_revoking.connect(on_revoking)
            rsp = self.api_put(get_review_item_url(review_request, review.pk), {b'ship_it': False}, expected_status=500)
        finally:
            review_ship_it_revoking.disconnect(on_revoking)

        self.assertEqual(rsp[b'err'][b'code'], REVOKE_SHIP_IT_ERROR.code)
        self.assertEqual(rsp[b'err'][b'msg'], b'Error revoking the Ship It: oh no')

    @webapi_test_template
    def test_put_revoke_ship_it_timestamp(self):
        """Testing the PUT <URL> API with revoking Ship It does not update
        timestamp
        """
        self.spy_on(get_tz_aware_utcnow, call_fake=lambda : timezone.now())
        creation_timestamp = datetime.fromtimestamp(0, timezone.utc)
        review_timestamp = creation_timestamp + timedelta(hours=1)
        revoke_timestamp = review_timestamp + timedelta(hours=1)
        with spy_on(timezone.now, call_fake=lambda : creation_timestamp):
            review_request = self.create_review_request(publish=True, submitter=self.user)
        with spy_on(timezone.now, call_fake=lambda : review_timestamp):
            review = self.create_review(review_request, body_top=Review.SHIP_IT_TEXT, ship_it=True, publish=True, user=self.user)
        review_request = ReviewRequest.objects.get(pk=review_request.pk)
        self.assertEqual(review_request.time_added, creation_timestamp)
        self.assertEqual(review_request.last_updated, review_timestamp)
        self.assertEqual(review.timestamp, review_timestamp)
        with spy_on(timezone.now, call_fake=lambda : revoke_timestamp):
            rsp = self.api_put(get_review_item_url(review_request, review.pk), {b'ship_it': False}, expected_mimetype=review_item_mimetype)
        self.assertIn(b'stat', rsp)
        self.assertEqual(rsp[b'stat'], b'ok')
        review = Review.objects.get(pk=review.pk)
        review_request = ReviewRequest.objects.get(pk=review_request.pk)
        self.assertEqual(review_request.time_added, creation_timestamp)
        self.assertEqual(review_request.last_updated, review_timestamp)
        self.assertEqual(review.timestamp, review_timestamp)

    @add_fixtures([b'test_site'])
    def test_put_publish(self):
        """Testing the PUT review-requests/<id>/reviews/<id>/?public=1 API"""
        body_top = b'My Body Top'
        body_bottom = b''
        ship_it = True
        review_request = self.create_review_request(publish=True)
        review = self.create_review(review_request, user=self.user)
        with self.siteconfig_settings({b'mail_send_review_mail': True}, reload_settings=False):
            self.api_put(get_review_item_url(review_request, review.pk), {b'public': True, 
               b'ship_it': ship_it, 
               b'body_top': body_top, 
               b'body_bottom': body_bottom}, expected_mimetype=review_item_mimetype)
        reviews = review_request.reviews.filter(user=self.user)
        self.assertEqual(len(reviews), 1)
        review = reviews[0]
        self.assertEqual(review.ship_it, ship_it)
        self.assertEqual(review.body_top, body_top)
        self.assertEqual(review.body_bottom, body_bottom)
        self.assertEqual(review.public, True)
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, b'Re: Review Request %s: %s' % (
         review_request.display_id, review_request.summary))
        self.assertValidRecipients([
         review_request.submitter.username,
         self.user.username])