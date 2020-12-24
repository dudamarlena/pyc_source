# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-intel/egg/filebrowser/decorators.py
# Compiled at: 2014-11-22 02:35:13
from django.contrib.sessions.models import Session
from django.shortcuts import get_object_or_404, render_to_response
from django.contrib.auth.models import User
from django.template import RequestContext
from django.conf import settings

def flash_login_required(function):
    """
    Decorator to recognize a user  by its session.
    Used for Flash-Uploading.
    """

    def decorator(request, *args, **kwargs):
        try:
            engine = __import__(settings.SESSION_ENGINE, {}, {}, [''])
        except:
            import django.contrib.sessions.backends.db
            engine = django.contrib.sessions.backends.db

        session_data = engine.SessionStore(request.POST.get('session_key'))
        user_id = session_data['_auth_user_id']
        request.user = get_object_or_404(User, pk=user_id)
        return function(request, *args, **kwargs)

    return decorator