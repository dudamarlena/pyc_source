# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/reviewboard/accounts/tests/test_standard_auth_backend.py
# Compiled at: 2020-02-11 04:03:56
"""Unit tests for StandardAuthBackend."""
from __future__ import unicode_literals
from django.contrib.auth.models import User
from djblets.testing.decorators import add_fixtures
from reviewboard.accounts.backends import StandardAuthBackend, get_enabled_auth_backends
from reviewboard.testing import TestCase

class StandardAuthBackendTests(TestCase):
    """Unit tests for StandardAuthBackend."""

    def _get_standard_auth_backend(self):
        backend = None
        for backend in get_enabled_auth_backends():
            if type(backend) is StandardAuthBackend:
                break

        self.assertIs(type(backend), StandardAuthBackend)
        return backend

    @add_fixtures([b'test_users'])
    def test_get_or_create_user_exists(self):
        """Testing StandardAuthBackend.get_or_create_user when the requested
        user already exists
        """
        original_count = User.objects.count()
        user = User.objects.get(username=b'doc')
        backend = self._get_standard_auth_backend()
        result = backend.get_or_create_user(b'doc', None)
        self.assertEqual(original_count, User.objects.count())
        self.assertEqual(user, result)
        return

    def test_get_or_create_user_new(self):
        """Testing StandardAuthBackend.get_or_create_user when the requested
        user does not exist
        """
        backend = self._get_standard_auth_backend()
        self.assertIsInstance(backend, StandardAuthBackend)
        user = backend.get_or_create_user(b'doc', None)
        self.assertIsNone(user)
        return

    @add_fixtures([b'test_users'])
    def test_get_user_exists(self):
        """Testing StandardAuthBackend.get_user when the requested user already
        exists
        """
        user = User.objects.get(username=b'doc')
        backend = self._get_standard_auth_backend()
        result = backend.get_user(user.pk)
        self.assertEqual(user, result)

    def test_get_user_not_exists(self):
        """Testing StandardAuthBackend.get_user when the requested user does
        not exist
        """
        backend = self._get_standard_auth_backend()
        result = backend.get_user(1)
        self.assertIsNone(result)