# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/filipeximenes/Projects/django-role-permissions/rolepermissions/mixins.py
# Compiled at: 2018-12-02 07:23:05
# Size of source mod 2**32: 865 bytes
from __future__ import unicode_literals
from rolepermissions.decorators import has_permission_decorator, has_role_decorator

class HasRoleMixin(object):
    allowed_roles = []
    redirect_to_login = None

    def dispatch(self, request, *args, **kwargs):
        roles = self.allowed_roles
        return (has_role_decorator(roles, redirect_to_login=(self.redirect_to_login))(super(HasRoleMixin, self).dispatch))(
 request, *args, **kwargs)


class HasPermissionsMixin(object):
    required_permission = ''
    redirect_to_login = None

    def dispatch(self, request, *args, **kwargs):
        permission = self.required_permission
        return (has_permission_decorator(permission, redirect_to_login=(self.redirect_to_login))(super(HasPermissionsMixin, self).dispatch))(
 request, *args, **kwargs)