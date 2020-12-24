# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/reviewboard/webapi/tests/test_server_info.py
# Compiled at: 2020-02-11 04:03:57
from __future__ import unicode_literals
from django.conf import settings
from django.utils import six
from reviewboard import get_version_string, get_package_version, is_release
from reviewboard.admin.server import get_server_url
from reviewboard.webapi.resources import resources
from reviewboard.webapi.server_info import get_capabilities
from reviewboard.webapi.tests.base import BaseWebAPITestCase
from reviewboard.webapi.tests.mimetypes import server_info_mimetype
from reviewboard.webapi.tests.mixins import BasicTestsMetaclass
from reviewboard.webapi.tests.urls import get_server_info_url

@six.add_metaclass(BasicTestsMetaclass)
class ResourceTests(BaseWebAPITestCase):
    """Testing the ServerInfoResource APIs."""
    fixtures = [
     b'test_users']
    sample_api_url = b'info/'
    resource = resources.server_info

    def setup_http_not_allowed_list_test(self, user):
        return get_server_info_url()

    def setup_http_not_allowed_item_test(self, user):
        return get_server_info_url()

    def compare_item(self, item_rsp, obj):
        self.assertIn(b'product', item_rsp)
        self.assertIn(b'site', item_rsp)
        self.assertIn(b'capabilities', item_rsp)
        product_rsp = item_rsp[b'product']
        self.assertEqual(product_rsp[b'name'], b'Review Board')
        self.assertEqual(product_rsp[b'version'], get_version_string())
        self.assertEqual(product_rsp[b'package_version'], get_package_version())
        self.assertEqual(product_rsp[b'is_release'], is_release())
        site_rsp = item_rsp[b'site']
        self.assertTrue(site_rsp[b'url'].startswith(get_server_url()))
        self.assertEqual(site_rsp[b'administrators'], [ {b'name': name, b'email': email} for name, email in settings.ADMINS
                                                      ])
        self.assertEqual(site_rsp[b'time_zone'], settings.TIME_ZONE)
        self.assertEqual(item_rsp[b'capabilities'], get_capabilities())

    def setup_basic_get_test(self, user, with_local_site, local_site_name):
        return (
         get_server_info_url(local_site_name),
         server_info_mimetype,
         None)