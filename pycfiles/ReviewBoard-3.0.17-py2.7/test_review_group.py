# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/reviewboard/webapi/tests/test_review_group.py
# Compiled at: 2020-02-11 04:03:57
from __future__ import unicode_literals
from django.utils import six
from djblets.db.query import get_object_or_none
from djblets.testing.decorators import add_fixtures
from djblets.webapi.errors import PERMISSION_DENIED
from reviewboard.reviews.models import Group, ReviewRequest
from reviewboard.site.models import LocalSite
from reviewboard.webapi.resources import resources
from reviewboard.webapi.errors import GROUP_ALREADY_EXISTS
from reviewboard.webapi.tests.base import BaseWebAPITestCase
from reviewboard.webapi.tests.mimetypes import review_group_item_mimetype, review_group_list_mimetype
from reviewboard.webapi.tests.mixins import BasicTestsMetaclass
from reviewboard.webapi.tests.mixins_extra_data import ExtraDataItemMixin, ExtraDataListMixin
from reviewboard.webapi.tests.urls import get_review_group_item_url, get_review_group_list_url

@six.add_metaclass(BasicTestsMetaclass)
class ResourceListTests(ExtraDataListMixin, BaseWebAPITestCase):
    """Testing the ReviewGroupResource list APIs."""
    fixtures = [
     b'test_users']
    sample_api_url = b'groups/'
    resource = resources.review_group
    basic_post_use_admin = True

    def compare_item(self, item_rsp, group):
        self.assertEqual(item_rsp[b'id'], group.pk)
        self.assertEqual(item_rsp[b'name'], group.name)
        self.assertEqual(item_rsp[b'display_name'], group.display_name)
        self.assertEqual(item_rsp[b'mailing_list'], group.mailing_list)
        self.assertEqual(item_rsp[b'visible'], group.visible)
        self.assertEqual(item_rsp[b'invite_only'], group.invite_only)
        self.assertEqual(item_rsp[b'extra_data'], group.extra_data)
        self.assertEqual(item_rsp[b'absolute_url'], self.base_url + group.get_absolute_url())

    def setup_basic_get_test(self, user, with_local_site, local_site_name, populate_items):
        if populate_items:
            if with_local_site:
                local_site = LocalSite.objects.get(name=local_site_name)
                items = [
                 self.create_review_group(name=b'group1', local_site=local_site)]
                self.create_review_group(name=b'group2')
            else:
                local_site = LocalSite.objects.get_or_create(name=self.local_site_name)[0]
                items = [
                 self.create_review_group(name=b'group1')]
                self.create_review_group(name=b'group2', local_site=local_site)
        else:
            items = []
        return (
         get_review_group_list_url(local_site_name),
         review_group_list_mimetype,
         items)

    def test_get_with_q(self):
        """Testing the GET groups/?q= API"""
        self.create_review_group(name=b'docgroup')
        self.create_review_group(name=b'devgroup')
        rsp = self.api_get(get_review_group_list_url(), {b'q': b'dev'}, expected_mimetype=review_group_list_mimetype)
        self.assertEqual(rsp[b'stat'], b'ok')
        self.assertEqual(len(rsp[b'groups']), 1)

    def setup_basic_post_test(self, user, with_local_site, local_site_name, post_valid_data):
        if post_valid_data:
            post_data = {b'name': b'my-group', b'display_name': b'My Group', 
               b'mailing_list': b'mygroup@example.com', 
               b'visible': False, 
               b'invite_only': True}
        else:
            post_data = {}
        return (
         get_review_group_list_url(local_site_name),
         review_group_item_mimetype,
         post_data, [])

    def check_post_result(self, user, rsp):
        group = Group.objects.get(pk=rsp[b'group'][b'id'])
        self.compare_item(rsp[b'group'], group)

    def test_post_with_defaults(self):
        """Testing the POST groups/ API with field defaults"""
        name = b'my-group'
        display_name = b'My Group'
        self._login_user(admin=True)
        rsp = self.api_post(get_review_group_list_url(), {b'name': name, 
           b'display_name': display_name}, expected_mimetype=review_group_item_mimetype)
        self.assertEqual(rsp[b'stat'], b'ok')
        group = Group.objects.get(pk=rsp[b'group'][b'id'])
        self.assertEqual(group.mailing_list, b'')
        self.assertEqual(group.visible, True)
        self.assertEqual(group.invite_only, False)

    @add_fixtures([b'test_site'])
    def test_post_with_site_admin(self):
        """Testing the POST groups/ API with a local site admin"""
        self._login_user(local_site=True, admin=True)
        local_site = self.get_local_site(name=self.local_site_name)
        rsp = self.api_post(get_review_group_list_url(local_site), {b'name': b'mygroup', 
           b'display_name': b'My Group', 
           b'mailing_list': b'mygroup@example.com'}, expected_mimetype=review_group_item_mimetype)
        self.assertEqual(rsp[b'stat'], b'ok')

    def test_post_with_conflict(self):
        """Testing the POST groups/ API with Group Already Exists error"""
        self._login_user(admin=True)
        group = self.create_review_group()
        rsp = self.api_post(get_review_group_list_url(), {b'name': group.name, 
           b'display_name': b'My Group'}, expected_status=409)
        self.assertEqual(rsp[b'stat'], b'fail')
        self.assertEqual(rsp[b'err'][b'code'], GROUP_ALREADY_EXISTS.code)


@six.add_metaclass(BasicTestsMetaclass)
class ResourceItemTests(ExtraDataItemMixin, BaseWebAPITestCase):
    """Testing the ReviewGroupResource item APIs."""
    fixtures = [
     b'test_users']
    sample_api_url = b'groups/<id>/'
    resource = resources.review_group
    basic_delete_use_admin = True
    basic_put_use_admin = True

    def compare_item(self, item_rsp, group):
        self.assertEqual(item_rsp[b'id'], group.pk)
        self.assertEqual(item_rsp[b'name'], group.name)
        self.assertEqual(item_rsp[b'display_name'], group.display_name)
        self.assertEqual(item_rsp[b'mailing_list'], group.mailing_list)
        self.assertEqual(item_rsp[b'visible'], group.visible)
        self.assertEqual(item_rsp[b'invite_only'], group.invite_only)
        self.assertEqual(item_rsp[b'extra_data'], group.extra_data)

    def setup_basic_delete_test(self, user, with_local_site, local_site_name):
        group = self.create_review_group(with_local_site=with_local_site)
        return (
         get_review_group_item_url(group.name, local_site_name),
         [
          group.name])

    def check_delete_result(self, user, group_name):
        self.assertIsNone(get_object_or_none(Group, name=group_name))

    def test_delete_with_permission_denied_error(self):
        """Testing the DELETE groups/<id>/ API with Permission Denied error"""
        group = Group.objects.create(name=b'test-group', invite_only=True)
        group.users.add(self.user)
        self.api_delete(get_review_group_item_url(b'test-group'), expected_status=403)

    @add_fixtures([b'test_scmtools'])
    def test_delete_with_review_requests(self):
        """Testing the DELETE groups/<id>/ API with existing review requests"""
        self._login_user(admin=True)
        group = Group.objects.create(name=b'test-group', invite_only=True)
        group.users.add(self.user)
        repository = self.create_repository()
        request = ReviewRequest.objects.create(self.user, repository)
        request.target_groups.add(group)
        self.api_delete(get_review_group_item_url(b'test-group'), expected_status=204)
        request = ReviewRequest.objects.get(pk=request.id)
        self.assertEqual(request.target_groups.count(), 0)

    def setup_basic_get_test(self, user, with_local_site, local_site_name):
        group = self.create_review_group(with_local_site=with_local_site)
        return (
         get_review_group_item_url(group.name, local_site_name),
         review_group_item_mimetype,
         group)

    def test_get_not_modified(self):
        """Testing the GET groups/<id>/ API with Not Modified response"""
        Group.objects.create(name=b'test-group')
        self._testHttpCaching(get_review_group_item_url(b'test-group'), check_etags=True)

    def test_get_invite_only(self):
        """Testing the GET groups/<id>/ API with invite-only"""
        group = Group.objects.create(name=b'test-group', invite_only=True)
        group.users.add(self.user)
        rsp = self.api_get(get_review_group_item_url(group.name), expected_mimetype=review_group_item_mimetype)
        self.assertEqual(rsp[b'stat'], b'ok')
        self.assertEqual(rsp[b'group'][b'invite_only'], True)

    def test_get_invite_only_with_permission_denied_error(self):
        """Testing the GET groups/<id>/ API
        with invite-only and Permission Denied error
        """
        group = Group.objects.create(name=b'test-group', invite_only=True)
        rsp = self.api_get(get_review_group_item_url(group.name), expected_status=403)
        self.assertEqual(rsp[b'stat'], b'fail')
        self.assertEqual(rsp[b'err'][b'code'], PERMISSION_DENIED.code)

    def setup_basic_put_test(self, user, with_local_site, local_site_name, put_valid_data):
        group = self.create_review_group(with_local_site=with_local_site)
        return (
         get_review_group_item_url(group.name, local_site_name),
         review_group_item_mimetype,
         {b'name': b'my-group', 
            b'display_name': b'My Group', 
            b'mailing_list': b'mygroup@example.com'},
         group, [])

    def check_put_result(self, user, item_rsp, group):
        group = Group.objects.get(pk=group.pk)
        self.compare_item(item_rsp, group)

    def test_put_with_no_access(self, local_site=None):
        """Testing the PUT groups/<name>/ API with no access"""
        group = self.create_review_group(with_local_site=local_site is not None)
        rsp = self.api_put(get_review_group_item_url(group.name, local_site), {b'name': b'mygroup', 
           b'display_name': b'My Group', 
           b'mailing_list': b'mygroup@example.com'}, expected_status=403)
        self.assertEqual(rsp[b'stat'], b'fail')
        return

    def test_put_with_conflict(self):
        """Testing the PUT groups/<name>/ API
        with Group Already Exists error
        """
        group = self.create_review_group(name=b'group1')
        group2 = self.create_review_group(name=b'group2')
        self._login_user(admin=True)
        rsp = self.api_put(get_review_group_item_url(group.name), {b'name': group2.name}, expected_status=409)
        self.assertEqual(rsp[b'stat'], b'fail')
        self.assertEqual(rsp[b'err'][b'code'], GROUP_ALREADY_EXISTS.code)