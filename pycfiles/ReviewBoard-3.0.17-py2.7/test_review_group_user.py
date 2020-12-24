# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/reviewboard/webapi/tests/test_review_group_user.py
# Compiled at: 2020-02-11 04:03:57
from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.utils import six
from djblets.testing.decorators import add_fixtures
from djblets.webapi.errors import PERMISSION_DENIED
from djblets.webapi.testing.decorators import webapi_test_template
from reviewboard.webapi.resources import resources
from reviewboard.webapi.errors import INVALID_USER
from reviewboard.webapi.tests.base import BaseWebAPITestCase
from reviewboard.webapi.tests.mimetypes import review_group_user_item_mimetype, review_group_user_list_mimetype
from reviewboard.webapi.tests.mixins import BasicTestsMetaclass
from reviewboard.webapi.tests.urls import get_review_group_user_item_url, get_review_group_user_list_url, get_user_item_url

@six.add_metaclass(BasicTestsMetaclass)
class ResourceListTests(BaseWebAPITestCase):
    """Testing the ReviewGroupUserResource list API tests."""
    fixtures = [
     b'test_users']
    sample_api_url = b'groups/<name>/users/'
    resource = resources.review_group_user
    basic_post_use_admin = True

    def compare_item(self, item_rsp, user):
        self.assertEqual(item_rsp[b'id'], user.pk)
        self.assertEqual(item_rsp[b'username'], user.username)
        self.assertEqual(item_rsp[b'first_name'], user.first_name)
        self.assertEqual(item_rsp[b'last_name'], user.last_name)

    def setup_basic_get_test(self, user, with_local_site, local_site_name, populate_items):
        group = self.create_review_group(with_local_site=with_local_site)
        if populate_items:
            items = [User.objects.get(username=b'doc'),
             User.objects.get(username=b'grumpy')]
            group.users = items
        else:
            items = []
        return (
         get_review_group_user_list_url(group.name, local_site_name),
         review_group_user_list_mimetype,
         items)

    @webapi_test_template
    def test_get_with_no_access(self):
        """Testing the GET <URL> API  without access to invite-only group"""
        group = self.create_review_group(name=b'priv-group', invite_only=True)
        rsp = self.api_get(get_review_group_user_list_url(group.name), expected_status=403)
        self.assertEqual(rsp[b'stat'], b'fail')
        self.assertEqual(rsp[b'err'][b'code'], PERMISSION_DENIED.code)

    @webapi_test_template
    def test_get_multiple_groups(self):
        """Testing GET <URL> API with a user in multiple groups"""
        doc = User.objects.get(username=b'doc')
        groups = [
         self.create_review_group(b'group1'),
         self.create_review_group(b'group2')]
        for group in groups:
            group.users.add(doc)

        rsp = self.api_get(get_review_group_user_list_url(groups[0].name), expected_mimetype=review_group_user_list_mimetype)
        self.assertEqual(rsp[b'stat'], b'ok')
        self.assertEqual(rsp[b'total_results'], 1)
        self.compare_item(rsp[b'users'][0], doc)

    def setup_basic_post_test(self, user, with_local_site, local_site_name, post_valid_data):
        group = self.create_review_group(with_local_site=with_local_site)
        if post_valid_data:
            post_data = {b'username': b'doc'}
        else:
            post_data = {}
        return (
         get_review_group_user_list_url(group.name, local_site_name),
         review_group_user_item_mimetype,
         post_data,
         [
          group])

    def check_post_result(self, user, rsp, group):
        users = list(group.users.all())
        self.assertEqual(len(users), 1)
        self.assertEqual(users[0].username, b'doc')
        self.compare_item(rsp[b'user'], users[0])

    @webapi_test_template
    def test_post_with_no_access(self, local_site=None):
        """Testing the POST <URL> API with Permission Denied"""
        group = self.create_review_group()
        user = User.objects.get(pk=1)
        rsp = self.api_post(get_review_group_user_list_url(group.name, local_site), {b'username': user.username}, expected_status=403)
        self.assertEqual(rsp[b'stat'], b'fail')

    @webapi_test_template
    def test_post_with_invalid_user(self):
        """Testing the POST <URL> API with invalid user"""
        self._login_user(admin=True)
        group = self.create_review_group()
        rsp = self.api_post(get_review_group_user_list_url(group.name), {b'username': b'grabl'}, expected_status=400)
        self.assertEqual(rsp[b'stat'], b'fail')
        self.assertEqual(rsp[b'err'][b'code'], INVALID_USER.code)
        self.assertEqual(group.users.count(), 0)

    @webapi_test_template
    def test_post_with_self(self):
        """Testing the POST <URL> API with the requesting user"""
        group = self.create_review_group()
        self.assertFalse(self.user.is_superuser)
        rsp = self.api_post(get_review_group_user_list_url(group.name), {b'username': self.user.username}, expected_mimetype=review_group_user_item_mimetype)
        self.assertEqual(rsp[b'stat'], b'ok')
        self.assertEqual(group.users.count(), 1)

    @webapi_test_template
    def test_post_with_self_and_private_group(self):
        """Testing the POST <URL> API with the requesting user and private
        group
        """
        group = self.create_review_group(invite_only=True)
        self.assertFalse(group.is_accessible_by(self.user))
        rsp = self.api_post(get_review_group_user_list_url(group.name), {b'username': self.user.username}, expected_status=403)
        self.assertEqual(rsp[b'stat'], b'fail')
        self.assertEqual(group.users.count(), 0)

    @add_fixtures([b'test_site'])
    @webapi_test_template
    def test_post_with_self_and_site(self):
        """Testing the POST <URL> API with the requesting user on a local site
        """
        self.assertFalse(self.user.is_superuser)
        local_site = self.get_local_site(name=self.local_site_name)
        local_site.users.add(self.user)
        group = self.create_review_group(with_local_site=True)
        self.assertEqual(group.users.count(), 0)
        rsp = self.api_post(get_review_group_user_list_url(group.name, self.local_site_name), {b'username': self.user.username}, expected_mimetype=review_group_user_item_mimetype)
        self.assertEqual(rsp[b'stat'], b'ok')
        self.assertEqual(group.users.count(), 1)

    @add_fixtures([b'test_site'])
    @webapi_test_template
    def test_post_with_self_and_unjoined_site(self):
        """Testing the POST <URL> API with the requesting user on an unjoined
        local site
        """
        self.assertFalse(self.user.is_superuser)
        group = self.create_review_group(with_local_site=True)
        self.assertEqual(group.users.count(), 0)
        rsp = self.api_post(get_review_group_user_list_url(group.name, self.local_site_name), {b'username': self.user.username}, expected_status=403)
        self.assertEqual(rsp[b'stat'], b'fail')
        self.assertEqual(group.users.count(), 0)


@six.add_metaclass(BasicTestsMetaclass)
class ResourceItemTests(BaseWebAPITestCase):
    """Testing the ReviewGroupUserResource item API tests."""
    fixtures = [
     b'test_users']
    sample_api_url = b'groups/<name>/users/<username>/'
    resource = resources.review_group_user
    basic_delete_use_admin = True
    basic_put_use_admin = True

    def setup_http_not_allowed_item_test(self, user):
        return get_review_group_user_list_url(b'my-group')

    def compare_item(self, item_rsp, user):
        self.assertEqual(item_rsp[b'id'], user.pk)
        self.assertEqual(item_rsp[b'username'], user.username)
        self.assertEqual(item_rsp[b'first_name'], user.first_name)
        self.assertEqual(item_rsp[b'last_name'], user.last_name)

    def setup_basic_delete_test(self, user, with_local_site, local_site_name):
        group = self.create_review_group(with_local_site=with_local_site)
        doc = User.objects.get(username=b'doc')
        group.users.add(doc)
        return (
         get_review_group_user_item_url(group.name, doc.username, local_site_name),
         [
          group, doc])

    def check_delete_result(self, user, group, doc):
        self.assertNotIn(doc, group.users.all())

    @webapi_test_template
    def test_delete_with_self(self):
        """Testing the DELETE <URL> API with the requesting user
        """
        group = self.create_review_group()
        group.users.add(self.user)
        self.assertFalse(self.user.is_superuser)
        self.api_delete(get_review_group_user_item_url(group.name, self.user.username))
        self.assertEqual(group.users.count(), 0)

    @add_fixtures([b'test_site'])
    @webapi_test_template
    def test_delete_with_self_with_site(self):
        """Testing the DELETE <URL> API with the requesting user on local site
        """
        self.assertFalse(self.user.is_superuser)
        local_site = self.get_local_site(name=self.local_site_name)
        local_site.users.add(self.user)
        group = self.create_review_group(with_local_site=True)
        group.users.add(self.user)
        self.assertEqual(group.users.count(), 1)
        self.api_delete(get_review_group_user_item_url(group.name, self.user.username, self.local_site_name))
        self.assertEqual(group.users.count(), 0)

    def setup_basic_get_test(self, user, with_local_site, local_site_name):
        group = self.create_review_group(with_local_site=with_local_site)
        doc = User.objects.get(username=b'doc')
        group.users.add(doc)
        return (
         get_review_group_user_item_url(group.name, doc.username, local_site_name),
         review_group_user_item_mimetype,
         doc)

    @webapi_test_template
    def test_get_delete_link(self):
        """Testing GET <URL> API contains the correct DELETE link"""
        doc = User.objects.get(username=b'doc')
        group = self.create_review_group()
        group.users.add(doc)
        rsp = self.api_get(get_review_group_user_item_url(group.name, doc.username), expected_mimetype=review_group_user_item_mimetype)
        delete_href = rsp[b'user'][b'links'][b'delete'][b'href'][len(self.base_url):]
        self.assertEqual(delete_href, get_review_group_user_item_url(group.name, doc.username))
        self.assertNotEqual(delete_href, get_user_item_url(doc.username))

    @add_fixtures([b'test_site'])
    @webapi_test_template
    def test_get_delete_link_local_site(self):
        """Testing GET <URL> API contains the correct DELETE link with a local
        site
        """
        doc = User.objects.get(username=b'doc')
        local_site = self.get_local_site(name=self.local_site_name)
        local_site.users.add(self.user)
        local_site.users.add(doc)
        group = self.create_review_group(local_site=local_site)
        group.users.add(doc)
        rsp = self.api_get(get_review_group_user_item_url(group.name, doc.username, local_site.name), expected_mimetype=review_group_user_item_mimetype)
        delete_href = rsp[b'user'][b'links'][b'delete'][b'href'][len(self.base_url):]
        self.assertEqual(delete_href, get_review_group_user_item_url(group.name, doc.username, local_site.name))
        self.assertNotEqual(delete_href, get_user_item_url(doc.username, local_site.name))