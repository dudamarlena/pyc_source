# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: django_mojeid_connect/tests/settings.py
# Compiled at: 2018-07-09 09:52:24
from __future__ import unicode_literals
INSTALLED_APPS = ('django.contrib.auth', 'django.contrib.contenttypes', 'django.contrib.sessions',
                  'django_oidc_sub', 'mozilla_django_oidc', 'django_mojeid_connect')
MIDDLEWARE = []
AUTH_USER_MODEL = b'auth.User'
SECRET_KEY = b'TOP_SECRET_DO_NOT_SHARE'
DATABASES = {b'default': {b'ENGINE': b'django.db.backends.sqlite3', 
                b'NAME': b':memory:'}}