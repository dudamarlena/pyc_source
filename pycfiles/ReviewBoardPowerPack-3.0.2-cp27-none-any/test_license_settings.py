# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /beanbag_licensing/tests/test_license_settings.py
# Compiled at: 2019-06-17 15:11:31
from __future__ import unicode_literals
from django.contrib.auth.models import User
from kgb import SpyAgency
from beanbag_licensing.errors import TooManyUsersForLicenseError
from beanbag_licensing.tests.models import LicensedUser
from beanbag_licensing.tests.testcases import LicensedExtensionTestCase

class LicenseSettingsTest(SpyAgency, LicensedExtensionTestCase):
    """Unit tests for LicenseSettings."""
    should_install_default_license = False

    def test_default_settings(self):
        """Testing LicenseSettings updates default_settings"""
        default_settings = self.extension.default_settings
        self.assertIn(b'license_data', default_settings)
        self.assertIn(b'licensed_users_stamp', default_settings)
        self.assertEqual(default_settings[b'license_data'], b'')
        self.assertEqual(default_settings[b'licensed_users_stamp'], b'')

    def test_add_licensed_users(self):
        """Testing LicenseSettings.add_licensed_users"""
        self.install_license_data(users=100)
        user1 = User.objects.create(username=b'doc')
        user2 = User.objects.create(username=b'dopey')
        self.license_settings.add_licensed_users([user1, user2])
        licensed_users = list(LicensedUser.objects.all())
        self.assertEqual(len(licensed_users), 2)
        self.assertEqual(licensed_users[0].user, user1)
        self.assertEqual(licensed_users[1].user, user2)

    def test_add_licensed_users_with_existing(self):
        """Testing LicenseSettings.add_licensed_users with existing licensed users"""
        self.install_license_data(users=100)
        user1 = User.objects.create(username=b'doc')
        user2 = User.objects.create(username=b'dopey')
        LicensedUser.objects.create(user=user1)
        self.license_settings.add_licensed_users([user1, user2])
        licensed_users = list(LicensedUser.objects.all())
        self.assertEqual(len(licensed_users), 2)
        self.assertEqual(licensed_users[0].user, user1)
        self.assertEqual(licensed_users[1].user, user2)

    def test_add_licensed_users_hit_cap(self):
        """Testing LicenseSettings.add_licensed_users with hitting user cap"""
        self.install_license_data(users=2)
        user1 = User.objects.create(username=b'doc')
        user2 = User.objects.create(username=b'dopey')
        self.license_settings.add_licensed_users([user1, user2])
        licensed_users = list(LicensedUser.objects.all())
        self.assertEqual(len(licensed_users), 2)
        self.assertEqual(licensed_users[0].user, user1)
        self.assertEqual(licensed_users[1].user, user2)

    def test_add_licensed_users_exceed_cap(self):
        """Testing LicenseSettings.add_licensed_users with exceeding user cap"""
        self.install_license_data(users=1)
        user1 = User.objects.create(username=b'doc')
        user2 = User.objects.create(username=b'dopey')
        user3 = User.objects.create(username=b'sleepy')
        self.assertRaises(TooManyUsersForLicenseError, lambda : self.license_settings.add_licensed_users([user1, user2,
         user3]))
        self.assertEqual(LicensedUser.objects.count(), 0)

    def test_remove_licensed_users(self):
        """Testing LicenseSettings.remove_licensed_users"""
        self.install_default_license()
        user1 = User.objects.create(username=b'doc')
        user2 = User.objects.create(username=b'dopey')
        user3 = User.objects.create(username=b'sleepy')
        LicensedUser.objects.create(user=user1)
        LicensedUser.objects.create(user=user2)
        LicensedUser.objects.create(user=user3)
        self.license_settings.sync_licensed_users()
        self.assertEqual(self.license_settings.licensed_user_ids, [
         user1.pk, user2.pk, user3.pk])
        self.license_settings.remove_licensed_users([user1.pk, user2.pk])
        self.assertEqual(self.license_settings.licensed_user_ids, [user3.pk])
        licensed_users = list(LicensedUser.objects.all())
        self.assertEqual(len(licensed_users), 1)
        self.assertEqual(licensed_users[0].user, user3)

    def test_remove_licensed_users_with_stale_user_id(self):
        """Testing LicenseSettings.remove_licensed_users with stale user ID"""
        self.install_default_license()
        user1 = User.objects.create(username=b'doc')
        user2 = User.objects.create(username=b'dopey')
        user3 = User.objects.create(username=b'sleepy')
        LicensedUser.objects.create(user=user1)
        LicensedUser.objects.create(user=user2)
        LicensedUser.objects.create(user=user3)
        self.license_settings.sync_licensed_users()
        self.assertEqual(self.license_settings.licensed_user_ids, [
         user1.pk, user2.pk, user3.pk])
        self.spy_on(self.license_settings.remove_licensed_users, call_original=False)
        user3_id = user3.pk
        user3.delete()
        self.license_settings.remove_licensed_users.unspy()
        self.assertEqual(self.license_settings.licensed_user_ids, [
         user1.pk, user2.pk, user3_id])
        self.license_settings.remove_licensed_users([user3_id])
        self.assertEqual(self.license_settings.licensed_user_ids, [
         user1.pk, user2.pk])
        licensed_users = list(LicensedUser.objects.all())
        self.assertEqual(len(licensed_users), 2)
        self.assertEqual(licensed_users[0].user, user1)
        self.assertEqual(licensed_users[1].user, user2)

    def test_remove_licensed_users_with_unlicensed_user(self):
        """Testing LicenseSettings.remove_licensed_users with unlicensed user"""
        self.install_default_license()
        user = User.objects.create(username=b'doc')
        self.assertEqual(self.license_settings.licensed_user_ids, [])
        self.license_settings.remove_licensed_users([user.pk])
        self.assertEqual(self.license_settings.licensed_user_ids, [])
        licensed_users = list(LicensedUser.objects.all())
        self.assertEqual(len(licensed_users), 0)

    def test_licensed_user_ids(self):
        """Testing LicenseSettings.licensed_user_ids"""
        self.install_license_data(users=100)
        user1 = User.objects.create(username=b'doc')
        user2 = User.objects.create(username=b'dopey')
        LicensedUser.objects.create(user=user1)
        LicensedUser.objects.create(user=user2)
        self.assertEqual(self.license_settings.licensed_user_ids, [
         user1.pk, user2.pk])

    def test_licensed_user_ids_caps(self):
        """Testing LicenseSettings.licensed_user_ids caps results"""
        self.install_license_data(users=1)
        user1 = User.objects.create(username=b'doc')
        user2 = User.objects.create(username=b'dopey')
        LicensedUser.objects.create(user=user1)
        LicensedUser.objects.create(user=user2)
        self.assertEqual(self.license_settings.licensed_user_ids, [
         user1.pk])

    def test_licensed_user_ids_no_license(self):
        """Testing LicenseSettings.licensed_user_ids without a license"""
        user1 = User.objects.create(username=b'doc')
        LicensedUser.objects.create(user=user1)
        self.assertEqual(self.license_settings.licensed_user_ids, [user1.pk])

    def test_licensed_users(self):
        """Testing LicenseSettings.licensed_users"""
        self.install_license_data(users=100)
        user1 = User.objects.create(username=b'doc')
        user2 = User.objects.create(username=b'dopey')
        LicensedUser.objects.create(user=user1)
        LicensedUser.objects.create(user=user2)
        licensed_users = list(self.license_settings.licensed_users)
        self.assertEqual(len(licensed_users), 2)
        self.assertEqual(licensed_users[0].user, user1)
        self.assertEqual(licensed_users[1].user, user2)

    def test_licensed_users_caps(self):
        """Testing LicenseSettings.licensed_users caps results"""
        self.install_license_data(users=1)
        user1 = User.objects.create(username=b'doc')
        user2 = User.objects.create(username=b'dopey')
        LicensedUser.objects.create(user=user1)
        LicensedUser.objects.create(user=user2)
        licensed_users = list(self.license_settings.licensed_users)
        self.assertEqual(len(licensed_users), 1)
        self.assertEqual(licensed_users[0].user, user1)

    def test_licensed_users_no_license(self):
        """Testing LicenseSettings.licensed_users without a license"""
        user1 = User.objects.create(username=b'doc')
        licensed_user1 = LicensedUser.objects.create(user=user1)
        self.assertEqual(list(self.license_settings.licensed_users), [
         licensed_user1])

    def test_licensed_user_count(self):
        """Testing LicenseSettings.licensed_user_count"""
        self.install_license_data(users=100)
        user1 = User.objects.create(username=b'doc')
        user2 = User.objects.create(username=b'dopey')
        LicensedUser.objects.create(user=user1)
        LicensedUser.objects.create(user=user2)
        self.assertEqual(self.license_settings.licensed_user_count, 2)

    def test_licensed_user_count_caps(self):
        """Testing LicenseSettings.licensed_user_count caps results"""
        self.install_license_data(users=1)
        user1 = User.objects.create(username=b'doc')
        user2 = User.objects.create(username=b'dopey')
        LicensedUser.objects.create(user=user1)
        LicensedUser.objects.create(user=user2)
        self.assertEqual(self.license_settings.licensed_user_count, 1)

    def test_licensed_user_count_no_license(self):
        """Testing LicenseSettings.licensed_user_count without a license"""
        user1 = User.objects.create(username=b'doc')
        LicensedUser.objects.create(user=user1)
        self.assertEqual(self.license_settings.licensed_user_count, 1)

    def test_hit_licensed_user_count_under(self):
        """Testing LicenseSettings.hit_licensed_user_count when under count"""
        self.install_license_data(users=100)
        user1 = User.objects.create(username=b'doc')
        user2 = User.objects.create(username=b'dopey')
        LicensedUser.objects.create(user=user1)
        LicensedUser.objects.create(user=user2)
        self.assertFalse(self.license_settings.hit_licensed_user_count)

    def test_hit_licensed_user_count_maxed(self):
        """Testing LicenseSettings.hit_licensed_user_count when maxed"""
        self.install_license_data(users=2)
        user1 = User.objects.create(username=b'doc')
        user2 = User.objects.create(username=b'dopey')
        LicensedUser.objects.create(user=user1)
        LicensedUser.objects.create(user=user2)
        self.assertTrue(self.license_settings.hit_licensed_user_count)

    def test_hit_licensed_user_count_over(self):
        """Testing LicenseSettings.hit_licensed_user_count when over count"""
        self.install_license_data(users=1)
        user1 = User.objects.create(username=b'doc')
        user2 = User.objects.create(username=b'dopey')
        self.assertFalse(self.license_settings.hit_licensed_user_count)
        LicensedUser.objects.create(user=user1)
        self.license_settings._licensed_user_ids = None
        self.assertTrue(self.license_settings.hit_licensed_user_count)
        LicensedUser.objects.create(user=user2)
        self.license_settings._licensed_user_ids = None
        self.assertTrue(self.license_settings.hit_licensed_user_count)
        return

    def test_hit_licensed_user_no_license(self):
        """Testing LicenseSettings.hit_licensed_user_count without a license"""
        user1 = User.objects.create(username=b'doc')
        user2 = User.objects.create(username=b'dopey')
        self.assertFalse(self.license_settings.hit_licensed_user_count)
        LicensedUser.objects.create(user=user1)
        self.license_settings._licensed_user_ids = None
        self.assertFalse(self.license_settings.hit_licensed_user_count)
        LicensedUser.objects.create(user=user2)
        self.license_settings._licensed_user_ids = None
        self.assertTrue(self.license_settings.hit_licensed_user_count)
        return

    def test_hit_licensed_user_no_cap(self):
        """Testing LicenseSettings.hit_licensed_user_count without a cap"""
        self.install_license_data(users=None)
        user1 = User.objects.create(username=b'doc')
        user2 = User.objects.create(username=b'dopey')
        LicensedUser.objects.create(user=user1)
        LicensedUser.objects.create(user=user2)
        self.assertFalse(self.license_settings.hit_licensed_user_count)
        return

    def test_licensed_users_remaining(self):
        """Testing LicenseSettings.licensed_users_remaining"""
        self.install_license_data(users=10)
        user1 = User.objects.create(username=b'doc')
        user2 = User.objects.create(username=b'dopey')
        LicensedUser.objects.create(user=user1)
        LicensedUser.objects.create(user=user2)
        self.assertEqual(self.license_settings.licensed_users_remaining, 8)

    def test_licensed_users_remaining_without_license(self):
        """Testing LicenseSettings.licensed_users_remaining without a license"""
        user1 = User.objects.create(username=b'doc')
        user2 = User.objects.create(username=b'dopey')
        LicensedUser.objects.create(user=user1)
        LicensedUser.objects.create(user=user2)
        self.assertEqual(self.license_settings.licensed_users_remaining, 0)

    def test_licensed_users_remaining_without_cap(self):
        """Testing LicenseSettings.licensed_users_remaining without a cap"""
        self.install_license_data(users=None)
        user1 = User.objects.create(username=b'doc')
        user2 = User.objects.create(username=b'dopey')
        LicensedUser.objects.create(user=user1)
        LicensedUser.objects.create(user=user2)
        self.assertRaises(AssertionError, lambda : self.license_settings.licensed_users_remaining)
        return

    def test_is_user_licensed_with_licensed_user(self):
        """Testing LicenseSettings.is_user_licensed with licensed user"""
        self.install_license_data(users=10)
        user = User.objects.create(username=b'doc')
        LicensedUser.objects.create(user=user)
        self.assertTrue(self.license_settings.is_user_licensed(user))

    def test_is_user_licensed_without_licensed_user(self):
        """Testing LicenseSettings.is_user_licensed without licensed user"""
        self.install_license_data(users=10)
        user = User.objects.create(username=b'doc')
        self.assertFalse(self.license_settings.is_user_licensed(user))

    def test_is_user_licensed_without_license(self):
        """Testing LicenseSettings.is_user_licensed without a license"""
        user = User.objects.create(username=b'doc')
        LicensedUser.objects.create(user=user)
        self.assertTrue(self.license_settings.is_user_licensed(user))

    def test_sync_licensed_users(self):
        """Testing LicenseSettings.sync_licensed_users"""
        self.spy_on(self.extension.settings.save, call_original=False)
        old_stamp = self.extension.settings[b'licensed_users_stamp']
        self.license_settings.sync_licensed_users()
        new_stamp = self.extension.settings[b'licensed_users_stamp']
        self.assertNotEqual(new_stamp, b'')
        self.assertNotEqual(old_stamp, new_stamp)
        self.assertTrue(self.extension.settings.save.called)