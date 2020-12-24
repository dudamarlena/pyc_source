# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/arroyo/ovp/gpa-ovp/django-ovp-users/ovp_users/tests/test_views/auth.py
# Compiled at: 2017-05-15 11:01:22
# Size of source mod 2**32: 756 bytes
from django.test import TestCase
from ovp_users.tests.helpers import authenticate
from ovp_users.tests.helpers import create_user
from ovp_users.tests.helpers import create_token

class JWTAuthTestCase(TestCase):

    def test_can_login(self):
        """Assert that it's possible to login"""
        user = create_user('test_can_login@test.com', 'validpassword')
        response = authenticate()
        self.assertTrue(response.data['token'] != None)

    def test_cant_login_wrong_password(self):
        """Assert that it's not possible to login with wrong password"""
        user = create_user('test_can_login@test.com', 'invalidpassword')
        response = authenticate()
        self.assertTrue(response.data['non_field_errors'][0] == 'Unable to login with provided credentials.')