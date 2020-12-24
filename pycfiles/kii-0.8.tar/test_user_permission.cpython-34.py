# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/eliotberriot/Seafile/kii/kii_main/kii/permission/tests/test_user_permission.py
# Compiled at: 2014-12-14 11:41:07
# Size of source mod 2**32: 3044 bytes
import django
from guardian.shortcuts import assign
from guardian.models import UserObjectPermission
from kii.stream.tests import base
from kii.tests import test_base_models
from .. import forms

class TestUserPermission(base.StreamTestCase):

    def test_view_permission(self):
        u2 = self.users[2]
        stream = self.streams[0]
        stream.assign_perm('read', u2)
        self.assertEqual(stream.readable_by(u2), True)
        self.assertEqual(stream.writable_by(u2), False)
        self.assertEqual(stream.deletable_by(u2), False)

    def test_edit_permission(self):
        u2 = self.users[2]
        stream = self.streams[0]
        stream.assign_perm('write', u2)
        self.assertEqual(stream.readable_by(u2), True)
        self.assertEqual(stream.writable_by(u2), True)
        self.assertEqual(stream.deletable_by(u2), False)

    def test_remove_permission(self):
        u2 = self.users[2]
        stream = self.streams[0]
        stream.assign_perm('delete', u2)
        self.assertEqual(stream.readable_by(u2), True)
        self.assertEqual(stream.writable_by(u2), True)
        self.assertEqual(stream.deletable_by(u2), True)

    def test_can_remove_permission(self):
        i = self.streams[0]
        i.assign_perm('read', self.anonymous_user)
        self.assertEqual(i.readable_by(self.anonymous_user), True)
        i.remove_perm('read', self.anonymous_user)
        self.assertEqual(i.readable_by(self.anonymous_user), False)

    def test_owner_gets_all_permissions(self):
        stream = self.streams[0]
        self.assertEqual(stream.deletable_by(stream.owner), True)

    def test_permission_is_deleted_when_stream_is_deleted(self):
        u2 = self.users[2]
        stream = self.streams[0]
        perm = stream.assign_perm('delete', u2)
        u2.delete()
        with self.assertRaises(UserObjectPermission.DoesNotExist):
            UserObjectPermission.objects.get(pk=perm.pk)

    def test_permission_mixin_form_populate_fields_correctly(self):
        i = self.streams[0]
        i.assign_perm('read', self.anonymous_user)
        form = forms.PermissionMixinForm(instance=i)
        self.assertEqual(form.fields['readable_by'].initial, 'everybody')

    def test_permission_mixin_form__save_create_permission(self):
        i = self.streams[0]
        form = forms.PermissionMixinForm(data={'readable_by': 'everybody'}, instance=i)
        self.assertEqual(form.is_valid(), True)
        form.save()
        self.assertEqual(i.readable_by(self.anonymous_user), True)

    def test_permission_mixin_form_delete_obsolete_permission(self):
        i = self.streams[0]
        i.assign_perm('read', self.anonymous_user)
        form = forms.PermissionMixinForm(data={'readable_by': 'owner'}, instance=i)
        self.assertEqual(form.is_valid(), True)
        form.save()
        self.assertEqual(i.readable_by(self.anonymous_user), False)