# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/tomeu/workspace/wdna/django-object-authority/django_object_authority/options.py
# Compiled at: 2017-06-02 03:02:30
# Size of source mod 2**32: 861 bytes
from . import settings
from .utils import get_full_permission_codename

class BaseObjectAuthorization(object):

    def has_object_permission(self, user, obj):
        return settings.AUTHORIZE_BY_DEFAULT


class BaseUserObjectAuthorization(BaseObjectAuthorization):

    def has_add_permission(self, user, obj):
        return self._has_permission(user, 'add', obj)

    def has_change_permission(self, user, obj):
        return self._has_permission(user, 'change', obj)

    def has_delete_permission(self, user, obj):
        return self._has_permission(user, 'delete', obj)

    def has_view_permission(self, user, obj):
        return self._has_permission(user, 'view', obj)

    def _has_permission(self, user, action, obj):
        permission_codename = get_full_permission_codename(action, obj._meta)
        return user.has_perm(permission_codename)