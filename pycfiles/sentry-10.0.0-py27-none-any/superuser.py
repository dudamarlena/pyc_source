# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/src/sentry/src/sentry/receivers/superuser.py
# Compiled at: 2019-08-16 17:27:45
from __future__ import absolute_import
from django.contrib.auth.signals import user_logged_in, user_logged_out

def enable_superuser(request, user, **kwargs):
    su = getattr(request, 'superuser', None)
    if su:
        if user.is_superuser:
            su.set_logged_in(user)
        else:
            su._set_logged_out()
    return


def disable_superuser(request, user, **kwargs):
    su = getattr(request, 'superuser', None)
    if su:
        su.set_logged_out()
    return


user_logged_in.connect(enable_superuser, dispatch_uid='enable_superuser', weak=False)
user_logged_out.connect(disable_superuser, dispatch_uid='disable_superuser', weak=False)