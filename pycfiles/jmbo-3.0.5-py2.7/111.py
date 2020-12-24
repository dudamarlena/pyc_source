# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/jmbo/tests/settings/111.py
# Compiled at: 2017-05-03 05:57:29
import os
USE_TZ = True
TIME_ZONE = 'Africa/Johannesburg'
DATABASES = {'default': {'ENGINE': 'django.db.backends.postgresql', 
               'NAME': 'jmbo', 
               'USER': 'postgres', 
               'PASSWORD': '', 
               'HOST': '', 
               'PORT': ''}}
INSTALLED_APPS = ('jmbo.tests', 'jmbo.tests.extra', 'jmbo', 'category', 'crum', 'django_comments',
                  'layers', 'likes', 'pagination', 'photologue', 'preferences', 'rest_framework',
                  'rest_framework_extras', 'secretballot', 'sites_groups', 'ultracache',
                  'django.contrib.admin', 'django.contrib.auth', 'django.contrib.contenttypes',
                  'django.contrib.sessions', 'django.contrib.sites')
ROOT_URLCONF = 'jmbo.tests.urls'
MIDDLEWARE_CLASSES = ('django.middleware.common.CommonMiddleware', 'django.contrib.sessions.middleware.SessionMiddleware',
                      'django.middleware.csrf.CsrfViewMiddleware', 'django.contrib.auth.middleware.AuthenticationMiddleware',
                      'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
                      'django.contrib.messages.middleware.MessageMiddleware', 'likes.middleware.SecretBallotUserIpUseragentMiddleware',
                      'pagination.middleware.PaginationMiddleware', 'crum.CurrentRequestUserMiddleware')
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
MEDIA_ROOT = '/tmp/jmbo'
CELERY_ALWAYS_EAGER = True
BROKER_BACKEND = 'memory'
SECRET_KEY = 'SECRET_KEY'
DEBUG = True
ULTRACACHE = {'invalidate': False}
REST_FRAMEWORK = {'DEFAULT_VERSIONING_CLASS': 'rest_framework.versioning.URLPathVersioning'}