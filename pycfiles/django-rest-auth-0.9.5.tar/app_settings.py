# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/mario/work/django-rest-auth/rest_auth/registration/app_settings.py
# Compiled at: 2017-10-02 15:35:16
from django.conf import settings
from rest_framework.permissions import AllowAny
from rest_auth.registration.serializers import RegisterSerializer as DefaultRegisterSerializer
from ..utils import import_callable
serializers = getattr(settings, 'REST_AUTH_REGISTER_SERIALIZERS', {})
RegisterSerializer = import_callable(serializers.get('REGISTER_SERIALIZER', DefaultRegisterSerializer))

def register_permission_classes():
    permission_classes = [
     AllowAny]
    for klass in getattr(settings, 'REST_AUTH_REGISTER_PERMISSION_CLASSES', tuple()):
        permission_classes.append(import_callable(klass))

    return tuple(permission_classes)