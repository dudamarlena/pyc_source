# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/mass/PythonProjects/oideas/oideas_backend/accounts/tests/tests_authentication.py
# Compiled at: 2015-08-17 02:31:54
from django.test import TestCase
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
User = get_user_model()

class AuthenticationTest(TestCase):

    def test_can_authenticate_with_username(self):
        username = 'a@b.com'
        password = 'secret!'
        User.objects.create_user(username=username, password=password)
        user = authenticate(username=username, password=password)
        self.assertIsNotNone(user)

    def test_can_authenticate_with_email(self):
        email = 'a@b.com'
        password = 'secret!'
        User.objects.create_user(username='Cool name!', email=email, password=password)
        user = authenticate(email=email, password=password)
        self.assertIsNotNone(user)