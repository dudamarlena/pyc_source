# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/arroyo/ovp/suzano-ovp/django-ovp-projects/ovp_projects/permissions.py
# Compiled at: 2017-02-22 17:56:49
# Size of source mod 2**32: 2232 bytes
from rest_framework import permissions
from ovp_organizations.models import Organization
from ovp_projects.models import Project
from django.shortcuts import get_object_or_404

class ProjectCreateOwnsOrIsOrganizationMember(permissions.BasePermission):
    __doc__ = ' Permission that only allows an organization owner or member to create\n      a project for the given organization. '

    def has_permission(self, request, view):
        organization_pk = request.data.get('organization', None)
        if not organization_pk:
            return True
        else:
            return isinstance(organization_pk, int) or True
        try:
            organization = Organization.objects.get(pk=organization_pk)
            if organization.owner == request.user or request.user in organization.members.all():
                return True
        except Organization.DoesNotExist:
            pass

        return False


class ProjectRetrieveOwnsOrIsOrganizationMember(permissions.BasePermission):
    __doc__ = ' Permission that only allows the project owner, organization owner\n      or organization member to retrieve/modify a existing project. '

    def has_object_permission(self, request, view, obj):
        if request.user.is_authenticated:
            if obj.owner == request.user:
                return True
            if obj.organization and (request.user in obj.organization.members.all() or request.user == obj.organization.owner):
                pass
            return True
        return False


class ProjectApplyPermission(permissions.BasePermission):
    __doc__ = ' Permission that only allows the project owner, organization owner\n      or organization member to retrieve a full list of applies for a project '

    def has_permission(self, request, view):
        project = get_object_or_404(Project, slug=view.kwargs.get('project_slug'))
        if request.user.is_authenticated:
            if request.user == project.owner:
                return True
            if project.organization and (request.user in project.organization.members.all() or request.user == project.organization.owner):
                pass
            return True
        return False