# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/scaleway/tests/apis/test_api_account.py
# Compiled at: 2019-12-16 08:49:55
import unittest, uuid, httpretty, slumber
from scaleway.apis import AccountAPI
from scaleway.apis.api_account import BadToken, ExpiredToken
from . import FakeAPITestCase

class TestAccountAPI(FakeAPITestCase, unittest.TestCase):
    fake_permissions = {'compute': {'can_boot': [
                              'server1', 'server2'], 
                   'can_delete': [
                                'server1']}, 
       'account': {'token:*': [
                             'token1', 'token2'], 
                   'token:read': [
                                'token2', 'token3'], 
                   'token:write': [
                                 'token4']}}

    def setUp(self):
        super(TestAccountAPI, self).setUp()
        self.api = AccountAPI(base_url='http://compute.localhost', auth_token=str(uuid.uuid4()))
        self.fake_orga_key = str(uuid.uuid4())

    def make_fake_perms(self, permissions):
        if self.api.auth_token:
            self.fake_endpoint(self.api, 'tokens/%s/permissions/' % self.api.auth_token, body={'permissions': permissions})
        else:
            self.fake_endpoint(self.api, 'jwt/permissions/', body={'permissions': permissions})

    def make_fake_quotas(self, quotas):
        self.fake_endpoint(self.api, 'organizations/%s/quotas/' % self.fake_orga_key, body={'quotas': quotas})

    def test_perm_matches(self):
        self.assertTrue(self.api.perm_matches('read', 'read'))
        self.assertTrue(self.api.perm_matches(None, 'read'))
        self.assertFalse(self.api.perm_matches('write', 'read'))
        self.assertTrue(self.api.perm_matches('read', '*'))
        self.assertTrue(self.api.perm_matches('object:read', 'object:read'))
        self.assertTrue(self.api.perm_matches('object:read', 'object:*'))
        self.assertTrue(self.api.perm_matches(None, 'object:*'))
        self.assertFalse(self.api.perm_matches('object:write', 'object:read'))
        self.assertTrue(self.api.perm_matches('object:read:subperm', '*'))
        self.assertTrue(self.api.perm_matches('object:read:hello', 'object'))
        self.assertFalse(self.api.perm_matches('object', 'object:read:hello'))
        return

    def test_get_resources(self):

        def compare_results(permissions, service=None, name=None, resource=None, result=None, include_locked=False):
            """ Resets the auth API endpoint /tokens/:id/permissions, call
            get_resources and compare results with what is expected.
            """
            if result is None:
                result = []
            self.make_fake_perms(permissions)
            resources = self.api.get_resources(service=service, name=name, resource=resource, include_locked=include_locked)
            self.assertFalse(set(resources) ^ set(result))
            self.assertEqual(httpretty.last_request().querystring.get('include_locked'), [
             str(include_locked)])
            return

        compare_results({}, result=[])
        compare_results(self.fake_permissions, service='compute', name='can_boot', result=[
         'server1', 'server2'])
        compare_results(self.fake_permissions, service='compute', name='can_boot', result=[
         'server1', 'server2'])
        compare_results(self.fake_permissions, service='compute', name='can_boot', resource='server2', result=[
         'server2'])
        compare_results(self.fake_permissions, service='compute', name='can_delete', result=[
         'server1'])
        compare_results(self.fake_permissions, service='compute', name='can_delete', resource='server1', result=[
         'server1'])
        compare_results(self.fake_permissions, service='compute', name='can_write', result=[])
        compare_results(self.fake_permissions, service='compute', name='can_delete', resource='server1:*', result=[
         'server1'])
        compare_results(self.fake_permissions, service='account', name='token:read', result=[
         'token1', 'token2', 'token3'])
        compare_results(self.fake_permissions, service='account', name='token:read', resource='invalid', result=[])
        compare_results(self.fake_permissions, service='account', name='token:read', resource='token2', result=[
         'token2'])
        compare_results(self.fake_permissions, service='account', name='token:write', result=[
         'token1', 'token2', 'token4'])
        compare_results(self.fake_permissions, service='account', name='token:admin', result=[
         'token1', 'token2'])
        compare_results(self.fake_permissions, service='account', name='token:admin', result=[
         'token1', 'token2'], include_locked=True)
        self.api = AccountAPI(base_url='http://compute.localhost', auth_jwt=str(uuid.uuid4()))
        compare_results(self.fake_permissions, service='compute', name='can_boot', result=[
         'server1', 'server2'])
        return

    def test_get_resources_with_empty_token(self):
        self.api = AccountAPI()
        self.assertEqual(self.api.get_resources(), [])

    def test_get_resources_with_invalid_token(self):
        url = 'tokens/%s/permissions/' % self.api.auth_token
        self.fake_endpoint(self.api, url, status=400)
        self.assertRaises(BadToken, self.api.get_resources)
        self.fake_endpoint(self.api, url, status=404)
        self.assertRaises(BadToken, self.api.get_resources)
        self.fake_endpoint(self.api, url, status=410)
        self.assertRaises(ExpiredToken, self.api.get_resources)
        self.fake_endpoint(self.api, url, status=418)
        self.assertRaises(slumber.exceptions.SlumberHttpBaseException, self.api.get_resources)
        self.fake_endpoint(self.api, url, status=500)
        self.assertRaises(slumber.exceptions.SlumberHttpBaseException, self.api.get_resources)

    def test_has_perm(self):

        def has_perm(permissions, service=None, name=None, resource=None):
            """ Resets the auth API endpoint /tokens/:id/permissions and call
            api.has_perm.
            """
            self.make_fake_perms(permissions)
            return self.api.has_perm(service=service, name=name, resource=resource)

        self.assertTrue(has_perm(self.fake_permissions, service='compute', name='can_boot', resource='server1'))
        self.assertTrue(has_perm(self.fake_permissions, service='compute', name='can_boot', resource='server2'))
        self.assertFalse(has_perm(self.fake_permissions, service='compute', name='can_boot', resource='server3'))
        self.assertTrue(has_perm(self.fake_permissions, service='account', name='token:read', resource='token1'))
        self.assertTrue(has_perm(self.fake_permissions, service='account', name='token:write', resource='token1'))
        self.assertTrue(has_perm(self.fake_permissions, service='account', name='token:write', resource='token4'))
        self.assertFalse(has_perm(self.fake_permissions, service='account', name='token:write', resource='token3'))
        return

    def test_get_quota_403(self):
        url = 'organizations/%s/quotas/' % self.fake_orga_key
        self.fake_endpoint(self.api, url, status=403)
        self.assertRaises(slumber.exceptions.HttpClientError, self.api.get_quotas, self.fake_orga_key)

    def test_get_quotas(self):
        self.make_fake_quotas({'invites': 5})
        self.assertEqual(self.api.get_quotas(self.fake_orga_key), {'invites': 5})

    def test_get_quota(self):
        self.make_fake_quotas({'invites': 5})
        self.assertEqual(self.api.get_quota(self.fake_orga_key, 'invites'), 5)

    def test_get_quota_None(self):
        self.make_fake_quotas({'invites': 5})
        self.assertEqual(self.api.get_quota(self.fake_orga_key, 'xoxo'), None)
        return

    def test_has_quota(self):
        self.make_fake_quotas({'invites': 5})
        self.assertTrue(self.api.has_quota(self.fake_orga_key, 'invites', 2))
        self.assertFalse(self.api.has_quota(self.fake_orga_key, 'invites', 5))
        self.assertFalse(self.api.has_quota(self.fake_orga_key, 'nope'))

    def test_has_unlimited_quota(self):
        self.make_fake_quotas({'invites': -1})
        self.assertTrue(self.api.has_quota(self.fake_orga_key, 'invites', 2))
        self.assertTrue(self.api.has_quota(self.fake_orga_key, 'invites', 200))