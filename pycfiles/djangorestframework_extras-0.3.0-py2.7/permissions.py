# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/rest_framework_extras/users/permissions.py
# Compiled at: 2016-10-26 05:12:13
from rest_framework.permissions import DjangoObjectPermissions

class UserPermissions(DjangoObjectPermissions):

    def has_permission(self, request, view):
        return view.action in ('retrieve', 'update', 'partial_update') or request.user.is_staff

    def has_object_permission(self, request, view, obj):
        user = request.user
        if user.is_superuser:
            return True
        if user.pk == obj.pk:
            return True
        if not user.is_staff:
            return False
        return super(UserPermissions, self).has_object_permission(request, view, obj)