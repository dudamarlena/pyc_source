# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: M:\Programming\Project\django-auth\auth\CustomAuth\decorators\superuser.py
# Compiled at: 2019-12-10 17:11:23
# Size of source mod 2**32: 322 bytes
from django.core.exceptions import PermissionDenied

def superuser_only(function):
    """Limit view to superusers only."""

    def wrap(request, *args, **kwargs):
        if not request.user.is_superuser:
            raise PermissionDenied
        return function(request, *args, **kwargs)

    return wrap