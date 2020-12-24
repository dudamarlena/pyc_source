# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/arroyo/ovp/atadosovp/django-ovp-users/ovp_users/tests/test_managers.py
# Compiled at: 2016-10-13 16:37:30
# Size of source mod 2**32: 854 bytes
from django.test import TestCase
from ovp_users.models import User

class TestUserManager(TestCase):

    def test_create_user_without_email(self):
        """Assert that UserManager doesn't create users without email"""
        with self.assertRaises(ValueError) as (context):
            User.objects.create_user(None, 'validpassword')
        self.assertTrue('The given email address must be set.' == str(context.exception))

    def test_create_user(self):
        """Assert that UserManager can create user"""
        user = User.objects.create_user('test_create_user@test.com', 'validpassword')
        self.assertTrue(user.id > 0)

    def test_create_superuser(self):
        """Assert that UserManager can create super user"""
        user = User.objects.create_superuser('test_create_superuser@test.com', 'validpassword')
        self.assertTrue(user.id > 0)