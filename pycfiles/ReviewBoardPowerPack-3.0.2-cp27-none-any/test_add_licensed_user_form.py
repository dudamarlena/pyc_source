# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /beanbag_licensing/tests/test_add_licensed_user_form.py
# Compiled at: 2019-06-17 15:11:31
from __future__ import unicode_literals
from django.contrib.auth.models import User
from beanbag_licensing.forms import AddLicensedUserForm
from beanbag_licensing.tests.models import LicensedUser
from beanbag_licensing.tests.testcases import LicensedExtensionTestCase

class AddLicensedUserFormTests(LicensedExtensionTestCase):
    """Unit tests for AddLicensedUserForm."""

    def test_save(self):
        """Testing AddLicensedUserForm.save"""
        user1 = User.objects.create(username=b'doc')
        user2 = User.objects.create(username=b'dopey')
        form = AddLicensedUserForm(None, self.extension, {b'users': b'doc,dopey'})
        self.assertTrue(form.is_valid())
        form.save()
        licensed_users = list(LicensedUser.objects.all())
        self.assertEqual(len(licensed_users), 2)
        self.assertEqual(licensed_users[0].user, user1)
        self.assertEqual(licensed_users[1].user, user2)
        return

    def test_validation_success(self):
        """Testing AddLicensedUserForm validation with no errors"""
        User.objects.create(username=b'doc')
        User.objects.create(username=b'dopey')
        form = AddLicensedUserForm(None, self.extension, {b'users': b'doc,dopey'})
        self.assertTrue(form.is_valid())
        return

    def test_validation_invalid_user(self):
        """Testing AddLicensedUserForm validation with invalid user"""
        form = AddLicensedUserForm(None, self.extension, {b'users': b'doc'})
        self.assertFalse(form.is_valid())
        self.assertIn(b'users', form.errors)
        self.assertEqual(form.errors[b'users'], [b'There is no user named doc'])
        return

    def test_validation_already_added(self):
        """Testing AddLicensedUserForm validation with already licensed user"""
        user = User.objects.create(username=b'doc')
        LicensedUser.objects.create(user=user)
        self.extension.license_settings.sync_licensed_users()
        form = AddLicensedUserForm(None, self.extension, {b'users': b'doc'})
        self.assertFalse(form.is_valid())
        self.assertIn(b'users', form.errors)
        self.assertEqual(form.errors[b'users'], [
         b'doc is already a licensed user'])
        return