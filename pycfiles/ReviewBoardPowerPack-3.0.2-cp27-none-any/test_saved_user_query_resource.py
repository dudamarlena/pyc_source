# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /rbpowerpack/reports/tests/test_saved_user_query_resource.py
# Compiled at: 2019-06-17 15:11:31
from __future__ import unicode_literals
from beanbag_licensing.tests.testcases import LicensedExtensionTestCase
from django.contrib.auth.models import User
from django.utils import six
from djblets.webapi.errors import DUPLICATE_ITEM
from djblets.webapi.testing.decorators import webapi_test_template
from reviewboard.site.models import LocalSite
from reviewboard.webapi.tests.base import BaseWebAPITestCase
from reviewboard.webapi.tests.mimetypes import _build_mimetype
from reviewboard.webapi.tests.mixins import BasicTestsMetaclass
from rbpowerpack.extension import PowerPackExtension
from rbpowerpack.reports.queries import UserQuery
from rbpowerpack.reports.resources import saved_user_query_resource
saved_user_query_list_mimetype = _build_mimetype(b'saved-user-queries')
saved_user_query_item_mimetype = _build_mimetype(b'saved-user-query')

def get_list_url(local_site_name=None):
    """Return the list URL for the saved user query resource."""
    return saved_user_query_resource.get_list_url(local_site_name=local_site_name)


def get_item_url(name, local_site_name=None):
    """Return the item URL for the saved user query resource."""
    return saved_user_query_resource.get_item_url(local_site_name=local_site_name, query_name=name)


@six.add_metaclass(BasicTestsMetaclass)
class ResourceListTests(LicensedExtensionTestCase, BaseWebAPITestCase):
    """Tests for the SavedUserQuery list API."""
    fixtures = [
     b'test_users']
    resource = saved_user_query_resource
    extension_class = PowerPackExtension
    sample_api_url = b'saved-user-queries/'

    def setup_basic_get_test(self, user, with_local_site, local_site_name, populate_items):
        """Set up the basic data for HTTP GET tests.

        Args:
            user (django.contrib.auth.models.User):
                The user making the request.

            with_local_site (bool):
                Whether the items should be associated with a LocalSite.

            local_site_name (unicode):
                The name of the LocalSite (if appropriate).

            populate_items (bool):
                Whether items should actually be created.

        Returns:
            tuple:
            A 3-tuple, containing the URL to GET, the expected mime type, and a
            list of the expected items.
        """
        items = []
        if populate_items:
            local_site = None
            if with_local_site:
                local_site = LocalSite.objects.get(name=local_site_name)
            group = self.create_review_group(local_site=local_site)
            query = UserQuery(name=b'My saved query', user=user, local_site=local_site, usernames=[
             b'doc', b'grumpy'], group_names=[
             group.name])
            query.save()
            items.append(query)
        return (get_list_url(local_site_name=local_site_name),
         saved_user_query_list_mimetype,
         items)

    def compare_item(self, item_rsp, query):
        """Assert that the GET request worked as expected.

        Args:
            item_rsp (dict):
                The response content from the API.

            query (rbpowerpack.reports.queries.UserQuery):
                The original query object.
        """
        self.assertEqual(item_rsp, query.to_json())

    def setup_basic_post_test(self, user, with_local_site, local_site_name, post_valid_data):
        """Set up the basic data for HTTP POST tests.

        Args:
            user (django.contrib.auth.models.User):
                The user doing the POST.

            with_local_site (bool):
                Whether the created items should be associated with a
                LocalSite.

            local_site_name (unicode):
                The name of the LocalSite (if appropriate).

            post_valid_data (bool):
                Whether the returned data should include a valid POST payload.

        Returns:
            tuple:
            A 4-tuple, containing the URL to POST, the expected mime type, a
            dict of the data to post, and any additional arguments to plumb
            through into :py:meth:`check_post_result`.
        """
        if post_valid_data:
            group = self.create_review_group(with_local_site=with_local_site)
            post_data = {b'name': b'My saved query', 
               b'usernames': (b',').join([b'doc', b'grumpy']), 
               b'group_names': (b',').join([group.name])}
        else:
            post_data = {}
        return (
         get_list_url(local_site_name=local_site_name),
         saved_user_query_item_mimetype,
         post_data,
         [
          local_site_name])

    def check_post_result(self, user, rsp, local_site_name):
        """Assert that the POST request worked as expected.

        Args:
            user (django.contrib.auth.models.User):
                The user who made the request.

            rsp (dict):
                The API response.

            local_site_name (unicode):
                The name of the LocalSite (if appropriate).
        """
        self.assertEqual(rsp[b'stat'], b'ok')
        local_site = None
        if local_site_name:
            local_site = LocalSite.objects.get(name=local_site_name)
        query = UserQuery.from_profile(user, local_site, rsp[b'saved_user_query'][b'name'])
        self.assertIsNotNone(query)
        self.assertEqual(rsp[b'saved_user_query'], query.to_json())
        return

    @webapi_test_template
    def test_post_with_conflict(self):
        """Testing the POST <URL> API with a duplicate name"""
        query = UserQuery(name=b'My saved query', user=self.user, usernames=[
         b'doc', b'grumpy'])
        query.save()
        rsp = self.api_post(get_list_url(), {b'name': b'My saved query', 
           b'usernames': b'doc', 
           b'group_names': b''}, expected_status=409)
        self.assertEqual(rsp[b'stat'], b'fail')
        self.assertEqual(rsp[b'err'][b'code'], DUPLICATE_ITEM.code)


@six.add_metaclass(BasicTestsMetaclass)
class ResourceItemTests(LicensedExtensionTestCase, BaseWebAPITestCase):
    """Tests for the SavedUserQuery item API."""
    fixtures = [
     b'test_users']
    resource = saved_user_query_resource
    test_http_methods = ('DELETE', 'GET', 'PUT')
    extension_class = PowerPackExtension
    sample_api_url = b'saved-user-queries/<name>/'

    def setup_basic_delete_test(self, user, with_local_site, local_site_name):
        """Set up the basic data for HTTP DELETE tests.

        Args:
            user (django.contrib.auth.models.User):
                The user making the request.

            with_local_site (bool):
                Whether the items should be associated with a LocalSite.

            local_site_name (unicode):
                The name of the LocalSite (if appropriate).

        Returns:
            tuple:
            A 2-tuple, containing the URL to DELETE and any extra arguments to
            be passed to check_delete_result.
        """
        local_site = None
        if with_local_site:
            local_site = LocalSite.objects.get(name=local_site_name)
        name = b'My saved query'
        query = UserQuery(name=name, user=user, local_site=local_site, usernames=[
         b'doc', b'grumpy'])
        query.save()
        return (
         get_item_url(name, local_site_name=local_site_name),
         [
          name, local_site_name])

    def check_delete_result(self, user, name, local_site_name):
        """Assert that the DELETE request worked as expected."""
        local_site = None
        if local_site_name:
            local_site = LocalSite.objects.get(name=local_site_name)
        with self.assertRaises(KeyError):
            UserQuery.from_profile(user, local_site, name)
        return

    @webapi_test_template
    def test_delete_not_owner(self):
        """Testing the DELETE <URL> API without owner"""
        self.load_fixtures(self.basic_delete_fixtures)
        user = User.objects.get(username=b'doc')
        self.assertNotEqual(user, self.user)
        url, cb_args = self.setup_basic_delete_test(user, False, None)
        self.assertFalse(url.startswith(b'/s/' + self.local_site_name))
        self.api_delete(url, expected_status=404)
        return

    def setup_basic_get_test(self, user, with_local_site, local_site_name):
        """Set up the basic data for HTTP GET tests.

        Args:
            user (django.contrib.auth.models.User):
                The user making the request.

            with_local_site (bool):
                Whether the items should be associated with a LocalSite.

            local_site_name (unicode):
                The name of the LocalSite (if appropriate).

            populate_items (bool):
                Whether items should actually be created.

        Returns:
            tuple:
            A 3-tuple, containing the URL to GET, the expected mime type, and
            the expected item.
        """
        local_site = None
        if with_local_site:
            local_site = LocalSite.objects.get(name=self.local_site_name)
        name = b'saved-query'
        query = UserQuery(name=name, user=user, local_site=local_site, usernames=[
         b'doc', b'dopey'])
        query.save()
        return (
         get_item_url(name, local_site_name=local_site_name),
         saved_user_query_item_mimetype,
         query)

    def compare_item(self, item_rsp, query):
        """Assert that the GET request worked as expected.

        Args:
            item_rsp (dict):
                The response content from the API.

            query (rbpowerpack.reports.queries.UserQuery):
                The original query object.
        """
        self.assertEqual(item_rsp, query.to_json())

    def setup_basic_put_test(self, user, with_local_site, local_site_name, put_valid_data):
        """Set up the basic data for HTTP PUT tests.

        Args:
            user (django.contrib.auth.models.User):
                The user making the request.

            with_local_site (bool):
                Whether the items should be associated with a LocalSite.

            local_site_name (unicode):
                The name of the LocalSite (if appropriate).

            put_valid_data (bool):
                Whether this should return valid data for the PUT API.

        Returns:
            tuple:
            A 4-tuple, containing the API to PUT, the expected mime type, the
            data to PUT, and a list of extra arguments to pass to
            check_put_result.
        """
        local_site = None
        if with_local_site:
            local_site = LocalSite.objects.get(name=self.local_site_name)
        old_name = b'saved-query'
        new_name = b'new-saved-query'
        query = UserQuery(name=old_name, user=user, local_site=local_site, usernames=[
         b'doc', b'dopey'])
        query.save()
        return (
         get_item_url(old_name, local_site_name=local_site_name),
         saved_user_query_item_mimetype,
         {b'name': new_name, 
            b'usernames': b'grumpy'},
         query,
         [
          local_site, new_name, old_name])

    def check_put_result(self, user, item_rsp, query, local_site, new_name, old_name):
        """Assert that the PUT request worked as expected.

        Args:
            user (django.contrib.auth.models.User):
                The user who made the request.

            item_rsp (dict):
                The response content from the API.

            query (rbpowerpack.reports.queries.UserQuery):
                The original query object.

            local_site (reviewboard.site.models.LocalSite):
                The LocalSite object, if present.

            new_name (unicode):
                The new name of the saved query.

            old_name (unicode):
                The old name of the saved query.
        """
        with self.assertRaises(KeyError):
            UserQuery.from_profile(user, local_site, old_name)
        query = UserQuery.from_profile(user, local_site, new_name)
        self.assertEqual(item_rsp, query.to_json())

    @webapi_test_template
    def test_put_not_owner(self):
        """Testing the PUT <URL> API without owner"""
        self.load_fixtures(self.basic_put_fixtures)
        user = User.objects.get(username=b'doc')
        self.assertNotEqual(user, self.user)
        url, mimetype, put_data, item, cb_args = self.setup_basic_put_test(user, False, None, False)
        self.assertFalse(url.startswith(b'/s/' + self.local_site_name))
        self.api_put(url, put_data, expected_status=404)
        return