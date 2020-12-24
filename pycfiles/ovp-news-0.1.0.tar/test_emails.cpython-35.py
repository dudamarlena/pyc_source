# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/arroyo/ovp/suzano-ovp/django-ovp-users/ovp_users/tests/test_emails.py
# Compiled at: 2017-02-22 17:56:49
# Size of source mod 2**32: 1009 bytes
from django.test import TestCase
from django.core import mail
from ovp_users.models import User, PasswordRecoveryToken

class TestEmailTriggers(TestCase):

    def test_user_creation_trigger_email(self):
        """Assert that email is triggered when creating an user"""
        user = User(email='a@b.c', password='validpassword', name='valid name')
        user.save()
        self.assertTrue(len(mail.outbox) > 0)

    def test_token_creation_trigger_email(self):
        """Assert that email is triggered when password recovery token is created"""
        user = User(email='d@e.f', password='validpassword', name='valid name')
        user.save()
        token = PasswordRecoveryToken(user=user)
        token.save()
        self.assertTrue(len(mail.outbox) >= 2)

    def test_async_email_works(self):
        """Assert that async emails are triggered by testing user creation"""
        user = User(email='a@b.c', password='validpassword', name='valid name')
        user.mailing(async_mail=True).sendWelcome().join()
        self.assertTrue(len(mail.outbox) > 0)