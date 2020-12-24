# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/mario/work/django-rest-auth/rest_auth/models.py
# Compiled at: 2017-08-26 14:01:07
from django.conf import settings
from rest_framework.authtoken.models import Token as DefaultTokenModel
from .utils import import_callable
TokenModel = import_callable(getattr(settings, 'REST_AUTH_TOKEN_MODEL', DefaultTokenModel))