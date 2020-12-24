# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/reviewboard/webapi/tests/test_oauth_app.py
# Compiled at: 2020-02-11 04:03:57
"""Tests for the OAuth applications web API,."""
from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.utils import six
from djblets.db.query import get_object_or_none
from djblets.testing.decorators import add_fixtures
from djblets.webapi.errors import DOES_NOT_EXIST
from djblets.webapi.testing.decorators import webapi_test_template
from reviewboard.oauth.forms import ApplicationChangeForm
from reviewboard.oauth.models import Application
from reviewboard.site.models import LocalSite
from reviewboard.webapi.resources import resources
from reviewboard.webapi.tests.base import BaseWebAPITestCase
from reviewboard.webapi.tests.mimetypes import oauth_app_item_mimetype, oauth_app_list_mimetype
from reviewboard.webapi.tests.mixins import BasicTestsMetaclass
from reviewboard.webapi.tests.mixins_extra_data import ExtraDataItemMixin, ExtraDataListMixin
from reviewboard.webapi.tests.urls import get_oauth_app_item_url, get_oauth_app_list_url

def _compare_item(self, item_rsp, app):
    self.assertEqual(item_rsp[b'authorization_grant_type'], app.authorization_grant_type)
    self.assertEqual(item_rsp[b'client_id'], app.client_id)
    self.assertEqual(item_rsp[b'client_secret'], app.client_secret)
    self.assertEqual(item_rsp[b'client_type'], app.client_type)
    self.assertEqual(item_rsp[b'id'], app.pk)
    self.assertEqual(item_rsp[b'name'], app.name)
    if app.redirect_uris:
        uris = {uri.strip() for uri in app.redirect_uris.split(b',')}
    else:
        uris = set()
    self.assertEqual(set(item_rsp[b'redirect_uris']), uris)
    self.assertEqual(item_rsp[b'skip_authorization'], app.skip_authorization)
    self.assertEqual(item_rsp[b'links'][b'user'][b'title'], app.user.username)


@six.add_metaclass(BasicTestsMetaclass)
class ResourceListTests(ExtraDataListMixin, BaseWebAPITestCase):
    """Testing the OAuthApplicationResource list APIs."""
    resource = resources.oauth_app
    sample_api_url = b'oauth-apps/'
    fixtures = [
     b'test_users']
    compare_item = _compare_item

    def setup_basic_get_test(self, user, with_local_site, local_site_name, populate_items):
        if populate_items:
            if with_local_site:
                local_site = LocalSite.objects.get(name=local_site_name)
            else:
                local_site = None
            items = [
             Application.objects.create(user=user, local_site=local_site)]
        else:
            items = []
        return (
         get_oauth_app_list_url(local_site_name=local_site_name),
         oauth_app_list_mimetype,
         items)

    @add_fixtures([b'test_site'])
    @webapi_test_template
    def test_get_filtered(self):
        """Testing the GET <URL> API only returns filtered applications"""
        admin = User.objects.get(username=b'admin')
        local_site = LocalSite.objects.get(pk=1)
        applications = set(filter(lambda a: a.local_site is None and a.user_id == self.user.pk, self._make_applications([self.user, admin], local_site)))
        rsp = self.api_get(get_oauth_app_list_url(), {}, expected_mimetype=oauth_app_list_mimetype)
        self.assertIn(b'stat', rsp)
        self.assertEqual(rsp[b'stat'], b'ok')
        self.assertEqual(applications, self._applications_from_response(rsp[b'oauth_apps']))

    @add_fixtures([b'test_site'])
    @webapi_test_template
    def test_get_filtered_with_localsite(self):
        """Testing the GET <URL> API only returns filtered applications on a
        LocalSite
        """
        admin = User.objects.get(username=b'admin')
        local_site = LocalSite.objects.get(pk=1)
        local_site.users.add(self.user)
        applications = self._make_applications(users=[
         self.user, admin], local_site=local_site, predicate=lambda a: a.local_site == local_site and a.user == self.user)
        rsp = self.api_get(get_oauth_app_list_url(local_site.name), {}, expected_mimetype=oauth_app_list_mimetype)
        self.assertIn(b'stat', rsp)
        self.assertEqual(rsp[b'stat'], b'ok')
        self.assertEqual(applications, self._applications_from_response(rsp[b'oauth_apps']))

    @add_fixtures([b'test_site'])
    @webapi_test_template
    def test_superuser_get(self):
        """Testing the GET <URL> API as a superuser"""
        self.user = self._login_user(local_site=False, admin=True)
        local_site = LocalSite.objects.get(pk=1)
        doc = User.objects.get(username=b'doc')
        applications = self._make_applications(users=[
         self.user, doc], local_site=local_site, predicate=lambda a: a.local_site is None)
        rsp = self.api_get(get_oauth_app_list_url(), {}, expected_mimetype=oauth_app_list_mimetype)
        self.assertIn(b'stat', rsp)
        self.assertEqual(rsp[b'stat'], b'ok')
        self.assertEqual(applications, self._applications_from_response(rsp[b'oauth_apps']))

    @add_fixtures([b'test_site'])
    @webapi_test_template
    def test_superuser_get_local_site(self):
        """Testing the GET <URL> API with a LocalSite as a superuser"""
        self.user = self._login_user(local_site=False, admin=True)
        local_site = LocalSite.objects.get(pk=1)
        doc = User.objects.get(username=b'doc')
        applications = self._make_applications(users=[
         self.user, doc], local_site=local_site, predicate=lambda a: a.local_site == local_site)
        rsp = self.api_get(get_oauth_app_list_url(local_site.name), {}, expected_mimetype=oauth_app_list_mimetype)
        self.assertIn(b'stat', rsp)
        self.assertEqual(rsp[b'stat'], b'ok')
        self.assertEqual(applications, self._applications_from_response(rsp[b'oauth_apps']))

    def _applications_from_response(self, item_rsps):
        """Return the Application instances for the given item responses.

        Args:
            item_rsps (list):
                The individual item responses.

        Returns:
            set of reviewboard.oauth.models.Application:
            The matching applications.
        """
        return set(Application.objects.filter(pk__in=(item[b'id'] for item in item_rsps)))

    def _make_applications(self, users, local_site, predicate=None):
        """Create some applications for testing:

        Args:
            users (list of django.contrib.auth.models.User):
                The users to create applications for.

            local_site (reviewboard.site.models.LocalSite):
                A LocalSite.

            predicate (callable, optional):
                An optional callable predicate to filter the results.

        Returns:
            set of reviewboard.oauth.models.Application:
            The created applications.
        """
        applications = set()
        applications.update(self.create_oauth_application(u, None, name=b'%s-app' % u.username) for u in users)
        applications.update(self.create_oauth_application(u, local_site, name=b'%s-site-app' % u.username) for u in users)
        if predicate:
            applications = set(filter(predicate, applications))
        return applications

    def setup_basic_post_test(self, user, with_local_site, local_site_name, post_valid_data):
        if post_valid_data:
            post_data = {b'authorization_grant_type': Application.GRANT_CLIENT_CREDENTIALS, 
               b'client_type': Application.CLIENT_PUBLIC, 
               b'name': b'test-application', 
               b'redirect_uris': b'https://example.com/oauth/'}
        else:
            post_data = {}
        return (
         get_oauth_app_list_url(local_site_name),
         oauth_app_item_mimetype,
         post_data, [])

    def check_post_result(self, user, rsp):
        app = Application.objects.get(pk=rsp[b'oauth_app'][b'id'])
        self.compare_item(rsp[b'oauth_app'], app)

    @webapi_test_template
    def test_post_grant_implicit_no_uris(self):
        """Testing the POST <URL> API with GRANT_IMPLICIT and no URIs"""
        self._test_post_redirect_uri_grant_combination(redirect_uris=b'', grant_type=Application.GRANT_IMPLICIT, is_valid=False)

    @webapi_test_template
    def test_post_grant_implicit_uris(self):
        """Testing the POST <URL> API with GRANT_IMPLICIT and URIs"""
        self._test_post_redirect_uri_grant_combination(redirect_uris=b'https://example.com/', grant_type=Application.GRANT_IMPLICIT, is_valid=True)

    @webapi_test_template
    def test_post_grant_authorization_code_no_uris(self):
        """Testing the POST <URL> API with GRANT_AUTHORIZATION_CODE and no URIs
        """
        self._test_post_redirect_uri_grant_combination(redirect_uris=b'', grant_type=Application.GRANT_AUTHORIZATION_CODE, is_valid=False)

    @webapi_test_template
    def test_post_grant_authorization_code_uris(self):
        """Testing the POST <URL> API with GRANT_AUTHORIZATION_CODE and URIs"""
        self._test_post_redirect_uri_grant_combination(redirect_uris=b'http://example.com', grant_type=Application.GRANT_AUTHORIZATION_CODE, is_valid=True)

    @webapi_test_template
    def test_post_grant_password_no_uris(self):
        """Testing the POST <URL> API with GRANT_PASSWORD and no URIs"""
        self._test_post_redirect_uri_grant_combination(redirect_uris=b'', grant_type=Application.GRANT_PASSWORD, is_valid=True)

    @webapi_test_template
    def test_post_grant_password_uris(self):
        """Testing the POST <URL> API with GRANT_PASSWORD and URIs"""
        self._test_post_redirect_uri_grant_combination(redirect_uris=b'http://example.com', grant_type=Application.GRANT_PASSWORD, is_valid=True)

    @webapi_test_template
    def test_post_grant_client_credentials_no_uris(self):
        """Testing the POST <URL> API with GRANT_CLIENT_CREDENTIALS and no URIs
        """
        self._test_post_redirect_uri_grant_combination(redirect_uris=b'', grant_type=Application.GRANT_CLIENT_CREDENTIALS, is_valid=True)

    @webapi_test_template
    def test_post_grant_client_credentials_uris(self):
        """Testing the POST <URL> API with GRANT_CLIENT_CREDENTIALS and URIs"""
        self._test_post_redirect_uri_grant_combination(redirect_uris=b'http://example.com', grant_type=Application.GRANT_CLIENT_CREDENTIALS, is_valid=True)

    @webapi_test_template
    def test_post_set_user(self):
        """Testing the POST <URL> API with user set"""
        rsp = self.api_post(get_oauth_app_list_url(), {b'authorization_grant_type': Application.GRANT_CLIENT_CREDENTIALS, 
           b'client_type': Application.CLIENT_PUBLIC, 
           b'name': b'test-application', 
           b'redirect_uris': b'https://example.com/oauth/', 
           b'user': b'doc'}, expected_status=400)
        self.assertIn(b'stat', rsp)
        self.assertEqual(rsp[b'stat'], b'fail')
        self.assertIn(b'fields', rsp)
        self.assertIn(b'user', rsp[b'fields'])
        self.assertEqual(rsp[b'fields'][b'user'], [
         b'You do not have permission to set this field.'])

    @webapi_test_template
    def test_post_set_user_as_superuser(self):
        """Testing the POST <URL> API as a superuser with user set"""
        self._login_user(admin=True)
        rsp = self.api_post(get_oauth_app_list_url(), {b'authorization_grant_type': Application.GRANT_CLIENT_CREDENTIALS, 
           b'client_type': Application.CLIENT_PUBLIC, 
           b'name': b'test-application', 
           b'redirect_uris': b'https://example.com/oauth/', 
           b'user': b'doc'}, expected_mimetype=oauth_app_item_mimetype)
        self.assertIn(b'stat', rsp)
        self.assertEqual(rsp[b'stat'], b'ok')
        app = Application.objects.get(pk=rsp[b'oauth_app'][b'id'])
        self.compare_item(rsp[b'oauth_app'], app)
        self.assertEqual(app.user.username, b'doc')

    @webapi_test_template
    def test_post_set_user_as_superuser_not_exists(self):
        """Testing the POST <URL> API as a superuser with user set as a
        non-existent user
        """
        self._login_user(admin=True)
        rsp = self.api_post(get_oauth_app_list_url(), {b'authorization_grant_type': Application.GRANT_CLIENT_CREDENTIALS, 
           b'client_type': Application.CLIENT_PUBLIC, 
           b'name': b'test-application', 
           b'redirect_uris': b'https://example.com/oauth/', 
           b'user': b'foofoo'}, expected_status=400)
        self.assertIn(b'stat', rsp)
        self.assertEqual(rsp[b'stat'], b'fail')
        self.assertIn(b'fields', rsp)
        self.assertIn(b'user', rsp[b'fields'])
        self.assertEqual(rsp[b'fields'][b'user'], [
         b'The user "foofoo" does not exist.'])

    @add_fixtures([b'test_site'])
    @webapi_test_template
    def test_post_set_user_as_local_site_admin(self):
        """Testing the POST <URL> API as a LocalSite admin with user set"""
        self._login_user(admin=True, local_site=True)
        local_site = LocalSite.objects.get(name=self.local_site_name)
        local_site.users.add(User.objects.get(username=b'dopey'))
        rsp = self.api_post(get_oauth_app_list_url(self.local_site_name), {b'authorization_grant_type': Application.GRANT_CLIENT_CREDENTIALS, 
           b'client_type': Application.CLIENT_PUBLIC, 
           b'name': b'test-application', 
           b'redirect_uris': b'https://example.com/oauth/', 
           b'user': b'dopey'}, expected_mimetype=oauth_app_item_mimetype)
        self.assertIn(b'stat', rsp)
        self.assertEqual(rsp[b'stat'], b'ok')
        app = Application.objects.get(pk=rsp[b'oauth_app'][b'id'])
        self.compare_item(rsp[b'oauth_app'], app)
        self.assertEqual(app.user.username, b'dopey')

    @add_fixtures([b'test_site'])
    @webapi_test_template
    def test_post_set_user_as_local_site_admin_with_non_local_site_user(self):
        """Testing the POST <URL> API as a LocalSite admin with user set to a
        non-LocalSite user
        """
        self._login_user(admin=True, local_site=True)
        rsp = self.api_post(get_oauth_app_list_url(self.local_site_name), {b'authorization_grant_type': Application.GRANT_CLIENT_CREDENTIALS, 
           b'client_type': Application.CLIENT_PUBLIC, 
           b'name': b'test-application', 
           b'redirect_uris': b'https://example.com/oauth/', 
           b'user': b'dopey'}, expected_status=400)
        self.assertIn(b'stat', rsp)
        self.assertEqual(rsp[b'stat'], b'fail')
        self.assertIn(b'fields', rsp)
        self.assertIn(b'user', rsp[b'fields'])
        self.assertEqual(rsp[b'fields'][b'user'], [
         b'The user "dopey" does not exist.'])

    @webapi_test_template
    def test_post_set_skip_authorization(self):
        """Testing the POST <URL> API with skip_authorization set"""
        rsp = self.api_post(get_oauth_app_list_url(), {b'authorization_grant_type': Application.GRANT_CLIENT_CREDENTIALS, 
           b'client_type': Application.CLIENT_PUBLIC, 
           b'name': b'test-application', 
           b'redirect_uris': b'https://example.com/oauth/', 
           b'skip_authorization': b'1'}, expected_status=400)
        self.assertIn(b'stat', rsp)
        self.assertEqual(rsp[b'stat'], b'fail')
        self.assertIn(b'fields', rsp)
        self.assertIn(b'skip_authorization', rsp[b'fields'])
        self.assertEqual(rsp[b'fields'][b'skip_authorization'], [
         b'You do not have permission to set this field.'])

    @webapi_test_template
    def test_post_set_skip_authorization_as_superuser(self):
        """Testing the POST <URL> API as a superuser with skip_authorization"""
        self._login_user(admin=True)
        rsp = self.api_post(get_oauth_app_list_url(), {b'authorization_grant_type': Application.GRANT_CLIENT_CREDENTIALS, 
           b'client_type': Application.CLIENT_PUBLIC, 
           b'name': b'test-application', 
           b'redirect_uris': b'https://example.com/oauth/', 
           b'skip_authorization': b'1'}, expected_mimetype=oauth_app_item_mimetype)
        self.assertIn(b'stat', rsp)
        self.assertEqual(rsp[b'stat'], b'ok')
        app = Application.objects.get(pk=rsp[b'oauth_app'][b'id'])
        self.compare_item(rsp[b'oauth_app'], app)
        self.assertEqual(app.skip_authorization, True)

    @add_fixtures([b'test_site'])
    @webapi_test_template
    def test_post_set_skip_authorization_as_local_site_admin(self):
        """Testing the POST <URL> API as a LocalSite admin with
        skip_authorization set
        """
        self._login_user(admin=True, local_site=True)
        rsp = self.api_post(get_oauth_app_list_url(self.local_site_name), {b'authorization_grant_type': Application.GRANT_CLIENT_CREDENTIALS, 
           b'client_type': Application.CLIENT_PUBLIC, 
           b'name': b'test-application', 
           b'redirect_uris': b'https://example.com/oauth/', 
           b'skip_authorization': b'1'}, expected_mimetype=oauth_app_item_mimetype)
        self.assertIn(b'stat', rsp)
        self.assertEqual(rsp[b'stat'], b'ok')
        app = Application.objects.get(pk=rsp[b'oauth_app'][b'id'])
        self.compare_item(rsp[b'oauth_app'], app)
        self.assertEqual(app.skip_authorization, True)

    def _test_post_redirect_uri_grant_combination(self, redirect_uris, grant_type, is_valid):
        """Test the redirect_uris and grant type are valid or invalid.

        Args:
            redirect_uris (unicode):
                A space-separated list of redirect URIs.

            grant_type (unicode):
                The grant type.

            is_valid (bool):
                Whether or not the given combination is valid. This determines
                the testing done on the response.
        """
        post_data = {b'authorization_grant_type': grant_type, 
           b'client_type': Application.CLIENT_PUBLIC, 
           b'name': b'test-app', 
           b'redirect_uris': redirect_uris, 
           b'skip_authorization': b'0'}
        if is_valid:
            rsp = self.api_post(get_oauth_app_list_url(), post_data, expected_mimetype=oauth_app_item_mimetype)
            self.assertIn(b'stat', rsp)
            self.assertEqual(rsp[b'stat'], b'ok')
            self.compare_item(rsp[b'oauth_app'], Application.objects.get(name=b'test-app'))
        else:
            rsp = self.api_post(get_oauth_app_list_url(), post_data, expected_status=400)
            self.assertIn(b'stat', rsp)
            self.assertEqual(rsp[b'stat'], b'fail')
            self.assertIn(b'err', rsp)
            self.assertIn(b'fields', rsp)
            self.assertIn(b'redirect_uris', rsp[b'fields'])


@six.add_metaclass(BasicTestsMetaclass)
class ResourceItemTests(ExtraDataItemMixin, BaseWebAPITestCase):
    """Testing the OAuthApplicationResource item APIs."""
    resource = resources.oauth_app
    sample_api_url = b'oauth-apps/<app-id>/'
    fixtures = [b'test_users']
    not_owner_status_code = 404
    not_owner_error = DOES_NOT_EXIST
    compare_item = _compare_item

    def setup_basic_get_test(self, user, with_local_site, local_site_name):
        app = self.create_oauth_application(user, with_local_site=with_local_site)
        return (
         get_oauth_app_item_url(app.pk, local_site_name),
         oauth_app_item_mimetype,
         app)

    @webapi_test_template
    def test_get_without_owner(self):
        """Testing the GET <URL> API without owner"""
        app = self.create_oauth_application(User.objects.get(username=b'admin'))
        self.api_get(get_oauth_app_item_url(app.pk), expected_status=404)

    @webapi_test_template
    def test_get_without_owner_as_superuser(self):
        """Testing the GET <URL> API without owner as superuser"""
        self.user = self._login_user(admin=True)
        app = self.create_oauth_application(User.objects.get(username=b'doc'))
        rsp = self.api_get(get_oauth_app_item_url(app.pk), expected_mimetype=oauth_app_item_mimetype)
        self.assertIn(b'stat', rsp)
        self.assertEqual(rsp[b'stat'], b'ok')
        self.assertIn(b'oauth_app', rsp)
        self.compare_item(rsp[b'oauth_app'], app)

    @add_fixtures([b'test_site'])
    @webapi_test_template
    def test_get_without_local_site(self):
        """Testing the GET <URL> API for an app related to a LocalSite"""
        local_site = LocalSite.objects.get(pk=1)
        local_site.users.add(self.user)
        app = self.create_oauth_application(self.user, local_site=LocalSite.objects.get(pk=1))
        rsp = self.api_get(get_oauth_app_item_url(app.pk), expected_status=404)
        self.assertIn(b'stat', rsp)
        self.assertEqual(rsp[b'stat'], b'fail')

    @add_fixtures([b'test_site'])
    @webapi_test_template
    def test_get_with_invalid_local_site(self):
        """Testing the GET <URL> API with an app related to a LocalSite not
        using the LocalSite's API
        """
        local_site = LocalSite.objects.get(pk=1)
        local_site.users.add(self.user)
        app = self.create_oauth_application(self.user)
        rsp = self.api_get(get_oauth_app_item_url(app.pk, local_site.name), expected_status=404)
        self.assertIn(b'stat', rsp)
        self.assertEqual(rsp[b'stat'], b'fail')

    @add_fixtures([b'test_site'])
    @webapi_test_template
    def test_get_without_owner_as_local_site_admin(self):
        """Testing the GET <URL> API without owner on a LocalSite as a
        LocalSite admin
        """
        local_site = LocalSite.objects.get(pk=1)
        local_site.users.add(self.user)
        app = self.create_oauth_application(self.user, local_site=local_site)
        self.user = self._login_user(admin=True, local_site=True)
        rsp = self.api_get(get_oauth_app_item_url(app.pk, local_site.name), expected_mimetype=oauth_app_item_mimetype)
        self.assertIn(b'stat', rsp)
        self.assertEqual(rsp[b'stat'], b'ok')
        self.assertIn(b'oauth_app', rsp)
        self.compare_item(rsp[b'oauth_app'], app)

    def setup_basic_put_test(self, user, with_local_site, local_site_name, put_valid_data):
        app = self.create_oauth_application(user, with_local_site=with_local_site)
        if put_valid_data:
            request_data = {b'extra_data.fake_key': b''}
        else:
            request_data = {b'user': b'admin'}
        return (
         get_oauth_app_item_url(app.pk, local_site_name),
         oauth_app_item_mimetype,
         request_data,
         app, [])

    def check_put_result(self, user, item_rsp, app):
        app = Application.objects.get(pk=app.pk)
        self.compare_item(item_rsp, app)

    @add_fixtures([b'test_site'])
    @webapi_test_template
    def test_put_re_enable_security_disabled(self):
        """Testing the PUT <URL> API with enabled=1 for an application disabled
        due to security
        """
        self.user = self._login_user(admin=True)
        doc = User.objects.get(username=b'doc')
        local_site = LocalSite.objects.get(pk=1)
        app = self.create_oauth_application(user=doc, local_site=local_site)
        original_secret = app.client_secret
        local_site.users.remove(doc)
        app = Application.objects.get(pk=app.pk)
        self.assertTrue(app.is_disabled_for_security)
        self.assertEqual(app.user, self.user)
        self.assertEqual(app.original_user, doc)
        rsp = self.api_put(get_oauth_app_item_url(app.pk, local_site.name), {b'enabled': b'1'}, expected_status=400)
        app = Application.objects.get(pk=app.pk)
        self.assertIn(b'stat', rsp)
        self.assertEqual(rsp[b'stat'], b'fail')
        self.assertIn(b'fields', rsp)
        self.assertIn(b'__all__', rsp[b'fields'])
        self.assertEqual(rsp[b'fields'][b'__all__'][0], ApplicationChangeForm.DISABLED_FOR_SECURITY_ERROR)
        self.assertEqual(app.original_user, doc)
        self.assertEqual(app.client_secret, original_secret)

    @webapi_test_template
    def test_put_regenerate_secret_key(self):
        """Testing the PUT <URL> API with regenerate_client_secret=1"""
        app = self.create_oauth_application(user=self.user)
        original_secret = app.client_secret
        rsp = self.api_put(get_oauth_app_item_url(app.pk), {b'regenerate_client_secret': 1}, expected_mimetype=oauth_app_item_mimetype)
        app = Application.objects.get(pk=app.pk)
        self.assertIn(b'stat', rsp)
        self.assertEqual(rsp[b'stat'], b'ok')
        self.compare_item(rsp[b'oauth_app'], app)
        self.assertNotEqual(app.client_secret, original_secret)

    @add_fixtures([b'test_site'])
    @webapi_test_template
    def test_put_regenerate_secret_key_enable(self):
        """Testing the PUT <URL> API with regenerate_secret_key=1 and enabled=1
        """
        self.user = self._login_user(admin=True)
        doc = User.objects.get(username=b'doc')
        local_site = LocalSite.objects.get(pk=1)
        app = self.create_oauth_application(user=doc, local_site=local_site)
        original_secret = app.client_secret
        local_site.users.remove(doc)
        app = Application.objects.get(pk=app.pk)
        self.assertTrue(app.is_disabled_for_security)
        self.assertEqual(app.user, self.user)
        self.assertEqual(app.original_user, doc)
        rsp = self.api_put(get_oauth_app_item_url(app.pk, local_site.name), {b'enabled': b'1', 
           b'regenerate_client_secret': b'1'}, expected_mimetype=oauth_app_item_mimetype)
        app = Application.objects.get(pk=app.pk)
        self.assertIn(b'stat', rsp)
        self.assertEqual(rsp[b'stat'], b'ok')
        item_rsp = rsp[b'oauth_app']
        self.compare_item(item_rsp, app)
        self.assertNotEqual(item_rsp[b'client_secret'], original_secret)
        self.assertFalse(app.is_disabled_for_security)
        self.assertIsNone(app.original_user)
        self.assertTrue(app.enabled)
        self.assertNotEqual(app.client_secret, original_secret)

    def setup_basic_delete_test(self, user, with_local_site, local_site_name):
        app = self.create_oauth_application(user=user, with_local_site=with_local_site)
        return (
         get_oauth_app_item_url(app.pk, local_site_name),
         [
          app.pk])

    def check_delete_result(self, user, app_pk):
        self.assertIsNone(get_object_or_none(Application, pk=app_pk))