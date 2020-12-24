# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ali/ownCloud/Project/python/django-aparnik-framework-project/testandbuildprojectframework/aparnik/contrib/users/api/permissions.py
# Compiled at: 2020-03-16 03:15:39
# Size of source mod 2**32: 447 bytes
from rest_framework import permissions
from rest_framework.permissions import SAFE_METHODS

class IsAdminPermission(permissions.BasePermission):
    __doc__ = '\n    Object-level permission to only allow owners of an object to edit it.\n    Assumes the model instance has an `owner` attribute.\n    '

    def has_object_permission(self, request, view, obj):
        if request.user:
            if request.user.is_admin:
                return True
        return False