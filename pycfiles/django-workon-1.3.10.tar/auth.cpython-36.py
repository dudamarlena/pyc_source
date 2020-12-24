# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/dalou/www/LEPOLE/workon/utils/auth.py
# Compiled at: 2018-01-04 09:37:52
# Size of source mod 2**32: 910 bytes
from django.conf import settings
from django.contrib import auth
from django.contrib.auth import get_user_model
from django.utils import timezone
import workon.utils
__all__ = [
 'authenticate_user']

def authenticate_user(request, user, remember=True, backend=None, expiry=315360000):
    if user:
        if not hasattr(user, 'backend'):
            if backend:
                user.backend = backend
            elif hasattr(settings, 'AUTHENTICATION_BACKENDS'):
                if len(settings.AUTHENTICATION_BACKENDS):
                    user.backend = settings.AUTHENTICATION_BACKENDS[0]
            else:
                user.backend = 'django.contrib.auth.backends.ModelBackend'
        if request.user.is_authenticated:
            auth.logout(request)
        auth.login(request, user)
        request.session.set_expiry(expiry if remember else 0)
        return True
    else:
        return False