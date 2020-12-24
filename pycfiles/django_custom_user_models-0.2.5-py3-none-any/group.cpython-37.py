# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: M:\Programming\Project\django-auth\auth\CustomAuth\decorators\group.py
# Compiled at: 2019-12-10 17:11:23
# Size of source mod 2**32: 945 bytes
from django.contrib.auth.decorators import user_passes_test
from django.conf import settings

def group_required(*group_names, redirect_url=None):
    """
    Requires user membership in at least one of the groups passed in.
    The way to use this decorator is:
        @group_required(‘admins’, ‘seller’)
        def my_view(request, pk)
        ...
    """
    if not redirect_url:
        redirect_url = settings.LOGIN_REDIRECT_URL

    def in_groups(user):
        if user.is_authenticated:
            if bool(user.groups.filter(name__in=group_names)) | user.is_superuser:
                return True
        return False

    actual_decorator = user_passes_test(in_groups,
      login_url=redirect_url)
    return actual_decorator