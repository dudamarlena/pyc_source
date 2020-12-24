# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.15-x86_64/egg/tests/tests/test_03_user_autologin.py
# Compiled at: 2020-04-15 11:39:00
# Size of source mod 2**32: 810 bytes
from __future__ import annotations
from unittest import mock
from django_selenium_test import IntegrationTest

class ExampleIntegrationTest(IntegrationTest):
    user = 'alice'

    def setUp(self):
        from django.contrib.auth.hashers import make_password
        from django.contrib.auth.models import User
        alice = User.objects.create(username='alice',
          password=(make_password('topsecret')),
          is_active=True)
        super().setUp()

    def test_auto_login(self):
        """ Checks that the user was actually logged in """
        element = self.load_live_url('core', selector='#user')
        self.assertEqual(element.text, 'The logged on user is alice.')
        self.assertIsNone(self.user.last_login)