# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/reviewboard/webapi/tests/test_base.py
# Compiled at: 2020-02-11 04:03:57
"""Generic unit tests for Web API resources"""
from __future__ import unicode_literals
import json
from django.conf.urls import include, url
from django.core.urlresolvers import clear_url_caches
from djblets.features import Feature, get_features_registry
from djblets.testing.decorators import add_fixtures
from djblets.webapi.errors import PERMISSION_DENIED
from reviewboard.site.models import LocalSite
from reviewboard.webapi.base import WebAPIResource
from reviewboard.webapi.tests.base import BaseWebAPITestCase
urlpatterns = []

class TestingFeature(Feature):
    """A dummy feature for testing."""
    feature_id = b'test.feature'
    name = b'Test Feature'
    summary = b'A testing feature'


class BaseTestingResource(WebAPIResource):
    """A testing resource for testing required_features."""
    allowed_methods = ('GET', 'POST', 'PUT', 'DELETE')
    uri_object_key = b'obj_id'

    def has_access_permissions(self, *args, **kwargs):
        return True

    def has_list_access_permissions(self, *args, **kwargs):
        return True

    def has_modify_permissions(self, *args, **kwargs):
        return True

    def has_delete_permissions(self, *args, **kwargs):
        return True

    def get(self, request, obj_id=None, *args, **kwargs):
        return (418, {b'obj_id': obj_id})

    def get_list(self, request, obj_id=None, *args, **kwargs):
        return (418, {b'obj_id': obj_id})

    def update(self, request, obj_id=None, *args, **kwargs):
        return (418, {b'obj_id': obj_id})

    def create(self, request, obj_id=None, *args, **kwargs):
        return (418, {b'obj_id': obj_id})

    def delete(self, request, obj_id=None, *args, **kwargs):
        return (418, {b'obj_id': obj_id})


class WebAPIResourceFeatureTests(BaseWebAPITestCase):
    """Tests for Web API Resources with required features"""

    @classmethod
    def setUpClass(cls):
        super(WebAPIResourceFeatureTests, cls).setUpClass()
        cls.feature = TestingFeature()

        class TestingResource(BaseTestingResource):
            required_features = [
             cls.feature]

        cls.resource_cls = TestingResource
        cls.resource = cls.resource_cls()
        urlpatterns.append(url(b'^/api/', include(cls.resource.get_url_patterns())))
        urlpatterns.append(url(b'^s/(?P<local_site_name>[\\w\\.-]+)', include(list(urlpatterns))))

    @classmethod
    def tearDownClass(cls):
        super(WebAPIResourceFeatureTests, cls).tearDownClass()
        registry = get_features_registry()
        registry.unregister(cls.feature)
        del urlpatterns[:]

    def test_disabled_feature_post(self):
        """Testing POST with a disabled required feature returns
        PERMISSION_DENIED
        """
        self._test_method(b'post', feature_enabled=False)

    def test_disabled_feature_get_list(self):
        """Testing GET with a disabled required feature returns
        PERMISSION_DENIED for a list_resource
        """
        self._test_method(b'get', feature_enabled=False)

    def test_disabled_feature_get(self):
        """Testing GET with a disabled required feature returns
        PERMISSION_DENIED
        """
        self._test_method(b'get', feature_enabled=False, obj_id=b'123')

    def test_disabled_feature_delete(self):
        """Testing DELETE with a disabled required feature returns
        PERMISSION_DENIED
        """
        self._test_method(b'delete', feature_enabled=False, obj_id=b'123')

    def test_disabled_feature_forbidden_update(self):
        """Testing PUT with a disabled required feature returns
        PERMISSION_DENIED
        """
        self._test_method(b'put', feature_enabled=False, obj_id=b'123')

    def test_enabled_feature_post(self):
        """Testing POST with an enabled required feature returns the correct
        response
        """
        self._test_method(b'post', feature_enabled=True)

    def test_enabled_feature_get_list(self):
        """Testing GET with an enabled required feature returns the correct
        response for a list resource
        """
        self._test_method(b'get', feature_enabled=True)

    def test_enabled_feature_get(self):
        """Testing GET with an enabled required feature returns the correct
        response
        """
        self._test_method(b'get', feature_enabled=True, obj_id=b'123')

    def test_enabled_feature_delete(self):
        """Testing DELETE with an enabled required feature returns the correct
        response
        """
        self._test_method(b'delete', feature_enabled=True, obj_id=b'123')

    def test_enabled_feature_update(self):
        """Testing PUT with an enabled required feature returns the correct
        response
        """
        self._test_method(b'put', feature_enabled=True, obj_id=b'123')

    @add_fixtures([b'test_site'])
    def test_disabled_feature_post_local_site(self):
        """Testing POST with a disabled required feature returns
        PERMISSION_DENIED on a LocalSite
        """
        self._test_method(b'post', feature_enabled=False, feature_local_site_enabled=False, local_site=LocalSite.objects.get(name=b'local-site-1'))

    @add_fixtures([b'test_site'])
    def test_disabled_feature_get_list_local_site(self):
        """Testing GET with a disabled required feature returns
        PERMISSION_DENIED for a list_resource on a LocalSite
        """
        self._test_method(b'get', feature_enabled=False)

    @add_fixtures([b'test_site'])
    def test_disabled_feature_get_local_site(self):
        """Testing GET with a disabled required feature returns
        PERMISSION_DENIED on a LocalSite
        """
        self._test_method(b'get', feature_enabled=False, feature_local_site_enabled=False, obj_id=b'123', local_site=LocalSite.objects.get(name=b'local-site-1'))

    @add_fixtures([b'test_site'])
    def test_disabled_feature_delete_local_site(self):
        """Testing DELETE with a disabled required feature returns
        PERMISSION_DENIED on a LocalSite
        """
        self._test_method(b'delete', feature_enabled=False, feature_local_site_enabled=False, obj_id=b'123', local_site=LocalSite.objects.get(name=b'local-site-1'))

    @add_fixtures([b'test_site'])
    def test_disabled_feature_forbidden_update_local_site(self):
        """Testing PUT with a disabled required feature returns
        PERMISSION_DENIED on a LocalSite
        """
        self._test_method(b'put', feature_enabled=False, feature_local_site_enabled=False, obj_id=b'123', local_site=LocalSite.objects.get(name=b'local-site-1'))

    @add_fixtures([b'test_site'])
    def test_enabled_feature_post_local_site(self):
        """Testing POST with an enabled required feature returns the correct
        response on a LocalSite
        """
        self._test_method(b'post', feature_enabled=False, feature_local_site_enabled=True, local_site=LocalSite.objects.get(name=b'local-site-1'))

    @add_fixtures([b'test_site'])
    def test_globally_enabled_feature_post_local_site(self):
        """Testing POST with a globally enabled but locally disabled required
        feature returns the correct response on a LocalSite
        """
        self._test_method(b'post', feature_enabled=True, feature_local_site_enabled=False, local_site=LocalSite.objects.get(name=b'local-site-1'))

    @add_fixtures([b'test_site'])
    def test_enabled_feature_get_list_local_site(self):
        """Testing GET with an enabled required feature returns the correct
        response for a list resource on a LocalSite
        """
        self._test_method(b'get', feature_enabled=False, feature_local_site_enabled=True, local_site=LocalSite.objects.get(name=b'local-site-1'))

    @add_fixtures([b'test_site'])
    def test_globally_enabled_feature_get_list_local_site(self):
        """Testing GET with a globally enabled but locally disabled required
        feature returns the correct response on a LocalSite
        """
        self._test_method(b'get', feature_enabled=True, feature_local_site_enabled=False, local_site=LocalSite.objects.get(name=b'local-site-1'))

    @add_fixtures([b'test_site'])
    def test_enabled_feature_get_local_site(self):
        """Testing GET with an enabled required feature returns the correct
        response on a LocalSite
        """
        self._test_method(b'get', feature_enabled=False, feature_local_site_enabled=True, obj_id=b'123', local_site=LocalSite.objects.get(name=b'local-site-1'))

    @add_fixtures([b'test_site'])
    def test_globally_enabled_feature_get_local_site(self):
        """Testing GET with a globally enabled but locally disabled required
        feature returns the correct response on a LocalSite
        """
        self._test_method(b'get', feature_enabled=True, feature_local_site_enabled=False, obj_id=b'123', local_site=LocalSite.objects.get(name=b'local-site-1'))

    @add_fixtures([b'test_site'])
    def test_enabled_feature_delete_local_site(self):
        """Testing DELETE with an enabled required feature returns the correct
        response on a LocalSite
        """
        self._test_method(b'delete', feature_enabled=False, feature_local_site_enabled=True, obj_id=b'123', local_site=LocalSite.objects.get(name=b'local-site-1'))

    @add_fixtures([b'test_site'])
    def test_globally_enabled_feature_delete_local_site(self):
        """Testing DELETE with a globally enabled but locally disabled required
        feature returns the correct response on a LocalSite
        """
        self._test_method(b'delete', feature_enabled=True, feature_local_site_enabled=False, obj_id=b'123', local_site=LocalSite.objects.get(name=b'local-site-1'))

    @add_fixtures([b'test_site'])
    def test_enabled_feature_update_local_site(self):
        """Testing PUT with an enabled required feature returns the correct
        response on a LocalSite
        """
        self._test_method(b'put', feature_enabled=False, feature_local_site_enabled=True, obj_id=b'123', local_site=LocalSite.objects.get(name=b'local-site-1'))

    @add_fixtures([b'test_site'])
    def test_globally_enabled_feature_put_local_site(self):
        """Testing PUT with a globally enabled but locally disabled required
        feature returns the correct response on a LocalSite
        """
        self._test_method(b'put', feature_enabled=True, feature_local_site_enabled=False, obj_id=b'123', local_site=LocalSite.objects.get(name=b'local-site-1'))

    def _test_method(self, method, feature_enabled, local_site=None, feature_local_site_enabled=None, obj_id=None):
        """Test an HTTP method on the resource.

        Args:
            method (unicode):
                The HTTP method (e.g., ``"POST"`` or ``"PUT"``).

            feature_enabled (bool):
                Whether or not the feature should be enabled globally.

            local_site (reviewboard.site.models.LocalSite, optional):
                If provided, the request will be made against the API using the
                given LocalSite.

            feature_local_site_enabled (bool, optional):
                Whether or not the feature is enabled on the given LocalSite.

                This argument must be provided if ``local_site`` is provided,

            obj_id (unicode, optional):
                If provided, the request will be made against the item
                resource. Otherwise the request is made against the list
                resource.
        """
        if local_site is not None:
            if feature_local_site_enabled is None:
                raise ValueError(b'feature_local_site_enabled must not be None')
            if not local_site.extra_data:
                local_site.extra_data = {}
            local_site.extra_data[b'enabled_features'] = {TestingFeature.feature_id: feature_local_site_enabled}
            local_site.save(update_fields=('extra_data', ))
        method = getattr(self.client, method)
        local_site_name = None
        if local_site:
            local_site_name = local_site.name
        settings = {b'ENABLED_FEATURES': {TestingFeature.feature_id: feature_enabled}, 
           b'ROOT_URLCONF': b'reviewboard.webapi.tests.test_base'}
        try:
            clear_url_caches()
            with self.settings(**settings):
                if obj_id is None:
                    resource_url = self.resource.get_list_url(local_site_name=local_site_name)
                else:
                    resource_url = self.resource.get_item_url(local_site_name=local_site_name, obj_id=obj_id)
                rsp = method(resource_url)
        finally:
            clear_url_caches()

        content = json.loads(rsp.content)
        if feature_enabled or feature_local_site_enabled:
            self.assertEqual(rsp.status_code, 418)
            self.assertEqual(content[b'stat'], b'ok')
            self.assertEqual(content[b'obj_id'], obj_id)
        else:
            self.assertEqual(rsp.status_code, 403)
            self.assertEqual(content[b'stat'], b'fail')
            self.assertEqual(content[b'err'][b'msg'], PERMISSION_DENIED.msg)
            self.assertEqual(content[b'err'][b'code'], PERMISSION_DENIED.code)
        return