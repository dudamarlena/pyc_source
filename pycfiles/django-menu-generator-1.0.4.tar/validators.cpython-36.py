# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/miltonln/Proyectos/django-menu-generator/menu_generator/validators.py
# Compiled at: 2018-01-31 09:25:36
# Size of source mod 2**32: 920 bytes


def is_superuser(request):
    """
    Returns True if request.user is superuser else returns False
    """
    return is_authenticated(request) and request.user.is_superuser


def is_staff(request):
    """
    Returns True if request.user is staff else returns False
    """
    return is_authenticated(request) and request.user.is_staff


def is_authenticated(request):
    """
    Returns True if request.user authenticated else returns False
    """
    return request.user.is_authenticated


def is_anonymous(request):
    """
    Returns True if request.user is not authenticated else returns False
    """
    return not request.user.is_authenticated


def user_has_permission(request, permission):
    """
    Returns True if request.user has the permission else returns False
    :param request: HttpRequest
    :param permission: Permission to be searched
    """
    return request.user.has_perm(permission)