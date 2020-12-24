# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/reviewboard/webapi/tests/test_hosting_service.py
# Compiled at: 2020-02-11 04:03:57
from __future__ import unicode_literals
from django.utils import six
from reviewboard.hostingsvcs.service import get_hosting_services, get_hosting_service
from reviewboard.webapi.resources import resources
from reviewboard.webapi.tests.base import BaseWebAPITestCase
from reviewboard.webapi.tests.mimetypes import hosting_service_item_mimetype, hosting_service_list_mimetype
from reviewboard.webapi.tests.mixins import BasicTestsMetaclass
from reviewboard.webapi.tests.urls import get_hosting_service_item_url, get_hosting_service_list_url

def _compare_item(self, item_rsp, hosting_service):
    self.assertEqual(item_rsp[b'id'], hosting_service.hosting_service_id)
    self.assertEqual(item_rsp[b'name'], hosting_service.name)
    self.assertEqual(item_rsp[b'needs_authorization'], hosting_service.needs_authorization)
    self.assertEqual(item_rsp[b'supports_bug_trackers'], hosting_service.supports_bug_trackers)
    self.assertEqual(item_rsp[b'supports_repositories'], hosting_service.supports_repositories)
    self.assertEqual(item_rsp[b'supports_two_factor_auth'], hosting_service.supports_two_factor_auth)
    self.assertEqual(item_rsp[b'supported_scmtools'], hosting_service.supported_scmtools)
    url_base = b'http://testserver/'
    if b'/s/local-site-1/' in item_rsp[b'links'][b'self'][b'href']:
        url_base += b's/local-site-1/'
    url_base += b'api/'
    accounts_url = url_base + b'hosting-service-accounts/?service=%s' % hosting_service.hosting_service_id
    self.assertIn(b'accounts', item_rsp[b'links'])
    self.assertEqual(item_rsp[b'links'][b'accounts'][b'href'], accounts_url)
    accounts_url = url_base + b'repositories/?hosting-service=%s' % hosting_service.hosting_service_id
    self.assertIn(b'repositories', item_rsp[b'links'])
    self.assertEqual(item_rsp[b'links'][b'repositories'][b'href'], accounts_url)


@six.add_metaclass(BasicTestsMetaclass)
class ResourceListTests(BaseWebAPITestCase):
    """Testing the HostingServiceResource list APIs."""
    fixtures = [
     b'test_users']
    sample_api_url = b'hosting-services/'
    resource = resources.hosting_service
    compare_item = _compare_item

    def setup_http_not_allowed_list_test(self, user):
        return get_hosting_service_list_url()

    def setup_basic_get_test(self, user, with_local_site, local_site_name, populate_items):
        return (
         get_hosting_service_list_url(local_site_name),
         hosting_service_list_mimetype,
         get_hosting_services())


@six.add_metaclass(BasicTestsMetaclass)
class ResourceItemTests(BaseWebAPITestCase):
    """Testing the HostingServiceResource item APIs."""
    fixtures = [
     b'test_users']
    sample_api_url = b'hosting-services/<id>/'
    resource = resources.hosting_service
    compare_item = _compare_item

    def setup_http_not_allowed_item_test(self, user):
        hosting_service = get_hosting_service(b'github')
        return get_hosting_service_item_url(hosting_service)

    def setup_basic_get_test(self, user, with_local_site, local_site_name):
        hosting_service = get_hosting_service(b'github')
        return (
         get_hosting_service_item_url(hosting_service, local_site_name),
         hosting_service_item_mimetype,
         hosting_service)