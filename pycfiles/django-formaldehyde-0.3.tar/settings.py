# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/kraken/Projects/websites/django-formaldehyde/formaldehyde/formaldehyde/tests/settings.py
# Compiled at: 2015-01-30 04:54:36
import os
DIRNAME = os.path.dirname(__file__)
DEBUG = True
TEMPLATE_DEBUG = DEBUG
DEBUG_PROPAGATE_EXCEPTIONS = True
ADMINS = ()
MANAGERS = ADMINS
DATABASES = {'default': {'ENGINE': 'django.db.backends.sqlite3', 
               'NAME': os.path.join(DIRNAME, 'db.sqlite3'), 
               'TEST_NAME': os.path.join(DIRNAME, 'test_db.sqlite3')}}
TIME_ZONE = 'Europe/Rome'
LANGUAGE_CODE = 'en-us'
SITE_ID = 1
USE_I18N = True
USE_L10N = True
MEDIA_ROOT = ''
MEDIA_URL = ''
SECRET_KEY = 'fdO5Y<g#YRWG8;My1nrkLp>.w(w~q_b=|2`?3<x>0KxA%UB!77'
TEMPLATE_LOADERS = ('django.template.loaders.filesystem.Loader', 'django.template.loaders.app_directories.Loader')
MIDDLEWARE_CLASSES = ('django.middleware.common.CommonMiddleware', 'django.contrib.sessions.middleware.SessionMiddleware',
                      'django.middleware.csrf.CsrfViewMiddleware', 'django.contrib.auth.middleware.AuthenticationMiddleware',
                      'django.contrib.messages.middleware.MessageMiddleware')
ROOT_URLCONF = 'formaldehyde.tests.urls'
TEMPLATE_DIRS = ()
INSTALLED_APPS = ('django.contrib.auth', 'django.contrib.contenttypes', 'django.contrib.sessions',
                  'django.contrib.sites', 'django.contrib.messages', 'django.contrib.admin',
                  'formaldehyde', 'formaldehyde.tests')
TEST_RUNNER = 'django.test.runner.DiscoverRunner'
STATIC_URL = '/static/'