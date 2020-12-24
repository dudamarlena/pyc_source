# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: M:\Programming\Project\django-auth\auth\CustomAuth\apps.py
# Compiled at: 2019-12-09 12:37:18
# Size of source mod 2**32: 1257 bytes
from django.apps import AppConfig
from django.core import checks
from django.db.models.query_utils import DeferredAttribute
from django.db.models.signals import post_migrate
import django.utils.translation as _
from django.contrib.auth import get_user_model
from django.contrib.auth.checks import check_models_permissions, check_user_model
from django.contrib.auth.management import create_permissions
from django.contrib.auth.signals import user_logged_in

class CustomAuthConfig(AppConfig):
    name = 'CustomAuth'
    verbose_name = _('Custom Authentication')

    def ready(self):
        post_migrate.connect(create_permissions,
          dispatch_uid='django.contrib.auth.management.create_permissions')
        last_login_field = getattr(get_user_model(), 'last_login', None)
        if isinstance(last_login_field, DeferredAttribute):
            from .models import update_last_login
            user_logged_in.connect(update_last_login, dispatch_uid='update_last_login')
        checks.register(check_user_model, checks.Tags.models)
        checks.register(check_models_permissions, checks.Tags.models)