# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/eliotberriot/Seafile/kii/kii_main/kii/user/views.py
# Compiled at: 2015-01-18 07:28:37
from django.contrib.auth import views
from django.contrib import messages
from kii.stream.models import Stream

def login(request, **kwargs):
    r = views.login(request, **kwargs)
    if request.user.is_authenticated():
        if not request.session.get('default_stream'):
            request.session['selected_stream'] = Stream.objects.get_user_stream(request.user).pk
        messages.success(request, 'user.login.success')
    return r


def logout(request, **kwargs):
    return views.logout(request, **kwargs)