# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/filipeximenes/Projects/django-role-permissions/rolepermissions/decorators.py
# Compiled at: 2018-12-02 07:23:05
# Size of source mod 2**32: 1808 bytes
from __future__ import unicode_literals
from functools import wraps
from django.conf import settings
from django.contrib.auth.views import redirect_to_login as dj_redirect_to_login
from django.core.exceptions import PermissionDenied
from rolepermissions.checkers import has_role, has_permission
from rolepermissions.utils import user_is_authenticated

def has_role_decorator(role, redirect_to_login=None):

    def request_decorator(dispatch):

        @wraps(dispatch)
        def wrapper(request, *args, **kwargs):
            user = request.user
            if user_is_authenticated(user):
                if has_role(user, role):
                    return dispatch(request, *args, **kwargs)
            redirect = redirect_to_login
            if redirect is None:
                redirect = getattr(settings, 'ROLEPERMISSIONS_REDIRECT_TO_LOGIN', False)
            if redirect:
                return dj_redirect_to_login(request.get_full_path())
            raise PermissionDenied

        return wrapper

    return request_decorator


def has_permission_decorator(permission_name, redirect_to_login=None):

    def request_decorator(dispatch):

        @wraps(dispatch)
        def wrapper(request, *args, **kwargs):
            user = request.user
            if user_is_authenticated(user):
                if has_permission(user, permission_name):
                    return dispatch(request, *args, **kwargs)
            redirect = redirect_to_login
            if redirect is None:
                redirect = getattr(settings, 'ROLEPERMISSIONS_REDIRECT_TO_LOGIN', False)
            if redirect:
                return dj_redirect_to_login(request.get_full_path())
            raise PermissionDenied

        return wrapper

    return request_decorator