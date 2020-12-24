# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/dev/dev/django-rest-framework-features/rest_framework_features/permissions.py
# Compiled at: 2019-10-04 10:43:00
# Size of source mod 2**32: 1019 bytes
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated
from . import schema

class CanAccessFeature(IsAuthenticated):

    def has_permission(self, request, view):
        if not super().has_permission(request, view):
            return False
        if request.user.is_superuser:
            return True
        method = request.method.lower()
        meta = getattr(view, schema.REGISTRY_ATTR_NAME)
        try:
            description = meta[method][0]
        except KeyError:
            return False
        else:
            for codename in get_codenames_from_description(description):
                if request.user.has_perm(f"rest_framework_features.{codename}"):
                    return True

            raise PermissionDenied(code=(description[(-1)]))


def get_codenames_from_description(description):
    return ['_'.join(description[:i]) for i in range(1, len(description) + 1)]


__all__ = ('CanAccessFeature', 'get_codenames_from_description')