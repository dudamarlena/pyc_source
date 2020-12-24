# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ramzi/drf-social-auth/drf_social/helpers.py
# Compiled at: 2020-03-05 05:12:00
# Size of source mod 2**32: 803 bytes
import json
import django.conf as conf
from drf_social.models import AuthProvider, Providers

def extract_scopes(scopes):
    try:
        scopes = json.loads(scopes)
        return scopes
    except json.JSONDecodeError:
        raise ValueError('Invalid extras were provided, must be json encoded')


AUTH_MAPPING = {Providers.GOOGLE: 'GOOGLE_OAUTH2', 
 Providers.FACEBOOK: 'FACEBOOK'}

def load_providers():
    all_auth = AuthProvider.objects.all()
    for auth in all_auth:
        setattr(conf.settings, f"SOCIAL_AUTH_{AUTH_MAPPING[auth.provider]}_KEY", auth.client_id)
        setattr(conf.settings, f"SOCIAL_AUTH_{AUTH_MAPPING[auth.provider]}_SECRET", auth.client_secret)
        setattr(conf.settings, f"SOCIAL_AUTH_{AUTH_MAPPING[auth.provider]}_SCOPE", extract_scopes(auth.scopes))