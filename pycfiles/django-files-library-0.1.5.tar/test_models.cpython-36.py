# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.6/site-packages/django_files_library/tests/test_models.py
# Compiled at: 2018-02-10 09:33:43
# Size of source mod 2**32: 2382 bytes
from django_files_library.tests.base_setup import BaseSetupTestCase

class LibraryModelTestCase(BaseSetupTestCase):

    def test_user1_permissions(self):
        """assert user1 permissions"""
        self.assertEqual(self.public_library.user_can_read(self.user1), True)
        self.assertEqual(self.public_library.user_can_write(self.user1), True)
        self.assertEqual(self.private_library.user_can_read(self.user1), True)
        self.assertEqual(self.private_library.user_can_write(self.user1), True)

    def test_user2_permissions(self):
        """assert user1 permissions"""
        self.assertEqual(self.public_library.user_can_read(self.user2), True)
        self.assertEqual(self.public_library.user_can_write(self.user2), True)
        self.assertEqual(self.private_library.user_can_read(self.user2), False)
        self.assertEqual(self.private_library.user_can_write(self.user2), True)

    def test_user3_permissions(self):
        """assert user1 permissions"""
        self.assertEqual(self.public_library.user_can_read(self.user3), True)
        self.assertEqual(self.public_library.user_can_write(self.user3), False)
        self.assertEqual(self.private_library.user_can_read(self.user3), True)
        self.assertEqual(self.private_library.user_can_write(self.user3), False)

    def test_user4_permissions(self):
        """assert user1 permissions"""
        self.assertEqual(self.public_library.user_can_read(self.user4), True)
        self.assertEqual(self.public_library.user_can_write(self.user4), False)
        self.assertEqual(self.private_library.user_can_read(self.user4), False)
        self.assertEqual(self.private_library.user_can_write(self.user4), False)

    def test_library_str(self):
        """assert user1 permissions"""
        self.assertEqual(str(self.public_library), self.public_library.name)

    def test_permissions_str(self):
        """assert user1 permissions"""
        self.assertEqual(str(self.permissions1), self.permissions1.library.name + ' - ' + self.permissions1.user.username)

    def test_file_str(self):
        """assert user1 permissions"""
        self.assertEqual(str(self.file1), self.file1.name)

    def test_file_url(self):
        """assert user1 permissions"""
        self.assertEqual(self.file1.url(), self.file1.uploaded_file.url.split('?')[0])