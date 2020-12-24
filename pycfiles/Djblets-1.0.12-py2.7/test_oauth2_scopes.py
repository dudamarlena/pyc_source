# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-x86_64/egg/djblets/webapi/tests/test_oauth2_scopes.py
# Compiled at: 2019-06-12 01:17:17
"""WebAPI scope dictionary tests."""
from __future__ import unicode_literals
from django.test.utils import override_settings
from django.utils import six
from oauth2_provider.settings import oauth2_settings
from djblets.extensions.extension import Extension
from djblets.extensions.manager import ExtensionManager
from djblets.extensions.models import RegisteredExtension
from djblets.extensions.testing.testcases import ExtensionTestCaseMixin
from djblets.testing.testcases import TestCase
from djblets.webapi.oauth2_scopes import ExtensionEnabledWebAPIScopeDictionary, WebAPIScopeDictionary, enable_web_api_scopes, get_scope_dictionary
from djblets.webapi.resources.mixins.oauth2_tokens import ResourceOAuth2TokenMixin
from djblets.webapi.testing.resources import make_resource_tree

class WebAPIScopeDictionaryTests(TestCase):
    """Tests for WebAPIScopeDictionary."""

    @classmethod
    def setUpClass(cls):
        super(WebAPIScopeDictionaryTests, cls).setUpClass()
        cls._resources = make_resource_tree(mixins=[
         ResourceOAuth2TokenMixin])

    def test_scope_dict(self):
        """Testing WebAPIScopeDictionary.scope_dict generates and caches scopes
        """
        scopes = WebAPIScopeDictionary(self._resources.root_resource)
        self.assertEqual(scopes.scope_dict, {b'root:read': b'Ability to perform HTTP GET on the root resource', 
           b'item-child:read': b'Ability to perform HTTP GET on the item-child resource', 
           b'item-child:write': b'Ability to perform HTTP PUT, POST on the item-child resource', 
           b'list-child:read': b'Ability to perform HTTP GET on the list-child resource', 
           b'list-child:destroy': b'Ability to perform HTTP DELETE on the list-child resource', 
           b'parent:read': b'Ability to perform HTTP GET on the parent resource'})

    def test_getitem(self):
        """Testing WebAPIScopeDictionary.__getitem__"""
        scopes = WebAPIScopeDictionary(self._resources.root_resource)
        self.assertEqual(scopes[b'root:read'], b'Ability to perform HTTP GET on the root resource')
        with self.assertRaises(KeyError):
            scopes[b'bad-key']

    def test_contains(self):
        """Testing WebAPIScopeDictionary.__contains__"""
        scopes = WebAPIScopeDictionary(self._resources.root_resource)
        self.assertIn(b'root:read', scopes)
        self.assertNotIn(b'bad-key', scopes)

    def test_iterkeys(self):
        """Testing WebAPIScopeDictionary with six.iterkeys"""
        scopes = WebAPIScopeDictionary(self._resources.root_resource)
        self.assertEqual(set(six.iterkeys(scopes)), {
         b'root:read',
         b'item-child:read',
         b'item-child:write',
         b'list-child:read',
         b'list-child:destroy',
         b'parent:read'})

    def test_clear(self):
        """Testing WebAPIScopeDictionary.clear"""
        scopes = WebAPIScopeDictionary(self._resources.root_resource)
        self.assertEqual(scopes.scope_dict, {b'root:read': b'Ability to perform HTTP GET on the root resource', 
           b'item-child:read': b'Ability to perform HTTP GET on the item-child resource', 
           b'item-child:write': b'Ability to perform HTTP PUT, POST on the item-child resource', 
           b'list-child:read': b'Ability to perform HTTP GET on the list-child resource', 
           b'list-child:destroy': b'Ability to perform HTTP DELETE on the list-child resource', 
           b'parent:read': b'Ability to perform HTTP GET on the parent resource'})
        scopes.clear()
        self.assertEqual(scopes._scope_dict, {})


class ExtensionEnabledWebAPIScopeDictionaryTests(ExtensionTestCaseMixin, TestCase):
    """Tests for ExtensionEnabledWebAPIScopeDictionary."""

    @classmethod
    def setUpClass(cls):
        super(ExtensionEnabledWebAPIScopeDictionaryTests, cls).setUpClass()
        cls._extension_manager = ExtensionManager(b'')
        cls._resources = make_resource_tree(mixins=[
         ResourceOAuth2TokenMixin], extension_manager=cls._extension_manager)

        class TestExtensionResource(cls._resources.base_resource):
            """An example resource on an extension."""
            name = b'test-ext'
            allowed_methods = ('GET', 'POST', 'PUT', 'DELETE')

        cls._extension_resource = TestExtensionResource()

        class TestExtension(Extension):
            """An example extension."""
            extension_id = b'djblets.webapi.tests.test_oauth2_scopes.TestExtension'
            resources = [cls._extension_resource]
            registration = RegisteredExtension()

        cls.extension_class = TestExtension

    def test_scope_dict(self):
        """Testing ExtensionEnabledWebAPIScopeDictionary.scope_dict generates
        and caches scopes
        """
        self.extension_mgr.disable_extension(self.extension_class.extension_id)
        scopes = ExtensionEnabledWebAPIScopeDictionary(self._resources.root_resource)
        original_scope_dict = scopes.scope_dict
        base_scopes = {b'root:read': b'Ability to perform HTTP GET on the root resource', 
           b'extension:read': b'Ability to perform HTTP GET on the extension resource', 
           b'extension:write': b'Ability to perform HTTP PUT on the extension resource', 
           b'item-child:read': b'Ability to perform HTTP GET on the item-child resource', 
           b'item-child:write': b'Ability to perform HTTP PUT, POST on the item-child resource', 
           b'list-child:read': b'Ability to perform HTTP GET on the list-child resource', 
           b'list-child:destroy': b'Ability to perform HTTP DELETE on the list-child resource', 
           b'parent:read': b'Ability to perform HTTP GET on the parent resource'}
        self.assertEqual(original_scope_dict, base_scopes)
        self.extension_mgr.enable_extension(self.extension_class.extension_id)
        self.assertEqual(scopes._scope_dict, {})
        new_base_scopes = dict({b'test-ext:read': b'Ability to perform HTTP GET on the test-ext resource', 
           b'test-ext:write': b'Ability to perform HTTP PUT, POST on the test-ext resource', 
           b'test-ext:destroy': b'Ability to perform HTTP DELETE on the test-ext resource'}, **base_scopes)
        new_scope_dict = scopes.scope_dict
        self.assertIs(new_scope_dict, original_scope_dict)
        self.assertEqual(new_scope_dict, new_base_scopes)
        self.extension_mgr.disable_extension(self.extension_class.extension_id)
        self.assertEqual(scopes._scope_dict, {})
        newest_scope_dict = scopes.scope_dict
        self.assertIs(newest_scope_dict, new_scope_dict)
        self.assertIs(newest_scope_dict, original_scope_dict)
        self.assertEqual(newest_scope_dict, base_scopes)


class ScopeEnablingTests(TestCase):
    """Tests for enabling WebAPI scopes at runtime."""

    @override_settings(WEB_API_ROOT_RESOURCE=b'djblets.webapi.tests.test_oauth2_auth.root_resource')
    def test_enable_webapi_scopes(self):
        """Testing enable_web_api_scopes()"""
        enable_web_api_scopes()
        scopes = get_scope_dictionary()
        self.assertIs(oauth2_settings.SCOPES, scopes)
        self.assertEqual(set(oauth2_settings._SCOPES), {
         b'root:read',
         b'item-child:read',
         b'item-child:write',
         b'list-child:read',
         b'list-child:destroy',
         b'parent:read'})