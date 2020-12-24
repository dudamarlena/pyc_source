# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/sharing/tests.py
# Compiled at: 2010-09-29 05:19:38
import unittest
from django.contrib import admin
from django.contrib.auth.models import Group, User
from django.contrib.contenttypes.models import ContentType
from django.db import models
from sharing import utils
from sharing.admin import ShareAdminMixin
from sharing.models import GroupShare, UserShare
from snippetscream import RequestFactory

class TestModel(models.Model):
    pass


models.register_models('sharing', TestModel)

class TestModelAdmin(ShareAdminMixin, admin.ModelAdmin):
    pass


admin.site.register(TestModel, TestModelAdmin)

class ShareBackendTestCase(unittest.TestCase):

    def setUp(self):
        self.obj = TestModel.objects.create(id=1)
        self.user = User.objects.create(username='user')
        self.group = Group.objects.create(name='group')
        self.group_user = User.objects.create(username='group_user')
        self.group_user.groups.add(self.group)
        self.group_user.save()

    def tearDown(self):
        self.obj.delete()
        self.user.delete()
        self.group.delete()
        self.group_user.delete()

    def test_has_perm(self):
        self.failIf(self.user.has_perm('view', self.obj))
        self.failIf(self.user.has_perm('change', self.obj))
        self.failIf(self.user.has_perm('delete', self.obj))
        self.failIf(self.group_user.has_perm('view', self.obj))
        self.failIf(self.group_user.has_perm('change', self.obj))
        self.failIf(self.group_user.has_perm('delete', self.obj))
        UserShare.objects.create(user=self.user, can_view=True, can_change=True, can_delete=True, content_type=ContentType.objects.get_for_model(self.obj), object_id=self.obj.id)
        self.failUnless(self.user.has_perm('view', self.obj))
        self.failUnless(self.user.has_perm('change', self.obj))
        self.failUnless(self.user.has_perm('delete', self.obj))
        self.failIf(self.group_user.has_perm('view', self.obj))
        self.failIf(self.group_user.has_perm('change', self.obj))
        self.failIf(self.group_user.has_perm('delete', self.obj))
        GroupShare.objects.create(group=self.group, can_view=True, can_change=True, can_delete=True, content_type=ContentType.objects.get_for_model(self.obj), object_id=self.obj.id)
        self.failUnless(self.group_user.has_perm('view', self.obj))
        self.failUnless(self.group_user.has_perm('change', self.obj))
        self.failUnless(self.group_user.has_perm('delete', self.obj))


class ShareAdminTestCase(unittest.TestCase):

    def setUp(self):
        self.obj = TestModel.objects.create(id=1)
        self.user = User.objects.create(username='user')
        self.group = Group.objects.create(name='group')
        self.group_user = User.objects.create(username='group_user')
        self.group_user.groups.add(self.group)
        self.group_user.save()
        self.request = RequestFactory().get('/')
        self.share_admin = TestModelAdmin(TestModel, admin.site)

    def tearDown(self):
        self.obj.delete()
        self.user.delete()
        self.group.delete()
        self.group_user.delete()

    def test_has_change_permission(self):
        self.failIf(self.share_admin.has_change_permission(self.request, self.obj))
        self.request.user = self.user
        self.failIf(self.share_admin.has_change_permission(self.request, self.obj))
        UserShare.objects.get_or_create(user=self.user, can_change=True, content_type=ContentType.objects.get_for_model(self.obj), object_id=self.obj.id)
        self.failUnless(self.share_admin.has_change_permission(self.request, self.obj))
        self.request.user = self.group_user
        self.failIf(self.share_admin.has_change_permission(self.request, self.obj))
        GroupShare.objects.get_or_create(group=self.group, can_change=True, content_type=ContentType.objects.get_for_model(self.obj), object_id=self.obj.id)
        self.failUnless(self.share_admin.has_change_permission(self.request, self.obj))

    def test_has_delete_permission(self):
        self.failIf(self.share_admin.has_delete_permission(self.request, self.obj))
        self.request.user = self.user
        self.failIf(self.share_admin.has_delete_permission(self.request, self.obj))
        UserShare.objects.get_or_create(user=self.user, can_delete=True, content_type=ContentType.objects.get_for_model(self.obj), object_id=self.obj.id)
        self.failUnless(self.share_admin.has_delete_permission(self.request, self.obj))
        self.request.user = self.group_user
        self.failIf(self.share_admin.has_delete_permission(self.request, self.obj))
        GroupShare.objects.get_or_create(group=self.group, can_delete=True, content_type=ContentType.objects.get_for_model(self.obj), object_id=self.obj.id)
        self.failUnless(self.share_admin.has_delete_permission(self.request, self.obj))

    def test_queryset(self):
        self.failIf(self.share_admin.queryset(self.request))
        self.request.user = self.user
        self.failIf(self.share_admin.queryset(self.request))
        UserShare.objects.get_or_create(user=self.user, can_view=True, content_type=ContentType.objects.get_for_model(self.obj), object_id=self.obj.id)
        self.failUnless(self.obj in self.share_admin.queryset(self.request))
        self.request.user = self.group_user
        self.failIf(self.share_admin.queryset(self.request))
        GroupShare.objects.get_or_create(group=self.group, can_view=True, content_type=ContentType.objects.get_for_model(self.obj), object_id=self.obj.id)
        self.failUnless(self.obj in self.share_admin.queryset(self.request))


class UtilsTestCase(unittest.TestCase):

    def setUp(self):
        self.obj = TestModel.objects.create(id=1)
        self.user = User.objects.create(username='user')
        self.group = Group.objects.create(name='group')
        self.group_user = User.objects.create(username='group_user')
        self.group_user.groups.add(self.group)
        self.group_user.save()

    def tearDown(self):
        self.obj.delete()
        self.user.delete()
        self.group.delete()
        self.group_user.delete()

    def test_limit_queryset_by_permission(self):
        self.failIf(utils.limit_queryset_by_permission(TestModel.objects.all(), 'view', self.user))
        self.failIf(utils.limit_queryset_by_permission(TestModel.objects.all(), 'change', self.user))
        self.failIf(utils.limit_queryset_by_permission(TestModel.objects.all(), 'delete', self.user))
        self.failIf(utils.limit_queryset_by_permission(TestModel.objects.all(), 'view', self.group_user))
        self.failIf(utils.limit_queryset_by_permission(TestModel.objects.all(), 'change', self.group_user))
        self.failIf(utils.limit_queryset_by_permission(TestModel.objects.all(), 'delete', self.group_user))
        UserShare.objects.create(user=self.user, can_view=True, can_change=True, can_delete=True, content_type=ContentType.objects.get_for_model(self.obj), object_id=self.obj.id)
        self.failUnless(utils.limit_queryset_by_permission(TestModel.objects.all(), 'view', self.user))
        self.failUnless(utils.limit_queryset_by_permission(TestModel.objects.all(), 'change', self.user))
        self.failUnless(utils.limit_queryset_by_permission(TestModel.objects.all(), 'delete', self.user))
        self.failIf(utils.limit_queryset_by_permission(TestModel.objects.all(), 'view', self.group_user))
        self.failIf(utils.limit_queryset_by_permission(TestModel.objects.all(), 'change', self.group_user))
        self.failIf(utils.limit_queryset_by_permission(TestModel.objects.all(), 'delete', self.group_user))
        GroupShare.objects.create(group=self.group, can_view=True, can_change=True, can_delete=True, content_type=ContentType.objects.get_for_model(self.obj), object_id=self.obj.id)
        self.failUnless(utils.limit_queryset_by_permission(TestModel.objects.all(), 'view', self.group_user))
        self.failUnless(utils.limit_queryset_by_permission(TestModel.objects.all(), 'change', self.group_user))
        self.failUnless(utils.limit_queryset_by_permission(TestModel.objects.all(), 'delete', self.group_user))
        self.failUnless(self.user in utils.limit_queryset_by_permission(User.objects.all(), 'view', self.user))
        self.failUnless(self.user in utils.limit_queryset_by_permission(User.objects.all(), 'change', self.user))
        self.failUnless(self.user in utils.limit_queryset_by_permission(User.objects.all(), 'delete', self.user))
        self.failIf(self.user in utils.limit_queryset_by_permission(User.objects.all(), 'view', self.group_user))
        self.failIf(self.user in utils.limit_queryset_by_permission(User.objects.all(), 'change', self.group_user))
        self.failIf(self.user in utils.limit_queryset_by_permission(User.objects.all(), 'delete', self.group_user))