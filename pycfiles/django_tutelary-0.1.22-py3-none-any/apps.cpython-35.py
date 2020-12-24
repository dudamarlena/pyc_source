# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Volumes/Work/dev/cadasta/django-tutelary/tutelary/apps.py
# Compiled at: 2017-12-04 06:48:52
# Size of source mod 2**32: 519 bytes
from django.apps import AppConfig
from django.apps import apps as django_apps
from django.conf import settings

class TutelaryConfig(AppConfig):
    name = 'tutelary'

    def ready(self):
        user_model = django_apps.get_model(settings.AUTH_USER_MODEL)
        if not hasattr(user_model, 'assign_policies'):
            from .models import assign_user_policies, user_assigned_policies
            user_model.assign_policies = assign_user_policies
            user_model.assigned_policies = user_assigned_policies