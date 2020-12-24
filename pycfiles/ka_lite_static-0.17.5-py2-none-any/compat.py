# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-jkXn_D/django-tastypie-legacy/tastypie/compat.py
# Compiled at: 2018-07-11 18:15:32
from __future__ import unicode_literals
import django
from django.conf import settings
__all__ = [
 b'get_user_model', b'get_username_field', b'AUTH_USER_MODEL']
AUTH_USER_MODEL = getattr(settings, b'AUTH_USER_MODEL', b'auth.User')
if django.VERSION >= (1, 5):

    def get_user_model():
        from django.contrib.auth import get_user_model as django_get_user_model
        return django_get_user_model()


    def get_username_field():
        return get_user_model().USERNAME_FIELD


else:

    def get_user_model():
        from django.contrib.auth.models import User
        return User


    def get_username_field():
        return b'username'


def get_module_name(meta):
    return getattr(meta, b'model_name', None) or getattr(meta, b'module_name')


atomic_decorator = getattr(django.db.transaction, b'atomic', None) or getattr(django.db.transaction, b'commit_on_success')