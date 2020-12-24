# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: django_mojeid_connect/tests/test_views.py
# Compiled at: 2018-07-09 09:57:02
"""Unittests for views."""
from __future__ import unicode_literals
from django.contrib import auth
from django.test import TestCase, override_settings

@override_settings(ROOT_URLCONF=b'django_mojeid_connect.urls', MIDDLEWARE=[
 b'django.contrib.sessions.middleware.SessionMiddleware'])
class TestCreateUser(TestCase):
    """Unittests for CreateUser helper view."""

    def test_post(self):
        response = self.client.post(b'/create_user/', {b'username': b'test'})
        self.assertRedirects(response, b'/oidc/authenticate/', fetch_redirect_response=False)
        user = auth.get_user(self.client)
        self.assertTrue(user.is_authenticated)
        self.assertEqual(user.username, b'test')