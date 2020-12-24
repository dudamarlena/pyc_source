# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ramusus/workspace/manufacture/env/src/django-oauth-tokens/oauth_tokens/factories.py
# Compiled at: 2015-01-25 03:14:29
from datetime import timedelta
from django.utils import timezone
import factory
from .models import AccessToken, UserCredentials

class UserCredentialsFactory(factory.DjangoModelFactory):
    FACTORY_FOR = UserCredentials
    active = True


class AccessTokenFactory(factory.DjangoModelFactory):
    FACTORY_FOR = AccessToken
    user_credentials = factory.SubFactory(UserCredentialsFactory)
    expires_at = timezone.now() + timedelta(1)