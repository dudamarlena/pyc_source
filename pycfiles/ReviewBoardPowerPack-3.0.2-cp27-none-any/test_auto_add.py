# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /beanbag_licensing/tests/test_auto_add.py
# Compiled at: 2019-06-17 15:11:31
from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.core import mail
from kgb import SpyAgency
from reviewboard.reviews.models import Group
from beanbag_licensing.auto_add import AutoAddMode
from beanbag_licensing.tests.testcases import LicensedExtensionTestCase

class AutoAddTestCase(SpyAgency, LicensedExtensionTestCase):
    """Base test case for licensing auto-add abilities."""

    def setUp(self):
        super(AutoAddTestCase, self).setUp()
        self.spy_on(self.license_settings.sync_licensed_users)


class AutoAddNewTests(AutoAddTestCase):
    """Unit tests for auto-add with mode=all-new."""

    def test_new_user(self):
        """Testing auto_add_mode=all-new and new user"""
        self.extension.settings[b'auto_add_mode'] = AutoAddMode.ALL_NEW
        user = User.objects.create(username=b'test-user')
        self.assertTrue(self.license_settings.is_user_licensed(user))
        self.assertTrue(self.license_settings.sync_licensed_users.called)

    def test_join_group(self):
        """Testing auto_add_mode=all-new and joining group"""
        group = Group.objects.create(name=b'test-group')
        user = User.objects.create(username=b'test-user')
        self.extension.settings.update({b'auto_add_mode': AutoAddMode.ALL_NEW, 
           b'auto_add_groups': [
                              group.pk]})
        group.users.add(user)
        self.assertFalse(self.license_settings.is_user_licensed(user))
        self.assertFalse(self.license_settings.sync_licensed_users.called)


class AutoAddDisabledTests(AutoAddTestCase):
    """Unit tests for auto-add with mode=disabled."""

    def test_new_user(self):
        """Testing auto_add_mode=disabled and new user"""
        self.extension.settings[b'auto_add_mode'] = AutoAddMode.DISABLED
        user = User.objects.create(username=b'test-user')
        self.assertFalse(self.license_settings.is_user_licensed(user))
        self.assertFalse(self.license_settings.sync_licensed_users.called)

    def test_join_group(self):
        """Testing auto_add_mode=disabled and joining group"""
        group = Group.objects.create(name=b'test-group')
        user = User.objects.create(username=b'test-user')
        self.extension.settings.update({b'auto_add_mode': AutoAddMode.DISABLED, 
           b'auto_add_groups': [
                              group.pk]})
        group.users.add(user)
        self.assertFalse(self.license_settings.is_user_licensed(user))
        self.assertFalse(self.license_settings.sync_licensed_users.called)


class AutoAddGroupsTests(AutoAddTestCase):
    """Unit tests for auto-add with mode=groups."""

    def test_new_user(self):
        """Testing auto_add_mode=groups and new user"""
        self.extension.settings[b'auto_add_mode'] = AutoAddMode.GROUPS
        user = User.objects.create(username=b'test-user')
        self.assertFalse(self.license_settings.is_user_licensed(user))
        self.assertFalse(self.license_settings.sync_licensed_users.called)

    def test_join_group(self):
        """Testing auto_add_mode=groups and joining group"""
        group = Group.objects.create(name=b'test-group')
        user = User.objects.create(username=b'test-user')
        self.extension.settings.update({b'auto_add_mode': AutoAddMode.GROUPS, 
           b'auto_add_groups': [
                              group.pk]})
        group.users.add(user)
        self.assertTrue(self.license_settings.is_user_licensed(user))
        self.assertTrue(self.license_settings.sync_licensed_users.called)

    def test_join_group_hit_cap(self):
        """Testing auto_add_mode=groups and joining group hit cap"""
        self.install_license_data(users=1)
        group = Group.objects.create(name=b'test-group')
        user = User.objects.create(username=b'test-user')
        self.extension.settings.update({b'auto_add_mode': AutoAddMode.GROUPS, 
           b'auto_add_groups': [
                              group.pk]})
        group.users.add(user)
        self.assertTrue(self.license_settings.is_user_licensed(user))
        self.assertTrue(self.license_settings.sync_licensed_users.called)
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, b'Test license limit reached')
        self.assertEqual(mail.outbox[0].body, b'Your Test license limit of 1 user has been reached.\nYou will be unable to add any more users to your current license.\n\nTo upgrade your license, please contact us at support@beanbaginc.com, and\nwe will assist you.\n\n- Beanbag, Inc.\n')

    def test_join_group_exceeds_cap(self):
        """Testing auto_add_mode=groups and joining group exceeds cap"""
        self.install_license_data(users=1)
        group = Group.objects.create(name=b'test-group')
        user1 = User.objects.create(username=b'doc')
        user2 = User.objects.create(username=b'grumpy')
        user3 = User.objects.create(username=b'sleepy')
        self.extension.settings.update({b'auto_add_mode': AutoAddMode.GROUPS, 
           b'auto_add_groups': [
                              group.pk]})
        group.users.add(user1, user2, user3)
        self.assertTrue(self.license_settings.is_user_licensed(user1))
        self.assertFalse(self.license_settings.is_user_licensed(user2))
        self.assertFalse(self.license_settings.is_user_licensed(user3))
        self.assertTrue(self.license_settings.sync_licensed_users.called)
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, b'Test license limit reached')
        self.assertEqual(mail.outbox[0].body, b'Your Test license limit of 1 user has been reached.\nYou will be unable to add any more users to your current license.\n\nThe following users could not be added to your license:\n\n    * grumpy\n    * sleepy\n\nTo upgrade your license, please contact us at support@beanbaginc.com, and\nwe will assist you.\n\n- Beanbag, Inc.\n')

    def test_join_other_group(self):
        """Testing auto_add_mode=groups and joining other group"""
        test_group = Group.objects.create(name=b'test-group')
        other_group = Group.objects.create(name=b'other-group')
        user = User.objects.create(username=b'test-user')
        self.extension.settings.update({b'auto_add_mode': AutoAddMode.GROUPS, 
           b'auto_add_groups': [
                              test_group.pk]})
        other_group.users.add(user)
        self.assertFalse(self.license_settings.is_user_licensed(user))
        self.assertFalse(self.license_settings.sync_licensed_users.called)


class AutoRemoveTests(AutoAddTestCase):
    """Unit tests for auto-removing users."""

    def test_user_deleted(self):
        """Testing auto-removing deleted users from license"""
        user = User.objects.create(username=b'test-user')
        self.license_settings.add_licensed_users([user])
        self.assertEqual(self.license_settings.licensed_user_ids, [user.pk])
        self.assertTrue(self.license_settings.is_user_licensed(user))
        self.assertTrue(self.license_settings.sync_licensed_users.called)
        self.license_settings.sync_licensed_users.reset_calls()
        user.delete()
        self.assertEqual(self.license_settings.licensed_user_ids, [])
        self.assertTrue(self.license_settings.sync_licensed_users.called)

    def test_inactive_users(self):
        """Testing auto-removing inactive users from license"""
        user = User.objects.create(username=b'test-user')
        self.license_settings.add_licensed_users([user])
        self.assertEqual(self.license_settings.licensed_user_ids, [user.pk])
        self.assertTrue(self.license_settings.is_user_licensed(user))
        self.assertTrue(self.license_settings.sync_licensed_users.called)
        self.license_settings.sync_licensed_users.reset_calls()
        user.is_active = False
        user.save()
        self.assertEqual(self.license_settings.licensed_user_ids, [])
        self.assertTrue(self.license_settings.sync_licensed_users.called)