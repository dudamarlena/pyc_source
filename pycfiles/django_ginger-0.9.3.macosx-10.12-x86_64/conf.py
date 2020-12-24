# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/shodh/Projects/django_ginger/ginger/staging/conf.py
# Compiled at: 2014-10-06 00:12:03
from django.conf import settings
STAGING_ALLOWED_HOSTS = None
STAGING_SECRET = None
STAGING_SESSION_KEY = 'staging-secret'
STAGING_TEMPLATE = 'staging/staging.html'

def reload_settings():
    global_vars = globals()
    for key in global_vars:
        if key.startswith('STAGING_'):
            if hasattr(settings, key):
                global_vars[key] = getattr(settings, key)


reload_settings()