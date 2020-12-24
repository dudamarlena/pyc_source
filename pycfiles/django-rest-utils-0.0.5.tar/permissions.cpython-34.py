# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/simon/Dropbox/Projects/django-rest-utils/rest_utils/permissions.py
# Compiled at: 2013-11-04 03:05:44
# Size of source mod 2**32: 689 bytes
from django.http import Http404
from rest_framework import permissions

class DenyCreateOnPutPermission(permissions.BasePermission):
    __doc__ = '\n    Prevent creating object on PUT\n    '

    def has_permission(self, request, view):
        if request.method == 'PUT':
            try:
                view.get_object()
            except Http404:
                return False

        return True


class NotAuthenticatedPermission(permissions.BasePermission):
    __doc__ = '\n    Deny access to authenticated users.\n    '

    def has_permission(self, request, view):
        if request.user and request.user.is_authenticated():
            return False
        return True