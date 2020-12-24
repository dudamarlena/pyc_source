# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/syfilebrowser/decorators.py
# Compiled at: 2016-04-18 13:42:40
from __future__ import unicode_literals
from django.shortcuts import get_object_or_404
from django.conf import settings
from shuyucms.utils.models import get_user_model

def flash_login_required(function):
    """
    Decorator to recognize a user by its session.
    Used for Flash-Uploading.
    """

    def decorator(request, *args, **kwargs):
        try:
            engine = __import__(settings.SESSION_ENGINE, {}, {}, [b''])
        except:
            import django.contrib.sessions.backends.db
            engine = django.contrib.sessions.backends.db

        session_data = engine.SessionStore(request.POST.get(b'session_key'))
        user_id = session_data[b'_auth_user_id']
        request.user = get_object_or_404(get_user_model(), pk=user_id)
        return function(request, *args, **kwargs)

    return decorator