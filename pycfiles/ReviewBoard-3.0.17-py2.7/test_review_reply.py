# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/reviewboard/webapi/tests/test_review_reply.py
# Compiled at: 2020-02-11 04:03:57
from __future__ import unicode_literals
from django.core import mail
from django.utils import six
from reviewboard.reviews.models import Review
from reviewboard.webapi.resources import resources
from reviewboard.webapi.tests.base import BaseWebAPITestCase
from reviewboard.webapi.tests.mimetypes import review_reply_item_mimetype, review_reply_list_mimetype
from reviewboard.webapi.tests.mixins import BasicTestsMetaclass, ReviewRequestChildItemMixin, ReviewRequestChildListMixin
from reviewboard.webapi.tests.mixins_review import ReviewItemMixin, ReviewListMixin
from reviewboard.webapi.tests.urls import get_review_reply_item_url, get_review_reply_list_url

class BaseResourceTestCase(BaseWebAPITestCase):

    def _create_test_review(self, with_local_site=False):
        review_request = self.create_review_request(submitter=self.user, with_local_site=with_local_site)
        file_attachment = self.create_file_attachment(review_request)
        review_request.publish(review_request.submitter)
        review = self.create_review(review_request, publish=True)
        self.create_file_attachment_comment(review, file_attachment)
        return review


@six.add_metaclass(BasicTestsMetaclass)
class ResourceListTests(ReviewListMixin, ReviewRequestChildListMixin, BaseResourceTestCase):
    """Testing the ReviewReplyResource list APIs."""
    fixtures = [
     b'test_users']
    sample_api_url = b'review-requests/<id>/reviews/<id>/replies/'
    resource = resources.review_reply

    def setup_review_request_child_test(self, review_request):
        review = self.create_review(review_request, publish=True)
        return (
         get_review_reply_list_url(review),
         review_reply_list_mimetype)

    def compare_item(self, item_rsp, reply):
        self.assertEqual(item_rsp[b'id'], reply.pk)
        self.assertEqual(item_rsp[b'body_top'], reply.body_top)
        self.assertEqual(item_rsp[b'body_bottom'], reply.body_bottom)
        if reply.body_top_rich_text:
            self.assertEqual(item_rsp[b'body_top_text_type'], b'markdown')
        else:
            self.assertEqual(item_rsp[b'body_top_text_type'], b'plain')
        if reply.body_bottom_rich_text:
            self.assertEqual(item_rsp[b'body_bottom_text_type'], b'markdown')
        else:
            self.assertEqual(item_rsp[b'body_bottom_text_type'], b'plain')

    def setup_basic_get_test(self, user, with_local_site, local_site_name, populate_items):
        review_request = self.create_review_request(with_local_site=with_local_site, submitter=user, publish=True)
        review = self.create_review(review_request, publish=True)
        if populate_items:
            items = [
             self.create_reply(review, publish=True)]
        else:
            items = []
        return (
         get_review_reply_list_url(review, local_site_name),
         review_reply_list_mimetype,
         items)

    def test_get_with_counts_only(self):
        """Testing the
        GET review-requests/<id>/reviews/<id>/replies/?counts-only=1 API
        """
        review = self._create_test_review()
        self.create_reply(review, user=self.user, publish=True)
        rsp = self.api_get(b'%s?counts-only=1' % get_review_reply_list_url(review), expected_mimetype=review_reply_list_mimetype)
        self.assertEqual(rsp[b'stat'], b'ok')
        self.assertEqual(rsp[b'count'], 1)

    def setup_basic_post_test(self, user, with_local_site, local_site_name, post_valid_data):
        review_request = self.create_review_request(with_local_site=with_local_site, submitter=user, publish=True)
        review = self.create_review(review_request, publish=True)
        return (
         get_review_reply_list_url(review, local_site_name),
         review_reply_item_mimetype, {},
         [
          review])

    def check_post_result(self, user, rsp, review):
        reply = Review.objects.get(pk=rsp[b'reply'][b'id'])
        self.assertFalse(reply.body_top_rich_text)
        self.compare_item(rsp[b'reply'], reply)

    def test_post_with_body_top(self):
        """Testing the POST review-requests/<id>/reviews/<id>/replies/ API
        with body_top
        """
        body_top = b'My Body Top'
        review_request = self.create_review_request(publish=True)
        review = self.create_review(review_request, publish=True)
        rsp = self.api_post(get_review_reply_list_url(review), {b'body_top': body_top}, expected_mimetype=review_reply_item_mimetype)
        self.assertEqual(rsp[b'stat'], b'ok')
        reply = Review.objects.get(pk=rsp[b'reply'][b'id'])
        self.assertEqual(reply.body_top, body_top)

    def test_post_with_body_bottom(self):
        """Testing the POST review-requests/<id>/reviews/<id>/replies/ API
        with body_bottom
        """
        body_bottom = b'My Body Bottom'
        review_request = self.create_review_request(publish=True)
        review = self.create_review(review_request, publish=True)
        rsp = self.api_post(get_review_reply_list_url(review), {b'body_bottom': body_bottom}, expected_mimetype=review_reply_item_mimetype)
        self.assertEqual(rsp[b'stat'], b'ok')
        reply = Review.objects.get(pk=rsp[b'reply'][b'id'])
        self.assertEqual(reply.body_bottom, body_bottom)


@six.add_metaclass(BasicTestsMetaclass)
class ResourceItemTests(ReviewItemMixin, ReviewRequestChildItemMixin, BaseResourceTestCase):
    """Testing the ReviewReplyResource item APIs."""
    fixtures = [
     b'test_users']
    sample_api_url = b'review-requests/<id>/reviews/<id>/replies/<id>/'
    resource = resources.review_reply

    def setup_review_request_child_test(self, review_request):
        review = self.create_review(review_request, publish=True)
        reply = self.create_reply(review, publish=True)
        return (
         get_review_reply_item_url(review, reply.pk),
         review_reply_item_mimetype)

    def compare_item(self, item_rsp, reply):
        self.assertEqual(item_rsp[b'id'], reply.pk)
        self.assertEqual(item_rsp[b'body_top'], reply.body_top)
        self.assertEqual(item_rsp[b'body_bottom'], reply.body_bottom)
        if reply.body_top_rich_text:
            self.assertEqual(item_rsp[b'body_top_text_type'], b'markdown')
        else:
            self.assertEqual(item_rsp[b'body_top_text_type'], b'plain')
        if reply.body_bottom_rich_text:
            self.assertEqual(item_rsp[b'body_bottom_text_type'], b'markdown')
        else:
            self.assertEqual(item_rsp[b'body_bottom_text_type'], b'plain')

    def setup_basic_delete_test(self, user, with_local_site, local_site_name):
        review_request = self.create_review_request(with_local_site=with_local_site, submitter=user, publish=True)
        review = self.create_review(review_request, user=user, publish=True)
        reply = self.create_reply(review, user=user)
        return (
         get_review_reply_item_url(review, reply.pk, local_site_name),
         [
          reply, review])

    def check_delete_result(self, user, reply, review):
        self.assertNotIn(reply, review.replies.all())

    def setup_basic_get_test(self, user, with_local_site, local_site_name):
        review_request = self.create_review_request(with_local_site=with_local_site, submitter=user, publish=True)
        review = self.create_review(review_request, user=user, publish=True)
        reply = self.create_reply(review, user=user)
        return (
         get_review_reply_item_url(review, reply.pk, local_site_name),
         review_reply_item_mimetype,
         reply)

    def test_get_not_modified(self):
        """Testing the GET review-requests/<id>/reviews/<id>/
        with Not Modified response
        """
        review_request = self.create_review_request(publish=True)
        review = self.create_review(review_request, publish=True)
        reply = self.create_reply(review, publish=True)
        self._testHttpCaching(get_review_reply_item_url(reply.base_reply_to, reply.id), check_etags=True)

    def setup_basic_put_test(self, user, with_local_site, local_site_name, put_valid_data):
        review_request = self.create_review_request(with_local_site=with_local_site, submitter=user, publish=True)
        review = self.create_review(review_request, user=user, publish=True)
        reply = self.create_reply(review, user=user)
        return (
         get_review_reply_item_url(review, reply.pk, local_site_name),
         review_reply_item_mimetype, {b'body_top': b'New body top'},
         reply, [])

    def check_put_result(self, user, item_rsp, reply, *args):
        self.assertEqual(item_rsp[b'id'], reply.pk)
        self.assertEqual(item_rsp[b'body_top'], b'New body top')
        self.assertEqual(item_rsp[b'body_top_text_type'], b'plain')
        reply = Review.objects.get(pk=reply.pk)
        self.compare_item(item_rsp, reply)

    def test_put_with_publish(self):
        """Testing the
        PUT review-requests/<id>/reviews/<id>/replies/<id>/?public=1 API
        """
        review_request = self.create_review_request(publish=True)
        review = self.create_review(review_request, publish=True)
        rsp, response = self.api_post_with_response(get_review_reply_list_url(review), expected_mimetype=review_reply_item_mimetype)
        self.assertIn(b'Location', response)
        self.assertIn(b'stat', rsp)
        self.assertEqual(rsp[b'stat'], b'ok')
        with self.siteconfig_settings({b'mail_send_review_mail': True}, reload_settings=False):
            rsp = self.api_put(response[b'Location'], {b'body_top': b'Test', 
               b'public': True}, expected_mimetype=review_reply_item_mimetype)
        self.assertEqual(rsp[b'stat'], b'ok')
        reply = Review.objects.get(pk=rsp[b'reply'][b'id'])
        self.assertEqual(reply.public, True)
        self.assertEqual(len(mail.outbox), 1)

    def test_put_with_publish_and_trivial(self):
        """Testing the PUT review-requests/<id>/draft/ API with trivial
        changes
        """
        review_request = self.create_review_request(submitter=self.user, publish=True)
        review = self.create_review(review_request, publish=True)
        rsp, response = self.api_post_with_response(get_review_reply_list_url(review), expected_mimetype=review_reply_item_mimetype)
        self.assertIn(b'Location', response)
        self.assertIn(b'stat', rsp)
        self.assertEqual(rsp[b'stat'], b'ok')
        with self.siteconfig_settings({b'mail_send_review_mail': True}, reload_settings=False):
            rsp = self.api_put(response[b'Location'], {b'body_top': b'Test', 
               b'public': True, 
               b'trivial': True}, expected_mimetype=review_reply_item_mimetype)
        self.assertIn(b'stat', rsp)
        self.assertEqual(rsp[b'stat'], b'ok')
        self.assertIn(b'reply', rsp)
        self.assertIn(b'id', rsp[b'reply'])
        reply = Review.objects.get(pk=rsp[b'reply'][b'id'])
        self.assertTrue(reply.public)
        self.assertEqual(len(mail.outbox), 0)