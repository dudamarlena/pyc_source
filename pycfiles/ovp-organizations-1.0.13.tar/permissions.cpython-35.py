# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/arroyo/ovp/suzano-ovp/django-ovp-organizations/ovp_organizations/permissions.py
# Compiled at: 2017-02-22 17:56:49
# Size of source mod 2**32: 1498 bytes
from rest_framework import permissions
from rest_framework import exceptions
from ovp_organizations.models import Organization, OrganizationInvite

class OwnsOrIsOrganizationMember(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.user.is_authenticated:
            if obj.owner == request.user:
                return True
            if request.user in obj.members.all():
                return True
            raise exceptions.PermissionDenied()
        return False


class OwnsOrganization(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.user.is_authenticated:
            if obj.owner == request.user:
                return True
            raise exceptions.PermissionDenied()
        return False


class IsOrganizationMember(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.user.is_authenticated:
            if request.user in obj.members.all():
                return True
            raise exceptions.PermissionDenied()
        return False


class IsInvitedToOrganization(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.user.is_authenticated:
            try:
                OrganizationInvite.objects.get(invited=request.user, organization=obj)
                return True
            except OrganizationInvite.DoesNotExist:
                raise exceptions.PermissionDenied()

            return False