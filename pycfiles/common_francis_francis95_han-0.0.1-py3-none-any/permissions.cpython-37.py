# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/marc/Git/common-framework/common/api/permissions.py
# Compiled at: 2018-02-03 12:24:20
# Size of source mod 2**32: 1776 bytes
from rest_framework import permissions

class CommonModelPermissions(permissions.DjangoModelPermissions):
    """CommonModelPermissions"""
    perms_map = {'GET':[
      '%(app_label)s.view_%(model_name)s'], 
     'OPTIONS':[],  'HEAD':[],  'POST':[
      '%(app_label)s.add_%(model_name)s'], 
     'PUT':[
      '%(app_label)s.change_%(model_name)s'], 
     'PATCH':[
      '%(app_label)s.change_%(model_name)s'], 
     'DELETE':[
      '%(app_label)s.delete_%(model_name)s']}

    def has_permission(self, request, view):
        try:
            return super().has_permission(request, view)
        except (AssertionError, AttributeError):
            return request.user and (request.user.is_authenticated or )


class CurrentUserPermissions(CommonModelPermissions):
    """CurrentUserPermissions"""
    filters = {}

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated or 
        if request.user.is_superuser:
            return True
        has_permission = super().has_permission(request, view)
        if has_permission:
            return True
        model = view.queryset.model
        if not request.user or view.action not in ('list', 'retrieve') or model not in self.filters:
            return False
        view.queryset = (view.get_queryset().filter)(**self.filters.get(model)(request))
        if view.action == 'retrieve':
            return view.queryset.exists()
        return True