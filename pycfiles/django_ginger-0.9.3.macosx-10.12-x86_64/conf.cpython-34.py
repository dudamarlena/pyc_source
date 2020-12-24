# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/shodh/Projects/django_ginger/ginger/contrib/staging/conf.py
# Compiled at: 2015-11-11 23:55:49
# Size of source mod 2**32: 305 bytes
from django.conf import settings
ALLOWED_HOSTS = None
SECRET = 'sim-sim'
SESSION_KEY = 'staging-secret'
TEMPLATE = 'staging/staging.html'
RESET_URL = 'staging/reset/'

def get(key):
    try:
        return getattr(settings, 'STAGING_' + key)
    except AttributeError:
        return globals()[key]