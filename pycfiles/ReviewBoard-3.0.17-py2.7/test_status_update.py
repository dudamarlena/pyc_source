# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/reviewboard/webapi/tests/test_status_update.py
# Compiled at: 2020-02-11 04:03:57
from __future__ import unicode_literals
from django.utils import six
from djblets.features.testing import override_feature_checks
from djblets.webapi.errors import DOES_NOT_EXIST, INVALID_FORM_DATA
from djblets.webapi.testing.decorators import webapi_test_template
from reviewboard.changedescs.models import ChangeDescription
from reviewboard.reviews.models.status_update import StatusUpdate
from reviewboard.webapi.resources import resources
from reviewboard.webapi.tests.base import BaseWebAPITestCase
from reviewboard.webapi.tests.mimetypes import status_update_item_mimetype, status_update_list_mimetype
from reviewboard.webapi.tests.mixins import BasicTestsMetaclass, ReviewRequestChildItemMixin, ReviewRequestChildListMixin
from reviewboard.webapi.tests.mixins_extra_data import ExtraDataItemMixin, ExtraDataListMixin
from reviewboard.webapi.tests.urls import get_review_item_url, get_status_update_item_url, get_status_update_list_url

@six.add_metaclass(BasicTestsMetaclass)
class ResourceListTests(ExtraDataListMixin, ReviewRequestChildListMixin, BaseWebAPITestCase):
    """Testing the StatusUpdateResource list APIs."""
    fixtures = [
     b'test_users']
    resource = resources.status_update
    sample_api_url = b'review-requests/<id>/status-updates/'

    def setup_review_request_child_test(self, review_request):
        return (
         get_status_update_list_url(review_request),
         status_update_list_mimetype)

    def compare_item(self, item_rsp, status_update):
        self.assertEqual(item_rsp[b'id'], status_update.pk)
        self.assertEqual(item_rsp[b'summary'], status_update.summary)
        self.assertEqual(item_rsp[b'description'], status_update.description)
        self.assertEqual(item_rsp[b'url'], status_update.url)
        self.assertEqual(item_rsp[b'url_text'], status_update.url_text)
        self.assertEqual(item_rsp[b'extra_data'], status_update.extra_data)

    def setup_basic_get_test(self, user, with_local_site, local_site_name, populate_items):
        review_request = self.create_review_request(with_local_site=with_local_site, submitter=user, publish=True)
        if populate_items:
            items = [
             self.create_status_update(review_request)]
        else:
            items = []
        return (
         get_status_update_list_url(review_request, local_site_name),
         status_update_list_mimetype,
         items)

    def test_get_with_change_id(self):
        """Testing the GET /review-requests/<id>/status-updates/?change= API"""
        review_request = self.create_review_request(submitter=self.user, publish=True)
        change = ChangeDescription.objects.create()
        review_request.changedescs.add(change)
        self.create_status_update(review_request)
        update = self.create_status_update(review_request, change_description=change)
        with override_feature_checks(self.override_features):
            rsp = self.api_get(get_status_update_list_url(review_request), {b'change': change.pk}, expected_mimetype=status_update_list_mimetype)
        self.assertEqual(rsp[b'stat'], b'ok')
        self.assertEqual(len(rsp[b'status_updates']), 1)
        self.assertEqual(rsp[b'status_updates'][0][b'id'], update.pk)

    def test_get_with_service_id(self):
        """Testing the GET /review-requests/<id>/status-updates/?service-id=
        API"""
        review_request = self.create_review_request(submitter=self.user, publish=True)
        self.create_status_update(review_request, service_id=b'service1')
        update = self.create_status_update(review_request, service_id=b'service2')
        with override_feature_checks(self.override_features):
            rsp = self.api_get(get_status_update_list_url(review_request), {b'service-id': update.service_id}, expected_mimetype=status_update_list_mimetype)
        self.assertEqual(rsp[b'stat'], b'ok')
        self.assertEqual(len(rsp[b'status_updates']), 1)
        self.assertEqual(rsp[b'status_updates'][0][b'id'], update.pk)

    def test_get_with_state(self):
        """Testing the GET /review-requests/<id>/status-updates/?state= API"""
        review_request = self.create_review_request(submitter=self.user, publish=True)
        self.create_status_update(review_request, state=StatusUpdate.PENDING)
        update = self.create_status_update(review_request, state=StatusUpdate.DONE_SUCCESS)
        with override_feature_checks(self.override_features):
            rsp = self.api_get(get_status_update_list_url(review_request), {b'state': b'done-success'}, expected_mimetype=status_update_list_mimetype)
        self.assertEqual(rsp[b'stat'], b'ok')
        self.assertEqual(len(rsp[b'status_updates']), 1)
        self.assertEqual(rsp[b'status_updates'][0][b'id'], update.pk)

    def setup_basic_post_test(self, user, with_local_site, local_site_name, post_valid_data):
        review_request = self.create_review_request(with_local_site=with_local_site, submitter=user, publish=True)
        if post_valid_data:
            post_data = {b'service_id': b'Service', b'summary': b'Summary'}
        else:
            post_data = {}
        return (get_status_update_list_url(review_request, local_site_name),
         status_update_item_mimetype,
         post_data,
         [
          review_request])

    def check_post_result(self, user, rsp, review_request):
        status_update = StatusUpdate.objects.get(pk=rsp[b'status_update'][b'id'])
        self.compare_item(rsp[b'status_update'], status_update)

    @webapi_test_template
    def test_post_with_invalid_state(self):
        """Testing the POST <URL> API with an invalid state"""
        review_request = self.create_review_request(publish=True)
        with override_feature_checks(self.override_features):
            rsp = self.api_post(get_status_update_list_url(review_request), {b'service_id': b'Service', 
               b'summary': b'Summary', 
               b'state': b'incorrect'}, expected_status=400)
        self.assertEqual(rsp[b'stat'], b'fail')
        self.assertEqual(rsp[b'err'][b'code'], INVALID_FORM_DATA.code)
        self.assertTrue(b'state' in rsp[b'fields'])

    @webapi_test_template
    def test_post_with_invalid_change_id(self):
        """Testing the POST <URL> API with an change_id state"""
        review_request = self.create_review_request(publish=True)
        with override_feature_checks(self.override_features):
            rsp = self.api_post(get_status_update_list_url(review_request), {b'service_id': b'Service', 
               b'summary': b'Summary', 
               b'change_id': b'123456'}, expected_status=400)
        self.assertEqual(rsp[b'stat'], b'fail')
        self.assertEqual(rsp[b'err'][b'code'], INVALID_FORM_DATA.code)
        self.assertTrue(b'change_id' in rsp[b'fields'])

    @webapi_test_template
    def test_post_with_invalid_review_id(self):
        """Testing the POST <URL> API with an invalid review_id"""
        review_request = self.create_review_request(publish=True)
        with override_feature_checks(self.override_features):
            rsp = self.api_post(get_status_update_list_url(review_request), {b'service_id': b'Service', 
               b'summary': b'Summary', 
               b'review_id': b'123456'}, expected_status=400)
        self.assertEqual(rsp[b'stat'], b'fail')
        self.assertEqual(rsp[b'err'][b'code'], INVALID_FORM_DATA.code)
        self.assertTrue(b'review_id' in rsp[b'fields'])


@six.add_metaclass(BasicTestsMetaclass)
class ResourceItemTests(ReviewRequestChildItemMixin, ExtraDataItemMixin, BaseWebAPITestCase):
    """Testing the StatusUpdateResource item APIs."""
    fixtures = [
     b'test_users']
    sample_api_url = b'review-requests/<id>/status-updates/<id>/'
    resource = resources.status_update

    def setup_review_request_child_test(self, review_request):
        status_update = self.create_status_update(review_request)
        return (
         get_status_update_item_url(review_request, status_update.pk),
         status_update_item_mimetype)

    def compare_item(self, item_rsp, status_update):
        self.assertEqual(item_rsp[b'id'], status_update.pk)
        if status_update.review_id:
            review_request = status_update.review_request
            local_site_name = review_request.local_site and review_request.local_site.name
            review_url = self.base_url + get_review_item_url(review_request, status_update.review_id, local_site_name)
            self.assertEqual(item_rsp[b'links'][b'review'][b'href'], review_url)

    def setup_basic_delete_test(self, user, with_local_site, local_site_name):
        review_request = self.create_review_request(with_local_site=with_local_site, submitter=user, publish=True)
        status_update = self.create_status_update(review_request, user=user)
        return (
         get_status_update_item_url(review_request, status_update.pk, local_site_name),
         [
          status_update, review_request])

    def check_delete_result(self, user, status_update, review_request):
        self.assertNotIn(status_update, review_request.status_updates.all())

    @webapi_test_template
    def test_delete_with_does_not_exist(self):
        """Testing the DELETE <URL> API
        with Does Not Exist error
        """
        review_request = self.create_review_request(publish=True)
        with override_feature_checks(self.override_features):
            rsp = self.api_delete(get_status_update_item_url(review_request, 12345), expected_status=404)
        self.assertEqual(rsp[b'stat'], b'fail')
        self.assertEqual(rsp[b'err'][b'code'], DOES_NOT_EXIST.code)

    def setup_basic_get_test(self, user, with_local_site, local_site_name):
        review_request = self.create_review_request(with_local_site=with_local_site, submitter=user, publish=True)
        status_update = self.create_status_update(review_request, user=user)
        return (
         get_status_update_item_url(review_request, status_update.pk, local_site_name),
         status_update_item_mimetype,
         status_update)

    @webapi_test_template
    def test_get_not_modified(self):
        """Testing the GET <URL> API
        with Not Modified response
        """
        review_request = self.create_review_request(publish=True)
        status_update = self.create_status_update(review_request)
        with override_feature_checks(self.override_features):
            self._testHttpCaching(get_status_update_item_url(review_request, status_update.pk), check_etags=True)

    def setup_basic_put_test(self, user, with_local_site, local_site_name, put_valid_data):
        review_request = self.create_review_request(with_local_site=with_local_site, submitter=user, publish=True)
        review = self.create_review(review_request=review_request)
        status_update = self.create_status_update(review_request, user=user)
        return (
         get_status_update_item_url(review_request, status_update.pk, local_site_name),
         status_update_item_mimetype,
         {b'summary': b'New summary', 
            b'review_id': review.pk},
         status_update, [])

    def check_put_result(self, user, item_rsp, status_update, *args):
        self.assertEqual(item_rsp[b'id'], status_update.pk)
        status_update = StatusUpdate.objects.get(pk=status_update.pk)
        self.compare_item(item_rsp, status_update)