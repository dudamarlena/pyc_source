# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jennyq/.pyenv/versions/venv_t12/lib/python3.7/site-packages/tendenci/apps/perms/decorators.py
# Compiled at: 2020-02-26 14:47:58
# Size of source mod 2**32: 4203 bytes
from functools import wraps
from django.conf import settings
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.utils.http import urlquote
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from tendenci.apps.base.http import Http403
from tendenci.apps.redirects.models import Redirect
from tendenci.apps.site_settings.utils import get_setting
from tendenci.apps.perms.utils import has_perm

class PageSecurityCheck(object):
    __doc__ = '\n        a decorator to check page security, and redirect accordingly\n    '

    def __init__(self, security_level):
        self.page_security_level = security_level.lower()

    def __call__(self, f):

        def check_security(request, *args, **kwargs):
            user_security_level = 'anonymous'
            if request.user.is_authenticated:
                if request.user.profile.is_superuser:
                    user_security_level = 'superuser'
                else:
                    if request.user.profile.is_staff:
                        user_security_level = 'staff'
                    else:
                        user_security_level = 'user'
            boo = False
            if self.page_security_level == 'anonymous':
                boo = True
            else:
                if self.page_security_level == 'user':
                    if user_security_level != 'anonymous':
                        boo = True
                    else:
                        if self.page_security_level == 'superuser':
                            if user_security_level == 'superuser':
                                boo = True
                        elif self.page_security_level == 'staff':
                            if user_security_level == 'staff':
                                boo = True
                elif boo:
                    return f(request, *args, **kwargs)
                    if request.user.is_authenticated:
                        raise Http403
                else:
                    redirect_field_name = REDIRECT_FIELD_NAME
                    login_url = settings.LOGIN_URL
                    path = urlquote(request.get_full_path())
                    tup = (login_url, redirect_field_name, path)
                    return HttpResponseRedirect('%s?%s=%s' % tup)

        return check_security


def is_enabled(*module_names):
    """
    Checks if module is enabled before
    returning view_method, else redirects to
    URL specified in "redirect" record.
    """

    def inner_render(fn):

        def wrapped(request, *args, **kwargs):
            for module_name in module_names:
                if not get_setting('module', module_name, 'enabled'):
                    r = get_object_or_404(Redirect, from_app=module_name)
                    return HttpResponseRedirect('/' + r.to_url)

            return fn(request, *args, **kwargs)

        return wraps(fn)(wrapped)

    return inner_render


def staff_with_perm(perm):
    """
    Checks if user is a staff and has the
    specified permission before returning
    method, else raises 403 exception.
    """

    def inner_render(fn):

        def wrapped(request, *args, **kwargs):
            if not request.user.profile.is_staff:
                raise Http403
            if not has_perm(request.user, perm):
                raise Http403
            return fn(request, *args, **kwargs)

        return wraps(fn)(wrapped)

    return inner_render


def admin_required(view_method):
    """
    Checks for admin permissions before
    returning method, else raises 403 exception.
    """

    def decorator(request, *args, **kwargs):
        admin = request.user.profile.is_superuser
        if not admin:
            raise Http403
        return view_method(request, *args, **kwargs)

    return decorator


def superuser_required(view_method):
    """
    Checks for superuser permissions before
    returning method, else raises 403 exception.
    """

    def decorator(request, *args, **kwargs):
        superuser = request.user.profile.is_superuser
        if not superuser:
            raise Http403
        return view_method(request, *args, **kwargs)

    return decorator