# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/reviewboard/webapi/tests/test_hosting_service_account.py
# Compiled at: 2020-02-11 04:03:57
from __future__ import unicode_literals
from django.utils import six
from reviewboard.hostingsvcs.models import HostingServiceAccount
from reviewboard.webapi.resources import resources
from reviewboard.webapi.tests.base import BaseWebAPITestCase
from reviewboard.webapi.tests.mimetypes import hosting_service_account_item_mimetype, hosting_service_account_list_mimetype
from reviewboard.webapi.tests.mixins import BasicTestsMetaclass
from reviewboard.webapi.tests.urls import get_hosting_service_account_item_url, get_hosting_service_account_list_url

def _compare_item(self, item_rsp, account):
    self.assertEqual(item_rsp[b'id'], account.id)
    self.assertEqual(item_rsp[b'username'], account.username)
    self.assertEqual(item_rsp[b'service'], account.service.hosting_service_id)


@six.add_metaclass(BasicTestsMetaclass)
class ResourceListTests(BaseWebAPITestCase):
    """Testing the HostingServiceAccountResource list APIs."""
    sample_api_url = b'hosting-services-accounts/'
    resource = resources.hosting_service_account
    fixtures = [b'test_users']
    basic_post_use_admin = True
    compare_item = _compare_item

    def setup_http_not_allowed_list_test(self, user):
        return get_hosting_service_account_list_url()

    def setup_basic_get_test(self, user, with_local_site, local_site_name, populate_items):
        if populate_items:
            if with_local_site:
                local_site = self.get_local_site(name=local_site_name)
            else:
                local_site = None
            accounts = [
             HostingServiceAccount.objects.create(service_name=b'googlecode', username=b'bob', local_site=local_site)]
        else:
            accounts = []
        return (
         get_hosting_service_account_list_url(local_site_name),
         hosting_service_account_list_mimetype,
         accounts)

    def test_get_with_service(self):
        """Testing the GET hosting-service-accounts/ API with service="""
        HostingServiceAccount.objects.create(service_name=b'googlecode', username=b'bob')
        account = HostingServiceAccount.objects.create(service_name=b'github', username=b'bob')
        rsp = self.api_get(get_hosting_service_account_list_url(), query={b'service': b'github'}, expected_mimetype=hosting_service_account_list_mimetype)
        self.assertEqual(rsp[b'stat'], b'ok')
        self.assertEqual(len(rsp[b'hosting_service_accounts']), 1)
        self.compare_item(rsp[b'hosting_service_accounts'][0], account)

    def test_get_with_username(self):
        """Testing the GET hosting-service-accounts/ API with username="""
        account = HostingServiceAccount.objects.create(service_name=b'googlecode', username=b'bob')
        HostingServiceAccount.objects.create(service_name=b'googlecode', username=b'frank')
        rsp = self.api_get(get_hosting_service_account_list_url(), query={b'username': b'bob'}, expected_mimetype=hosting_service_account_list_mimetype)
        self.assertEqual(rsp[b'stat'], b'ok')
        self.assertEqual(len(rsp[b'hosting_service_accounts']), 1)
        self.compare_item(rsp[b'hosting_service_accounts'][0], account)

    def setup_basic_post_test(self, user, with_local_site, local_site_name, post_valid_data):
        if post_valid_data:
            post_data = {b'username': b'bob', b'service_id': b'googlecode'}
        else:
            post_data = {}
        return (
         get_hosting_service_account_list_url(local_site_name),
         hosting_service_account_item_mimetype,
         post_data, [])

    def check_post_result(self, user, rsp):
        HostingServiceAccount.objects.get(pk=rsp[b'hosting_service_account'][b'id'])


@six.add_metaclass(BasicTestsMetaclass)
class ResourceItemTests(BaseWebAPITestCase):
    """Testing the HostingServiceAccountResource item APIs."""
    fixtures = [
     b'test_users']
    sample_api_url = b'hosting-service-accounts/<id>/'
    resource = resources.hosting_service_account
    compare_item = _compare_item

    def setup_http_not_allowed_item_test(self, user):
        account = HostingServiceAccount.objects.create(service_name=b'googlecode', username=b'bob')
        return get_hosting_service_account_item_url(account.pk)

    def setup_basic_get_test(self, user, with_local_site, local_site_name):
        if with_local_site:
            local_site = self.get_local_site(name=local_site_name)
        else:
            local_site = None
        account = HostingServiceAccount.objects.create(service_name=b'googlecode', username=b'bob', local_site=local_site)
        return (
         get_hosting_service_account_item_url(account, local_site_name),
         hosting_service_account_item_mimetype,
         account)