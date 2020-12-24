# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/tomas/Git/django-mojeid-connect/django_mojeid_connect/tests/settings.py
# Compiled at: 2018-07-09 09:52:24
# Size of source mod 2**32: 438 bytes
from __future__ import unicode_literals
INSTALLED_APPS = ('django.contrib.auth', 'django.contrib.contenttypes', 'django.contrib.sessions',
                  'django_oidc_sub', 'mozilla_django_oidc', 'django_mojeid_connect')
MIDDLEWARE = []
AUTH_USER_MODEL = 'auth.User'
SECRET_KEY = 'TOP_SECRET_DO_NOT_SHARE'
DATABASES = {'default': {'ENGINE': 'django.db.backends.sqlite3', 
             'NAME': ':memory:'}}