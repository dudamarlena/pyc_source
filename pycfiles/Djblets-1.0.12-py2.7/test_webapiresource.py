# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-x86_64/egg/djblets/webapi/tests/test_webapiresource.py
# Compiled at: 2019-06-12 01:17:17
from __future__ import print_function, unicode_literals
import warnings
from django.contrib.auth.models import User
from django.db.models import Model
from django.test.client import RequestFactory
from django.utils import six
from djblets.testing.testcases import TestCase
from djblets.webapi.resources.base import WebAPIResource
from djblets.webapi.resources.registry import register_resource_for_model, unregister_resource_for_model, unregister_resource

class WebAPIResourceTests(TestCase):
    """Unit tests for djblets.webapi.resources.base."""

    def setUp(self):
        super(WebAPIResourceTests, self).setUp()
        self.factory = RequestFactory()
        self.test_resource = None
        return

    def tearDown(self):
        super(WebAPIResourceTests, self).tearDown()
        if self.test_resource:
            unregister_resource(self.test_resource)

    def test_vendor_mimetypes(self):
        """Testing WebAPIResource with vendor-specific mimetypes"""

        class TestResource(WebAPIResource):
            mimetype_vendor = b'djblets'

        self.test_resource = TestResource()
        item_mimetypes = [ mimetype[b'item'] for mimetype in self.test_resource.allowed_mimetypes if b'item' in mimetype
                         ]
        list_mimetypes = [ mimetype[b'list'] for mimetype in self.test_resource.allowed_mimetypes if b'list' in mimetype
                         ]
        self.assertEqual(len(list_mimetypes), 4)
        self.assertEqual(len(item_mimetypes), 4)
        self.assertTrue(b'application/json' in list_mimetypes)
        self.assertTrue(b'application/xml' in list_mimetypes)
        self.assertTrue(b'application/vnd.djblets.testresources+json' in list_mimetypes)
        self.assertTrue(b'application/vnd.djblets.testresources+xml' in list_mimetypes)
        self.assertTrue(b'application/json' in item_mimetypes)
        self.assertTrue(b'application/xml' in item_mimetypes)
        self.assertTrue(b'application/vnd.djblets.testresource+json' in item_mimetypes)
        self.assertTrue(b'application/vnd.djblets.testresource+xml' in item_mimetypes)

    def test_vendor_mimetypes_with_custom(self):
        """Testing WebAPIResource with vendor-specific and custom mimetypes"""

        class TestResource(WebAPIResource):
            mimetype_vendor = b'djblets'
            allowed_mimetypes = WebAPIResource.allowed_mimetypes + [{b'item': b'text/html'}]

        self.test_resource = TestResource()
        item_mimetypes = [ mimetype[b'item'] for mimetype in self.test_resource.allowed_mimetypes if b'item' in mimetype
                         ]
        list_mimetypes = [ mimetype[b'list'] for mimetype in self.test_resource.allowed_mimetypes if b'list' in mimetype
                         ]
        self.assertEqual(len(list_mimetypes), 4)
        self.assertEqual(len(item_mimetypes), 5)
        self.assertTrue(b'application/json' in list_mimetypes)
        self.assertTrue(b'application/xml' in list_mimetypes)
        self.assertTrue(b'application/vnd.djblets.testresources+json' in list_mimetypes)
        self.assertTrue(b'application/vnd.djblets.testresources+xml' in list_mimetypes)
        self.assertTrue(b'application/json' in item_mimetypes)
        self.assertTrue(b'application/xml' in item_mimetypes)
        self.assertTrue(b'application/vnd.djblets.testresource+json' in item_mimetypes)
        self.assertTrue(b'application/vnd.djblets.testresource+xml' in item_mimetypes)
        self.assertTrue(b'application/vnd.djblets.testresource+xml' in item_mimetypes)
        self.assertTrue(b'text/html' in item_mimetypes)

    def test_get_with_vendor_mimetype(self):
        """Testing WebAPIResource with GET and vendor-specific mimetypes"""

        class TestResource(WebAPIResource):
            allowed_methods = ('GET', 'POST', 'PUT', 'DELETE')
            mimetype_vendor = b'djblets'
            uri_object_key = b'id'

            def get(self, *args, **kwargs):
                return (
                 200, {})

            create = get
            update = get
            delete = get

        self.test_resource = TestResource()
        self._test_mimetype_responses(self.test_resource, b'/api/tests/', b'application/vnd.djblets.testresources+json', b'application/vnd.djblets.testresources+xml')
        self._test_mimetype_responses(self.test_resource, b'/api/tests/', b'application/vnd.djblets.testresource+json', b'application/vnd.djblets.testresource+xml', method=b'post')
        self._test_mimetype_responses(self.test_resource, b'/api/tests/1/', b'application/vnd.djblets.testresource+json', b'application/vnd.djblets.testresource+xml', view_kwargs={b'id': 1}, method=b'put')
        self._test_mimetype_responses(self.test_resource, b'/api/tests/1/', b'application/vnd.djblets.testresource+json', b'application/vnd.djblets.testresource+xml', view_kwargs={b'id': 1}, method=b'delete')

    def test_get_with_item_mimetype(self):
        """Testing WebAPIResource with GET and Item-Content-Type header"""

        class TestResource(WebAPIResource):
            allowed_methods = ('GET', 'POST', 'PUT', 'DELETE')
            mimetype_vendor = b'djblets'
            uri_object_key = b'id'

            def get(self, *args, **kwargs):
                return (
                 200, {})

            create = get
            update = get
            delete = get

        self.test_resource = TestResource()
        self._test_item_mimetype_responses(self.test_resource, b'/api/tests/', b'application/vnd.djblets.testresources+json', b'application/vnd.djblets.testresources+xml', b'application/vnd.djblets.testresource+json', b'application/vnd.djblets.testresource+xml')
        self._test_item_mimetype_responses(self.test_resource, b'/api/tests/', b'application/vnd.djblets.testresource+json', b'application/vnd.djblets.testresource+xml', None, None, method=b'post')
        self._test_item_mimetype_responses(self.test_resource, b'/api/tests/1/', b'application/vnd.djblets.testresource+json', b'application/vnd.djblets.testresource+xml', None, None, view_kwargs={b'id': 1}, method=b'put')
        self._test_item_mimetype_responses(self.test_resource, b'/api/tests/', b'application/vnd.djblets.testresources+json', b'application/vnd.djblets.testresources+xml', b'application/vnd.djblets.testresource+json', b'application/vnd.djblets.testresource+xml')
        self._test_item_mimetype_responses(self.test_resource, b'/api/tests/1/', b'application/vnd.djblets.testresource+json', b'application/vnd.djblets.testresource+xml', None, None, view_kwargs={b'id': 1}, method=b'delete')
        return

    def test_generate_etag_with_encode_etag_true(self):
        """Testing WebAPIResource.generate_etag with encode_etag=True"""

        class TestObject(object):
            my_field = b'abc'

        request = RequestFactory().request()
        request.user = User()
        resource = WebAPIResource()
        with warnings.catch_warnings(record=True) as (w):
            etag = resource.generate_etag(TestObject(), [b'my_field'], request, encode_etag=True)
            self.assertEqual(len(w), 1)
            self.assertIn(b'generate_etag will stop generating', six.text_type(w[0].message))
        self.assertEqual(etag, b'416c0aecaf0b1e8ec64104349ba549c7534861f2')

    def test_generate_etag_with_encode_etag_false(self):
        """Testing WebAPIResource.generate_etag with encode_etag=False"""

        class TestObject(object):
            my_field = b'abc'

        request = RequestFactory().request()
        request.user = User()
        resource = WebAPIResource()
        obj = TestObject()
        with warnings.catch_warnings(record=True) as (w):
            etag = resource.generate_etag(obj, None, request, encode_etag=False)
            self.assertEqual(len(w), 0)
        self.assertEqual(etag, repr(resource.serialize_object(obj, request=request)))
        return

    def test_are_cache_headers_current_with_old_last_modified(self):
        """Testing WebAPIResource.are_cache_headers_current with old last
        modified timestamp
        """
        request = RequestFactory().request()
        request.META[b'HTTP_IF_MODIFIED_SINCE'] = b'Wed, 14 Jan 2015 13:49:10 GMT'
        resource = WebAPIResource()
        self.assertFalse(resource.are_cache_headers_current(request, last_modified=b'Wed, 14 Jan 2015 12:10:13 GMT'))

    def test_are_cache_headers_current_with_current_last_modified(self):
        """Testing WebAPIResource.are_cache_headers_current with current last
        modified timestamp
        """
        timestamp = b'Wed, 14 Jan 2015 13:49:10 GMT'
        request = RequestFactory().request()
        request.META[b'HTTP_IF_MODIFIED_SINCE'] = timestamp
        resource = WebAPIResource()
        self.assertTrue(resource.are_cache_headers_current(request, last_modified=timestamp))

    def test_are_cache_headers_current_with_old_etag(self):
        """Testing WebAPIResource.are_cache_headers_current with old ETag"""
        request = RequestFactory().request()
        request.META[b'HTTP_IF_NONE_MATCH'] = b'abc123'
        resource = WebAPIResource()
        self.assertFalse(resource.are_cache_headers_current(request, etag=b'def456'))

    def test_are_cache_headers_current_with_current_etag(self):
        """Testing WebAPIResource.are_cache_headers_current with current
        ETag
        """
        etag = b'abc123'
        request = RequestFactory().request()
        request.META[b'HTTP_IF_NONE_MATCH'] = etag
        resource = WebAPIResource()
        self.assertTrue(resource.are_cache_headers_current(request, etag=etag))

    def test_serialize_object_with_only_fields(self):
        """Testing WebAPIResource.serialize_object with
        ?only-fields=<fields>
        """

        class TestObject(object):
            field1 = b'abc'
            field2 = b'def'
            field3 = b'ghi'

        class TestResource(WebAPIResource):
            fields = {b'field1': {b'type': six.text_type}, 
               b'field2': {b'type': six.text_type}, 
               b'field3': {b'type': six.text_type}}

        request = RequestFactory().get(b'/api/test/?only-fields=field1,field3')
        resource = TestResource()
        data = resource.serialize_object(TestObject(), request=request)
        self.assertEqual(data, {b'field1': b'abc', 
           b'field3': b'ghi', 
           b'links': {b'self': {b'href': b'http://testserver/api/test/?only-fields=field1,field3', 
                                b'method': b'GET'}}})

    def test_serialize_object_with_only_fields_blank(self):
        """Testing WebAPIResource.serialize_object with ?only-fields="""

        class TestObject(object):
            field1 = b'abc'
            field2 = b'def'
            field3 = b'ghi'

        class TestResource(WebAPIResource):
            fields = {b'field1': {b'type': six.text_type}, 
               b'field2': {b'type': six.text_type}, 
               b'field3': {b'type': six.text_type}}

        request = RequestFactory().get(b'/api/test/?only-fields=')
        resource = TestResource()
        data = resource.serialize_object(TestObject(), request=request)
        self.assertEqual(data, {b'links': {b'self': {b'href': b'http://testserver/api/test/?only-fields=', 
                                b'method': b'GET'}}})

    def test_serialize_object_with_only_fields_and_expand(self):
        """Testing WebAPIResource.serialize_object with
        ?only-fields=<field>&expand=<field>
        """

        class TestModel(Model):
            field = b'test'

            def __init__(self, pk):
                self.pk = pk

            def __deepcopy__(self, other):
                return TestModel()

            def __str__(self):
                return b'Test'

        class TestObject(object):
            field1 = b'abc'
            field2 = TestModel(1)
            field3 = TestModel(2)

        class TestResource1(WebAPIResource):
            fields = {b'field': {b'type': six.text_type}}

            def get_href(self, *args, **kwargs):
                return b'http://testserver/api/test1/'

        class TestResource2(WebAPIResource):
            fields = {b'field1': {b'type': six.text_type}, 
               b'field2': {b'type': TestModel}, 
               b'field3': {b'type': TestModel}}

            def get_serializer_for_object(self, o):
                if isinstance(o, TestModel):
                    return TestResource1()
                else:
                    return self

        request = RequestFactory().get(b'/api/test2/?only-fields=field2&expand=field2')
        resource = TestResource2()
        obj = TestObject()
        data = resource.serialize_object(obj, request=request)
        self.assertEqual(data, {b'field2': {b'links': {b'self': {b'href': b'http://testserver/api/test1/', 
                                            b'method': b'GET'}}}, 
           b'links': {b'self': {b'href': b'http://testserver/api/test2/?only-fields=field2&expand=field2', 
                                b'method': b'GET'}, 
                      b'field3': {b'href': b'http://testserver/api/test1/', 
                                  b'method': b'GET', 
                                  b'title': b'Test'}}})

    def test_serialize_object_with_only_links(self):
        """Testing WebAPIResource.serialize_object with ?only-links=<links>"""

        class TestObject(object):
            field1 = b'abc'
            field2 = b'def'
            field3 = b'ghi'

        class TestResource(WebAPIResource):
            allowed_methods = ('GET', 'POST', 'PUT', 'DELETE')
            fields = {b'field1': {b'type': six.text_type}, 
               b'field2': {b'type': six.text_type}, 
               b'field3': {b'type': six.text_type}}

        request = RequestFactory().get(b'/api/test/?only-links=delete,update')
        resource = TestResource()
        data = resource.serialize_object(TestObject(), request=request)
        self.assertEqual(data, {b'field1': b'abc', 
           b'field2': b'def', 
           b'field3': b'ghi', 
           b'links': {b'delete': {b'href': b'http://testserver/api/test/', 
                                  b'method': b'DELETE'}, 
                      b'update': {b'href': b'http://testserver/api/test/', 
                                  b'method': b'PUT'}}})

    def test_serialize_object_with_only_links_blank(self):
        """Testing WebAPIResource.serialize_object with ?only-links="""

        class TestObject(object):
            field1 = b'abc'
            field2 = b'def'
            field3 = b'ghi'

        class TestResource(WebAPIResource):
            allowed_methods = ('GET', 'POST', 'PUT', 'DELETE')
            fields = {b'field1': {b'type': six.text_type}, 
               b'field2': {b'type': six.text_type}, 
               b'field3': {b'type': six.text_type}}

        request = RequestFactory().get(b'/api/test/?only-links=')
        resource = TestResource()
        data = resource.serialize_object(TestObject(), request=request)
        self.assertEqual(data, {b'field1': b'abc', 
           b'field2': b'def', 
           b'field3': b'ghi'})

    def test_serialize_object_with_cache_copy(self):
        """Testing WebAPIResource.serialize_object always returns a copy of
        the cached data
        """

        class TestObject(object):
            my_field = b'abc'

        request = RequestFactory().request()
        request.user = User()
        resource = WebAPIResource()
        resource.fields = {b'my_field': {b'type': six.text_type}}
        obj = TestObject()
        data = resource.serialize_object(obj, request=request)
        self.assertIn(b'my_field', data)
        del data[b'my_field']
        data = resource.serialize_object(obj, request=request)
        self.assertIn(b'my_field', data)
        del data[b'my_field']
        data = resource.serialize_object(obj, request=request)
        self.assertIn(b'my_field', data)

    def _test_mimetype_responses(self, resource, url, json_mimetype, xml_mimetype, **kwargs):
        self._test_mimetype_response(resource, url, b'*/*', json_mimetype, **kwargs)
        self._test_mimetype_response(resource, url, b'application/json', json_mimetype, **kwargs)
        self._test_mimetype_response(resource, url, json_mimetype, json_mimetype, **kwargs)
        self._test_mimetype_response(resource, url, b'application/xml', xml_mimetype, **kwargs)
        self._test_mimetype_response(resource, url, xml_mimetype, xml_mimetype, **kwargs)

    def _test_mimetype_response(self, resource, url, accept_mimetype, response_mimetype, method=b'get', view_kwargs={}):
        func = getattr(self.factory, method)
        if accept_mimetype:
            request = func(url, HTTP_ACCEPT=accept_mimetype)
        else:
            request = func(url)
        response = resource(request, **view_kwargs)
        print(response)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response[b'Content-Type'], response_mimetype)

    def test_serialize_object_with_circular_references(self):
        """Testing WebAPIResource.serialize_object with circular references and
        ?expand=
        """

        class TestObject(Model):

            def __init__(self, name, pk):
                super(TestObject, self).__init__()
                self.name = name
                self.pk = pk

        class TestResource(WebAPIResource):
            fields = {b'dependency': {b'type': [
                                       TestObject]}, 
               b'name': {b'type': six.text_type}}

        try:
            obj1 = TestObject(b'obj1', 1)
            obj2 = TestObject(b'obj2', 2)
            obj1.dependency = obj2
            obj2.dependency = obj1
            request = RequestFactory().get(b'/api/test/?expand=dependency')
            resource = TestResource()
            register_resource_for_model(TestObject, resource)
            data = resource.serialize_object(obj1, request=request)
            self.maxDiff = 100000
            self.assertEqual(data, {b'dependency': {b'links': {b'dependency': {b'href': None, 
                                                          b'method': b'GET', 
                                                          b'title': b'TestObject object'}, 
                                          b'self': {b'href': b'http://testserver/api/test/?expand=dependency', 
                                                    b'method': b'GET'}}, 
                               b'name': b'obj2'}, 
               b'links': {b'self': {b'href': b'http://testserver/api/test/?expand=dependency', 
                                    b'method': b'GET'}}, 
               b'name': b'obj1'})
        finally:
            unregister_resource_for_model(TestObject)

        return

    def _test_item_mimetype_responses(self, resource, url, json_mimetype, xml_mimetype, json_item_mimetype, xml_item_mimetype, **kwargs):
        self._test_item_mimetype_response(resource, url, b'*/*', json_item_mimetype, **kwargs)
        self._test_item_mimetype_response(resource, url, b'application/json', json_item_mimetype, **kwargs)
        self._test_item_mimetype_response(resource, url, json_mimetype, json_item_mimetype, **kwargs)
        self._test_item_mimetype_response(resource, url, b'application/xml', xml_item_mimetype, **kwargs)
        self._test_item_mimetype_response(resource, url, xml_mimetype, xml_item_mimetype, **kwargs)

    def _test_item_mimetype_response(self, resource, url, accept_mimetype, response_item_mimetype=None, method=b'get', view_kwargs={}):
        func = getattr(self.factory, method)
        if accept_mimetype:
            request = func(url, HTTP_ACCEPT=accept_mimetype)
        else:
            request = func(url)
        response = resource(request, **view_kwargs)
        print(response)
        self.assertEqual(response.status_code, 200)
        if response_item_mimetype:
            self.assertEqual(response[b'Item-Content-Type'], response_item_mimetype)
        else:
            self.assertTrue(b'Item-Content-Type' not in response)