# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/reviewboard/webapi/tests/test_webhook.py
# Compiled at: 2020-02-11 04:03:57
from __future__ import unicode_literals
from django.utils import six
from djblets.testing.decorators import add_fixtures
from djblets.webapi.errors import INVALID_FORM_DATA
from djblets.webapi.testing.decorators import webapi_test_template
from reviewboard.notifications.models import WebHookTarget
from reviewboard.site.models import LocalSite
from reviewboard.webapi.resources import resources
from reviewboard.webapi.tests.base import BaseWebAPITestCase
from reviewboard.webapi.tests.mimetypes import webhook_item_mimetype, webhook_list_mimetype
from reviewboard.webapi.tests.mixins import BasicTestsMetaclass
from reviewboard.webapi.tests.mixins_extra_data import ExtraDataItemMixin, ExtraDataListMixin
from reviewboard.webapi.tests.urls import get_webhook_item_url, get_webhook_list_url

def compare_item(self, item_rsp, webhook):
    self.assertEqual(item_rsp[b'id'], webhook.pk)
    self.assertEqual(item_rsp[b'enabled'], webhook.enabled)
    self.assertEqual(item_rsp[b'url'], webhook.url)
    self.assertEqual(item_rsp[b'custom_content'], webhook.custom_content)
    self.assertEqual(item_rsp[b'secret'], webhook.secret)
    self.assertEqual(resources.webhook.parse_apply_to_field(item_rsp[b'apply_to'], None), webhook.apply_to)
    self.assertEqual(set(item[b'title'] for item in item_rsp[b'repositories']), set(repo.name for repo in webhook.repositories.all()))
    self.assertEqual(item_rsp[b'events'], webhook.events)
    self.assertEqual(item_rsp[b'extra_data'], webhook.extra_data)
    return


@six.add_metaclass(BasicTestsMetaclass)
class ResourceListTests(ExtraDataListMixin, BaseWebAPITestCase):
    """Tests for the WebHookResource list resource."""
    resource = resources.webhook
    sample_api_url = b'webhooks/'
    basic_get_use_admin = True
    basic_post_use_admin = True
    fixtures = [
     b'test_users']
    compare_item = compare_item

    def setup_basic_get_test(self, user, with_local_site, local_site_name, populate_items):
        webhook = self.create_webhook(with_local_site=with_local_site)
        if populate_items:
            items = [
             webhook]
        else:
            items = []
        return (
         get_webhook_list_url(local_site_name),
         webhook_list_mimetype,
         items)

    def setup_basic_post_test(self, user, with_local_site, local_site_name, post_valid_data):
        if post_valid_data:
            post_data = {b'enabled': 0, b'events': b'*', 
               b'url': b'http://example.com', 
               b'encoding': b'application/json', 
               b'custom_content': b'', 
               b'apply_to': b'all'}
        else:
            post_data = {}
        return (
         get_webhook_list_url(local_site_name),
         webhook_item_mimetype,
         post_data,
         [
          local_site_name])

    def check_post_result(self, user, rsp, local_site_name=None):
        self.assertIn(b'webhook', rsp)
        item_rsp = rsp[b'webhook']
        webhook = WebHookTarget.objects.get(pk=item_rsp[b'id'])
        if local_site_name is None:
            self.assertIsNone(webhook.local_site)
        else:
            self.assertEqual(webhook.local_site.name, local_site_name)
        self.compare_item(item_rsp, webhook)
        return

    @add_fixtures([b'test_scmtools'])
    @webapi_test_template
    def test_post_with_repositories(self):
        """Testing the POST <url> API with custom repositories"""
        repositories = [
         self.create_repository(name=b'Repo 1'),
         self.create_repository(name=b'Repo 2')]
        self.user.is_superuser = True
        self.user.save()
        rsp = self.api_post(get_webhook_list_url(), {b'enabled': 0, 
           b'events': b'*', 
           b'url': b'http://example.com', 
           b'encoding': b'application/json', 
           b'apply_to': b'custom', 
           b'repositories': (b',').join(six.text_type(repo.pk) for repo in repositories)}, expected_mimetype=webhook_item_mimetype)
        self.assertEqual(rsp[b'stat'], b'ok')
        self.check_post_result(self.user, rsp)

    @add_fixtures([b'test_scmtools'])
    @webapi_test_template
    def test_post_all_repositories_not_same_local_site(self):
        """Testing the POST <URL> API with a local site and custom
        repositories that are not all in the same local site
        """
        local_site_1 = LocalSite.objects.create(name=b'local-site-1')
        local_site_2 = LocalSite.objects.create(name=b'local-site-2')
        for local_site in (local_site_1, local_site_2):
            local_site.admins = [self.user]
            local_site.users = [self.user]
            local_site.save()

        repositories = [
         self.create_repository(name=b'Repo 1', local_site=local_site_1),
         self.create_repository(name=b'Repo 2', local_site=local_site_2),
         self.create_repository(name=b'Repo 3')]
        rsp = self.api_post(get_webhook_list_url(local_site_1), {b'enabled': 0, 
           b'events': b'*', 
           b'url': b'http://example.com', 
           b'encoding': b'application/json', 
           b'custom_content': b'', 
           b'apply_to': b'custom', 
           b'repositories': (b',').join(six.text_type(repo.pk) for repo in repositories)}, expected_status=400)
        self.assertEqual(rsp[b'stat'], b'fail')
        self.assertTrue(b'err' in rsp)
        self.assertEqual(rsp[b'err'][b'code'], INVALID_FORM_DATA.code)
        self.assertEqual(rsp[b'err'][b'msg'], INVALID_FORM_DATA.msg)
        self.assertTrue(b'fields' in rsp)
        self.assertTrue(b'repositories' in rsp[b'fields'])
        self.assertEqual(rsp[b'fields'][b'repositories'], [
         b'A repository with ID 3 was not found.'])

    @add_fixtures([b'test_scmtools'])
    @webapi_test_template
    def test_post_repositories_local_site_but_webhook_not(self):
        """Testing the POST <URL> API without a local site for repositories
        that are in a local site
        """
        local_site = LocalSite.objects.create(name=b'local-site-1')
        self.user.is_superuser = True
        self.user.save()
        repositories = [
         self.create_repository(name=b'Repo 1', local_site=local_site),
         self.create_repository(name=b'Repo 2', local_site=local_site)]
        rsp = self.api_post(get_webhook_list_url(), {b'enabled': 0, 
           b'events': b'*', 
           b'url': b'http://example.com', 
           b'encoding': b'application/json', 
           b'custom_content': b'', 
           b'apply_to': b'custom', 
           b'repositories': (b',').join(six.text_type(repo.pk) for repo in repositories)}, expected_status=400)
        self.assertEqual(rsp[b'stat'], b'fail')
        self.assertTrue(b'err' in rsp)
        self.assertEqual(rsp[b'err'][b'code'], INVALID_FORM_DATA.code)
        self.assertEqual(rsp[b'err'][b'msg'], INVALID_FORM_DATA.msg)
        self.assertTrue(b'fields' in rsp)
        self.assertTrue(b'repositories' in rsp[b'fields'])
        self.assertEqual(rsp[b'fields'][b'repositories'], [
         b'A repository with ID 1 was not found.'])

    @webapi_test_template
    def test_post_with_global_site_and_set_local_site(self):
        """Testing the POST <URL> API and attempting to set a LocalSite for a
        non-LocalSite WebHook is ignored
        """
        local_site = LocalSite.objects.create(name=b'local-site-1')
        self.user.is_superuser = True
        self.user.save()
        rsp = self.api_post(get_webhook_list_url(), {b'enabled': 0, 
           b'events': b'*', 
           b'url': b'http://example.com', 
           b'encoding': b'application/json', 
           b'custom_content': b'', 
           b'apply_to': b'all', 
           b'local_site': local_site.pk}, expected_mimetype=webhook_item_mimetype)
        self.assertEqual(rsp[b'stat'], b'ok')
        webhook = WebHookTarget.objects.get(pk=rsp[b'webhook'][b'id'])
        self.assertIsNone(webhook.local_site)
        self.compare_item(rsp[b'webhook'], webhook)

    @webapi_test_template
    def test_post_with_local_site_and_set_local_site(self):
        """Testing the POST <URL> API and attempting to set a LocalSite for
        another LocalSite's WebHook is ignored
        """
        local_site_1 = LocalSite.objects.create(name=b'local-site-1')
        local_site_1.users.add(self.user)
        local_site_2 = LocalSite.objects.create(name=b'local-site-2')
        self.user.is_superuser = True
        self.user.save()
        rsp = self.api_post(get_webhook_list_url(local_site_name=b'local-site-1'), {b'enabled': 0, 
           b'events': b'*', 
           b'url': b'http://example.com', 
           b'encoding': b'application/json', 
           b'custom_content': b'', 
           b'apply_to': b'all', 
           b'local_site': local_site_2.pk}, expected_mimetype=webhook_item_mimetype)
        self.assertEqual(rsp[b'stat'], b'ok')
        webhook = WebHookTarget.objects.get(pk=rsp[b'webhook'][b'id'])
        self.assertEqual(webhook.local_site_id, local_site_1.pk)
        self.compare_item(rsp[b'webhook'], webhook)

    @add_fixtures([b'test_scmtools'])
    @webapi_test_template
    def test_post_multiple_events(self):
        """Testing the POST <URL> API with multiple events"""
        self.user.is_superuser = True
        self.user.save()
        rsp = self.api_post(get_webhook_list_url(), {b'enabled': 0, 
           b'events': b'review_request_closed,review_request_published', 
           b'url': b'http://example.com', 
           b'encoding': b'application/json', 
           b'custom_content': b'', 
           b'apply_to': b'all'}, expected_mimetype=webhook_item_mimetype)
        self.assertIn(b'stat', rsp)
        self.assertEqual(rsp[b'stat'], b'ok')
        self.assertIn(b'webhook', rsp)
        self.compare_item(rsp[b'webhook'], WebHookTarget.objects.get())

    @add_fixtures([b'test_scmtools'])
    @webapi_test_template
    def test_post_no_events(self):
        """Testing the POST <URL> API with no events"""
        self.user.is_superuser = True
        self.user.save()
        rsp = self.api_post(get_webhook_list_url(), {b'enabled': 0, 
           b'events': b'', 
           b'url': b'http://example.com', 
           b'encoding': b'application/json', 
           b'custom_content': b'', 
           b'apply_to': b'all'}, expected_mimetype=webhook_item_mimetype)
        self.assertIn(b'stat', rsp)
        self.assertEqual(rsp[b'stat'], b'ok')
        self.assertIn(b'webhook', rsp)
        self.compare_item(rsp[b'webhook'], WebHookTarget.objects.get())

    @add_fixtures([b'test_scmtools'])
    @webapi_test_template
    def test_post_all_events_and_more(self):
        """Testing the POST <URL> API with all events (*) and additional
        events
        """
        self.user.is_superuser = True
        self.user.save()
        rsp = self.api_post(get_webhook_list_url(), {b'enabled': 0, 
           b'events': b'review_request_closed,*,review_request_published', 
           b'url': b'http://example.com', 
           b'encoding': b'application/json', 
           b'custom_content': b'', 
           b'apply_to': b'all'}, expected_mimetype=webhook_item_mimetype)
        webhook = WebHookTarget.objects.get()
        self.assertIn(b'stat', rsp)
        self.assertEqual(rsp[b'stat'], b'ok')
        self.assertIn(b'webhook', rsp)
        self.compare_item(rsp[b'webhook'], webhook)
        self.assertListEqual(webhook.events, [b'*'])

    @add_fixtures([b'test_scmtools'])
    @webapi_test_template
    def test_post_empty_repositories(self):
        """Testing the POST <URL> API with an empty repositories field"""
        self.user.is_superuser = True
        self.user.save()
        rsp = self.api_post(get_webhook_list_url(), {b'enabled': 0, 
           b'events': b'review_request_closed,*,review_request_published', 
           b'url': b'http://example.com', 
           b'encoding': b'application/json', 
           b'custom_content': b'', 
           b'apply_to': b'custom', 
           b'repositories': b''}, expected_mimetype=webhook_item_mimetype)
        self.assertIn(b'stat', rsp)
        self.assertEqual(rsp[b'stat'], b'ok')
        self.assertIn(b'webhook', rsp)
        self.compare_item(rsp[b'webhook'], WebHookTarget.objects.get())


@six.add_metaclass(BasicTestsMetaclass)
class ResourceItemTests(ExtraDataItemMixin, BaseWebAPITestCase):
    """Tests for the WebHookResource item resource."""
    resource = resources.webhook
    sample_api_url = b'webhooks/<id>/'
    basic_get_use_admin = True
    basic_delete_use_admin = True
    basic_put_use_admin = True
    fixtures = [
     b'test_users']
    compare_item = compare_item

    def setup_basic_get_test(self, user, with_local_site, local_site_name):
        webhook = self.create_webhook(with_local_site=with_local_site)
        return (
         get_webhook_item_url(webhook.pk, local_site_name),
         webhook_item_mimetype,
         webhook)

    def setup_basic_put_test(self, user, with_local_site, local_site_name, put_valid_data):
        webhook = self.create_webhook(with_local_site=with_local_site)
        return (
         get_webhook_item_url(webhook.pk, local_site_name),
         webhook_item_mimetype, {},
         webhook,
         [
          local_site_name])

    def check_put_result(self, user, item_rsp, item, local_site_name=None):
        webhook = WebHookTarget.objects.get(pk=item_rsp[b'id'])
        if local_site_name is None:
            self.assertIsNone(webhook.local_site)
        else:
            self.assertEqual(webhook.local_site.name, local_site_name)
        self.compare_item(item_rsp, webhook)
        return

    def setup_basic_delete_test(self, user, with_local_site, local_site_name):
        webhook = self.create_webhook(with_local_site=with_local_site)
        return (
         get_webhook_item_url(webhook.pk, local_site_name),
         [
          webhook])

    def check_delete_result(self, user, webhook):
        self.assertRaises(WebHookTarget.DoesNotExist, lambda : WebHookTarget.objects.get(pk=webhook.pk))

    @webapi_test_template
    def test_put_with_global_site_and_set_local_site(self):
        """Testing the PUT <URL> API and attempting to set a LocalSite for a
        non-LocalSite WebHook is ignored
        """
        local_site = LocalSite.objects.create(name=b'local-site-1')
        self.user.is_superuser = True
        self.user.save()
        webhook = self.create_webhook()
        rsp = self.api_put(get_webhook_item_url(webhook.pk), {b'local_site': local_site.pk}, expected_mimetype=webhook_item_mimetype)
        self.assertEqual(rsp[b'stat'], b'ok')
        webhook = WebHookTarget.objects.get(pk=rsp[b'webhook'][b'id'])
        self.assertIsNone(webhook.local_site)
        self.compare_item(rsp[b'webhook'], webhook)

    @webapi_test_template
    def test_put_with_local_site_and_set_local_site(self):
        """Testing the PUT <URL> API and attempting to set a LocalSite for a
        another LocalSite's WebHook is ignored
        """
        local_site_1 = LocalSite.objects.create(name=b'local-site-1')
        local_site_1.users.add(self.user)
        local_site_2 = LocalSite.objects.create(name=b'local-site-2')
        self.user.is_superuser = True
        self.user.save()
        webhook = self.create_webhook(local_site=local_site_1)
        rsp = self.api_put(get_webhook_item_url(webhook.pk, local_site_1.name), {b'local_site': local_site_2.pk}, expected_mimetype=webhook_item_mimetype)
        self.assertEqual(rsp[b'stat'], b'ok')
        webhook = WebHookTarget.objects.get(pk=rsp[b'webhook'][b'id'])
        self.assertEqual(webhook.local_site_id, local_site_1.pk)
        self.compare_item(rsp[b'webhook'], webhook)