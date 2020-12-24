# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /beanbag_licensing/tests/test_import_licensed_users_form.py
# Compiled at: 2019-06-17 15:11:31
from __future__ import unicode_literals
from django.contrib.auth.models import User
from reviewboard.reviews.models import Group
from beanbag_licensing.forms import ImportLicensedUsersForm
from beanbag_licensing.tests.models import LicensedUser
from beanbag_licensing.tests.testcases import LicensedExtensionTestCase

class ImportLicensedUsersFormTests(LicensedExtensionTestCase):
    """Unit tests for ImportLicensedUsersForm."""

    def test_import_users_all(self):
        """Testing ImportLicensedUsersForm.import_users with all"""
        user1 = User.objects.create(username=b'doc')
        user2 = User.objects.create(username=b'dopey')
        User.objects.create(username=b'sleepy', is_active=False)
        form = ImportLicensedUsersForm(None, self.extension, {b'source': b'all'})
        self.assertTrue(form.is_valid())
        form.import_users(100)
        licensed_users = list(LicensedUser.objects.all())
        self.assertEqual(len(licensed_users), 2)
        self.assertEqual(licensed_users[0].user, user1)
        self.assertEqual(licensed_users[1].user, user2)
        return

    def test_import_users_group(self):
        """Testing ImportLicensedUsersForm.import_users with group"""
        user1 = User.objects.create(username=b'doc')
        user2 = User.objects.create(username=b'sleepy', is_active=False)
        User.objects.create(username=b'dopey')
        group = Group.objects.create(name=b'test')
        group.users.add(user1)
        group.users.add(user2)
        form = ImportLicensedUsersForm(None, self.extension, {b'source': b'group', 
           b'group': group.pk})
        self.assertTrue(form.is_valid())
        form.import_users(100)
        licensed_users = list(LicensedUser.objects.all())
        self.assertEqual(len(licensed_users), 1)
        self.assertEqual(licensed_users[0].user, user1)
        return