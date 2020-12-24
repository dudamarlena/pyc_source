# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/simple_autocomplete/tests/settings/111.py
# Compiled at: 2017-09-18 04:36:19
import os
DEBUG = True
TEMPLATE_DEBUG = DEBUG
DATABASES = {'default': {'ENGINE': 'django.db.backends.sqlite3'}}
ROOT_URLCONF = 'simple_autocomplete.urls'
INSTALLED_APPS = ('simple_autocomplete', 'simple_autocomplete.tests', 'django.contrib.admin',
                  'django.contrib.auth', 'django.contrib.contenttypes')
MIDDLEWARE_CLASSES = ('django.contrib.sessions.middleware.SessionMiddleware', 'django.contrib.auth.middleware.AuthenticationMiddleware')
SECRET_KEY = 'SECRET_KEY'
SIMPLE_AUTOCOMPLETE = {'auth.user': {'search_field': 'username'}}