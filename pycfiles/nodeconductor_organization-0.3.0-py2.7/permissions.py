# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/nodeconductor_organization/permissions.py
# Compiled at: 2016-09-25 10:50:25
from __future__ import unicode_literals
from rest_framework.permissions import BasePermission, SAFE_METHODS

class OrganizationUserPermissions(BasePermission):
    """
    Allows full access to admin users and organization customer owners.
    User can remove his organization user only when it is not approved.
    """

    def has_permission(self, request, view):
        user = request.user
        if not user.is_staff and request.method == b'DELETE':
            organization_user = view.get_object()
            if not organization_user.is_approved:
                return True
            return organization_user.can_be_managed_by(user)
        return True