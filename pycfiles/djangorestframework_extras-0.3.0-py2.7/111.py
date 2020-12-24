# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/rest_framework_extras/tests/settings/111.py
# Compiled at: 2017-05-03 09:02:01
import os
USE_TZ = True
DATABASES = {'default': {'ENGINE': 'django.db.backends.sqlite3', 
               'NAME': 'drfe.db', 
               'USER': '', 
               'PASSWORD': '', 
               'HOST': '', 
               'PORT': ''}}
INSTALLED_APPS = ('rest_framework_extras.tests', 'rest_framework_extras', 'rest_framework',
                  'django.contrib.admin', 'django.contrib.auth', 'django.contrib.contenttypes',
                  'django.contrib.sessions', 'django.contrib.sites')
ROOT_URLCONF = 'rest_framework_extras.tests.urls'
MIDDLEWARE_CLASSES = ('django.contrib.sessions.middleware.SessionMiddleware', 'django.middleware.common.CommonMiddleware',
                      'django.contrib.auth.middleware.AuthenticationMiddleware',
                      'django.contrib.auth.middleware.SessionAuthenticationMiddleware')
TEMPLATE_CONTEXT_PROCESSORS = ('django.contrib.auth.context_processors.auth', 'django.template.context_processors.debug',
                               'django.template.context_processors.i18n', 'django.template.context_processors.media',
                               'django.template.context_processors.static', 'django.template.context_processors.tz',
                               'django.template.context_processors.request', 'django.contrib.messages.context_processors.messages')
TEMPLATES = [
 {'BACKEND': 'django.template.backends.django.DjangoTemplates', 
    'DIRS': [], 'APP_DIRS': True, 
    'OPTIONS': {'context_processors': TEMPLATE_CONTEXT_PROCESSORS}}]
SITE_ID = 1
STATIC_URL = '/static/'
SECRET_KEY = 'SECRET_KEY'
DEBUG = True