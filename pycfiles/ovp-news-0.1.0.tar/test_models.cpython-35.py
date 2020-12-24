# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/arroyo/ovp/suzano-ovp/django-ovp-users/ovp_users/tests/test_models.py
# Compiled at: 2017-02-22 17:56:49
# Size of source mod 2**32: 1562 bytes
from django.test import TestCase
from ovp_users.models import User

class TestUserManager(TestCase):

    def test_create_user_without_email(self):
        """ Assert that UserManager doesn't create users without email"""
        with self.assertRaises(ValueError) as (context):
            User.objects.create_user(None, 'validpassword')
        self.assertTrue('The given email address must be set.' == str(context.exception))

    def test_create_user(self):
        """ Assert that UserManager can create user"""
        user = User.objects.create_user('test_create_user@test.com', 'validpassword')
        self.assertTrue(user.id > 0)

    def test_create_superuser(self):
        """ Assert that UserManager can create super user"""
        user = User.objects.create_superuser('test_create_superuser@test.com', 'validpassword')
        self.assertTrue(user.id > 0)


class TestUserModel(TestCase):

    def test_short_name(self):
        """ Assert that get_short_name returns name"""
        user = User.objects.create_user('test_short_name@test.com', 'validpassword')
        user.name = 'Abc def'
        user.save()
        self.assertTrue(user.get_short_name() == user.name)

    def test_password_hashing(self):
        """ Assert password is not rehashed during saves """
        user = User.objects.create_user('user@email.com', 'validpassword')
        user.save()
        self.assertTrue(user.check_password('validpassword'))
        user.set_password('anotherpassword')
        self.assertTrue(user.check_password('anotherpassword'))
        user.save()
        self.assertTrue(user.check_password('anotherpassword'))