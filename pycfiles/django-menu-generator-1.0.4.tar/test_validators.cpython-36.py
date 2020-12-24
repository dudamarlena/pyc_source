# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/miltonln/Proyectos/django-menu-generator/menu_generator/tests/test_validators.py
# Compiled at: 2018-01-31 09:25:36
# Size of source mod 2**32: 1224 bytes
from django.http import HttpRequest
from django.test import TestCase
from .utils import TestUser
from ..validators import is_superuser, is_staff, is_authenticated, is_anonymous, user_has_permission

class ValidatorsTestCase(TestCase):
    __doc__ = '\n    Validators test\n    '

    def setUp(self):
        """
        Setup the test.
        """
        self.request = HttpRequest()
        self.request.path = '/'

    def test_is_superuser(self):
        self.request.user = TestUser(authenticated=True, superuser=True)
        self.assertTrue(is_superuser(self.request))

    def test_is_staff(self):
        self.request.user = TestUser(authenticated=True, staff=True)
        self.assertTrue(is_staff(self.request))

    def test_is_authenticated(self):
        self.request.user = TestUser(authenticated=True)
        self.assertTrue(is_authenticated(self.request))

    def test_is_anonymous(self):
        self.request.user = TestUser()
        self.assertTrue(is_anonymous(self.request))

    def test_user_has_permission(self):
        self.request.user = TestUser(authenticated=True)
        self.request.user.add_perm('test_permission')
        self.assertTrue(user_has_permission(self.request, 'test_permission'))