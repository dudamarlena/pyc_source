# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/mass/PythonProjects/robin/robin/accounts/tests/tests_authentication.py
# Compiled at: 2015-10-05 13:17:49
# Size of source mod 2**32: 756 bytes
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