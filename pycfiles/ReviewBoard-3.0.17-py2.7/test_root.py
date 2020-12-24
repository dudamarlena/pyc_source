# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/reviewboard/webapi/tests/test_root.py
# Compiled at: 2020-02-11 04:03:57
from __future__ import unicode_literals
from django.utils import six
from djblets.testing.decorators import add_fixtures
from reviewboard.webapi.resources import resources
from reviewboard.webapi.tests.base import BaseWebAPITestCase
from reviewboard.webapi.tests.mimetypes import root_item_mimetype
from reviewboard.webapi.tests.mixins import BasicTestsMetaclass
from reviewboard.webapi.tests.urls import get_root_url

@six.add_metaclass(BasicTestsMetaclass)
class ResourceTests(BaseWebAPITestCase):
    """Testing the RootResource APIs."""
    fixtures = [
     b'test_users']
    sample_api_url = b'/'
    resource = resources.root
    test_http_methods = ('DELETE', 'PUT', 'POST')

    def setup_http_not_allowed_item_test(self, user):
        return get_root_url()

    def setup_http_not_allowed_list_test(self, user):
        return get_root_url()

    def test_get(self):
        """Testing the GET / API"""
        rsp = self.api_get(get_root_url(), expected_mimetype=root_item_mimetype)
        self.assertEqual(rsp[b'stat'], b'ok')
        self.assertIn(b'uri_templates', rsp)
        self.assertIn(b'repository', rsp[b'uri_templates'])
        self.assertEqual(rsp[b'uri_templates'][b'repository'], b'http://testserver/api/repositories/{repository_id}/')
        self._check_common_root_fields(rsp)

    @add_fixtures([b'test_users', b'test_site'])
    def test_get_with_site(self):
        """Testing the GET / API with local sites"""
        self._login_user(local_site=True)
        rsp = self.api_get(get_root_url(b'local-site-1'), expected_mimetype=root_item_mimetype)
        self.assertEqual(rsp[b'stat'], b'ok')
        self.assertIn(b'uri_templates', rsp)
        self.assertIn(b'repository', rsp[b'uri_templates'])
        self.assertEqual(rsp[b'uri_templates'][b'repository'], b'http://testserver/s/local-site-1/api/repositories/{repository_id}/')
        self._check_common_root_fields(rsp)

    @add_fixtures([b'test_users', b'test_site'])
    def test_get_with_site_no_access(self):
        """Testing the GET / API without access to local site"""
        self.api_get(get_root_url(b'local-site-1'), expected_status=403)

    @add_fixtures([b'test_users', b'test_site'])
    def test_get_with_site_and_cache(self):
        """Testing the GET / API with multiple local sites"""
        self.test_get_with_site()
        rsp = self.api_get(get_root_url(b'local-site-2'), expected_mimetype=root_item_mimetype)
        self.assertEqual(rsp[b'stat'], b'ok')
        self.assertIn(b'uri_templates', rsp)
        self.assertIn(b'repository', rsp[b'uri_templates'])
        self.assertEqual(rsp[b'uri_templates'][b'repository'], b'http://testserver/s/local-site-2/api/repositories/{repository_id}/')

    def _check_common_root_fields(self, item_rsp):
        self.assertIn(b'product', item_rsp)
        self.assertIn(b'site', item_rsp)
        self.assertIn(b'capabilities', item_rsp)
        caps = item_rsp[b'capabilities']
        self.assertIn(b'diffs', caps)
        diffs_caps = caps[b'diffs']
        self.assertTrue(diffs_caps[b'moved_files'])
        self.assertTrue(diffs_caps[b'base_commit_ids'])
        diff_validation_caps = diffs_caps[b'validation']
        self.assertTrue(diff_validation_caps[b'base_commit_ids'])
        review_request_caps = caps[b'review_requests']
        self.assertTrue(review_request_caps[b'commit_ids'])
        text_caps = caps[b'text']
        self.assertTrue(text_caps[b'markdown'])