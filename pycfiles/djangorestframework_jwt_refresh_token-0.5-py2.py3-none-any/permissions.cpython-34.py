# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/nicolas/src/django-rest-framework-jwt-refresh-token/refreshtoken/permissions.py
# Compiled at: 2016-01-28 09:27:04
# Size of source mod 2**32: 662 bytes
from rest_framework import permissions

class IsOwnerOrAdmin(permissions.BasePermission):
    __doc__ = '\n    Only admins or owners can have permission\n    '

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated()

    def has_object_permission(self, request, view, obj):
        """
        If user is staff or superuser or 'owner' of object return True
        Else return false.
        """
        if not request.user.is_authenticated():
            return False
        else:
            if request.user.is_staff or request.user.is_superuser:
                return True
            return request.user == obj.user