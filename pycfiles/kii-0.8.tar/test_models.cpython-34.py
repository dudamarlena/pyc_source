# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/eliotberriot/Seafile/kii/kii_main/kii/permission/tests/test_models.py
# Compiled at: 2014-10-10 08:40:24
# Size of source mod 2**32: 5488 bytes
from kii.stream.tests import base
from kii.tests.test_permission import models
from kii import user
import django

class TestPermissionMixin(base.StreamTestCase):

    def test_owner_can_view_permissionmodel(self):
        m = self.G(models.PermissionModel, owner=self.users[0])
        self.assertEqual(m.readable_by(self.users[0]), True)

    def test_permissionmodel_queryset_can_filter_instances_using_all_perms_level(self):
        m0 = self.G(models.PermissionModel, owner=self.users[0])
        m1 = self.G(models.PermissionModel, owner=self.users[0])
        m1.assign_perm('delete', self.users[1])
        m2 = self.G(models.PermissionModel, owner=self.users[0])
        user = self.users[1]
        queryset = models.PermissionModel.objects.readable_by(user)
        self.assertEqual(len(queryset), 1)
        self.assertIn(m1, queryset)

    def test_can_assign_permission_to_group(self):
        m0 = self.G(models.PermissionModel, owner=self.users[0])
        m0.assign_perm('read', self.all_users_group)
        self.assertEqual(m0.readable_by(self.users[1]), True)

    def test_allowing_premissions_to_anonymous_allow_to_everybody(self):
        m0 = self.G(models.PermissionModel, owner=self.users[0])
        m0.assign_perm('read', self.anonymous_user)
        for user in self.user_model.objects.all():
            self.assertEqual(m0.readable_by(user), True)

    def test_allowing_all_users_group_does_not_allow_anonymous(self):
        m0 = self.G(models.PermissionModel, owner=self.users[0])
        m0.assign_perm('read', user.models.get_all_users_group())
        for u in self.user_model.objects.all().exclude(pk=self.anonymous_user.pk):
            self.assertEqual(m0.readable_by(u), True)

        self.assertEqual(m0.readable_by(self.anonymous_user), False)


class TestInheritPermissionMixin(base.StreamTestCase):

    def test_inheritopermissionmodel_inherit_root_owner(self):
        p = self.G(models.PermissionModel, owner=self.users[0])
        m = self.G(models.InheritPermissionModel, root=p, inherit_permissions=True)
        self.assertEqual(m.owner, self.users[0])

    def test_inheritpermissionmodel_can_inherit_permissions(self):
        p = self.G(models.PermissionModel, owner=self.users[0])
        m = self.G(models.InheritPermissionModel, root=p, inherit_permissions=True)
        self.assertEqual(m.readable_by(self.users[1]), False)
        p.assign_perm('read', self.users[1])
        self.assertEqual(m.readable_by(self.users[1]), True)

    def test_inheritpermissionqueryset_include_correct_objects(self):
        p = self.G(models.PermissionModel, owner=self.users[0])
        m1 = self.G(models.InheritPermissionModel, root=p, inherit_permissions=True)
        m2 = self.G(models.InheritPermissionModel, root=p, inherit_permissions=True)
        m3 = self.G(models.InheritPermissionModel, root=p, inherit_permissions=False)
        m4 = self.G(models.InheritPermissionModel, root=p, inherit_permissions=False)
        p.assign_perm('read', self.anonymous_user)
        readable = models.InheritPermissionModel.objects.all().readable_by(self.users[1])
        self.assertQuerysetEqualIterable(readable, [m1, m2], ordered=False)

    def test_inheritpermissionqueryset_include_all_owned_objects(self):
        p = self.G(models.PermissionModel, owner=self.users[0])
        m1 = self.G(models.InheritPermissionModel, root=p, inherit_permissions=True)
        m2 = self.G(models.InheritPermissionModel, root=p, inherit_permissions=True)
        m3 = self.G(models.InheritPermissionModel, root=p, inherit_permissions=False)
        m4 = self.G(models.InheritPermissionModel, root=p, inherit_permissions=False)
        readable = models.InheritPermissionModel.objects.all().readable_by(self.users[0])
        self.assertQuerysetEqualIterable(readable, [m1, m2, m3, m4], ordered=False)

    def test_inheritinheritpermissionmodel_can_inherit_permissions(self):
        p = self.G(models.PermissionModel, owner=self.users[0])
        m = self.G(models.InheritPermissionModel, root=p, inherit_permissions=True)
        i = self.G(models.InheritInheritPermissionModel, root=m, inherit_permissions=True)
        self.assertEqual(i.readable_by(self.users[1]), False)
        p.assign_perm('read', self.users[1])
        self.assertEqual(i.readable_by(self.users[1]), True)

    def test_inheritinheritpermissionqueryset_include_correct_objects(self):
        p = self.G(models.PermissionModel, owner=self.users[0])
        m1 = self.G(models.InheritPermissionModel, root=p, inherit_permissions=True)
        m2 = self.G(models.InheritPermissionModel, root=p, inherit_permissions=True)
        m3 = self.G(models.InheritPermissionModel, root=p, inherit_permissions=False)
        m4 = self.G(models.InheritPermissionModel, root=p, inherit_permissions=False)
        i1 = self.G(models.InheritInheritPermissionModel, root=m1, inherit_permissions=True)
        i2 = self.G(models.InheritInheritPermissionModel, root=m2, inherit_permissions=False)
        i3 = self.G(models.InheritInheritPermissionModel, root=m3, inherit_permissions=True)
        i4 = self.G(models.InheritInheritPermissionModel, root=m4, inherit_permissions=False)
        p.assign_perm('read', self.anonymous_user)
        i4.assign_perm('read', self.users[1])
        readable = models.InheritInheritPermissionModel.objects.all().readable_by(self.users[1])
        self.assertQuerysetEqualIterable(readable, [i1, i4], ordered=False)