# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/arroyo/ovp/atadosovp/django-ovp-users/ovp_users/permissions.py
# Compiled at: 2016-10-14 21:26:58
# Size of source mod 2**32: 535 bytes
from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
    __doc__ = '\n  Custom permission to only allow Owner of an object to edit it.\n  '

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_staff or obj.user == request.user