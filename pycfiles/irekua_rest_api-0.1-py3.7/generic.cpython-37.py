# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/irekua_rest_api/permissions/generic.py
# Compiled at: 2019-10-27 19:02:52
# Size of source mod 2**32: 1294 bytes
from rest_framework.permissions import BasePermission
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import SAFE_METHODS

class ReadOnly(IsAuthenticated):

    def has_permission(self, request, view):
        is_auth = super().has_permission(request, view)
        if not is_auth:
            return False
        return request.method in SAFE_METHODS


class IsUnauthenticated(IsAuthenticated):

    def has_permission(self, request, view):
        return not super().has_permission(request, view)


class IsDeveloper(BasePermission):

    def has_permission(self, request, view):
        user = request.user
        return user.is_developer


class IsModel(BasePermission):

    def has_permission(self, request, view):
        user = request.user
        return user.is_model


class IsCurator(BasePermission):

    def has_permission(self, request, view):
        user = request.user
        return user.is_curator


class IsAdmin(BasePermission):

    def has_permission(self, request, view):
        user = request.user
        return user.is_superuser


class IsSpecialUser(BasePermission):

    def has_permission(self, request, view):
        user = request.user
        return user.is_superuser | user.is_curator | user.is_model | user.is_developer