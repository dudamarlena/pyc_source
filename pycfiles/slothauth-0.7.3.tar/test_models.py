# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/chris/workspace/slothauth/slothauth/tests/test_models.py
# Compiled at: 2016-02-01 18:16:07
from django.core import mail
from django.test import TestCase
from ..factories import AccountFactory, PasswordlessAccountFactory

class AccountModelTest(TestCase):

    def test_send_passwordless_login_email(self):
        account = AccountFactory()
        account.set_password('password')
        account.save()
        account.send_passwordless_login_email()
        self.assertEqual(len(mail.outbox), 0)
        passwordless_account = PasswordlessAccountFactory()
        self.assertTrue(passwordless_account.is_passwordless)
        passwordless_account.send_passwordless_login_email()
        self.assertEqual(len(mail.outbox), 1)