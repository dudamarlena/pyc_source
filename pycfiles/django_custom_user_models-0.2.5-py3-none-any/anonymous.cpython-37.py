# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: M:\Programming\Project\django-auth\auth\CustomAuth\decorators\anonymous.py
# Compiled at: 2019-12-10 17:11:23
# Size of source mod 2**32: 583 bytes
from django.contrib.auth.decorators import user_passes_test
from django.conf import settings

def anonymous_required(function=None, redirect_url=None):
    """
    The way to use this decorator is:
        @anonymous_required
        def my_view(request, pk)
        ...
    """
    if not redirect_url:
        redirect_url = settings.LOGIN_REDIRECT_URL
    actual_decorator = user_passes_test((lambda u: u.is_anonymous()),
      login_url=redirect_url)
    if function:
        return actual_decorator(function)
    return actual_decorator