# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/simon/Dropbox/Projects/django-rest-utils/rest_utils/tests.py
# Compiled at: 2013-12-13 09:24:32
# Size of source mod 2**32: 1155 bytes
from mock import Mock
from django.http import Http404
from django_nose import FastFixtureTestCase as TestCase
from .permissions import DenyCreateOnPutPermission, NotAuthenticatedPermission

class PermissionsTest(TestCase):

    def test_deny_create_on_put_permission(self):
        permission = DenyCreateOnPutPermission()
        view = Mock()
        request = Mock()
        request.method = 'GET'
        self.assertTrue(permission.has_permission(request, view))
        request.method = 'PUT'
        self.assertTrue(permission.has_permission(request, view))
        request.method = 'PUT'
        view.get_object = Mock(side_effect=Http404)
        self.assertFalse(permission.has_permission(request, view))

    def test_not_authenticated_permission(self):
        permission = NotAuthenticatedPermission()
        view = Mock()
        request = Mock()
        request.user.is_authenticated = Mock(return_value=True)
        self.assertFalse(permission.has_permission(request, view))
        request.user.is_authenticated = Mock(return_value=False)
        self.assertTrue(permission.has_permission(request, view))