# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: templateaddons/../templateaddons/test_settings.py
# Compiled at: 2016-10-21 19:20:08
import os
PROJECT_DIR = os.path.dirname(__file__)
DEBUG = True
ADMINS = ()
CACHE_BACKEND = 'locmem:///'
MANAGERS = ADMINS
DATABASES = {'default': {'ENGINE': 'django.db.backends.sqlite3', 
               'NAME': 'test.db'}}
TIME_ZONE = 'America/Chicago'
SITE_ID = 1
USE_I18N = True
MEDIA_ROOT = STATIC_ROOT = os.path.join(PROJECT_DIR, 'media')
MEDIA_URL = '/media/'
STATIC_ROOT = os.path.join(PROJECT_DIR, 'media', 'static')
STATIC_URL = MEDIA_URL + 'static/'
ADMIN_MEDIA_ROOT = os.path.join(STATIC_ROOT, 'admin_media')
ADMIN_MEDIA_PREFIX = '/admin_media/'
SECRET_KEY = '*xq7m@)*f2awoj!spa0(jibsrz9%c0d=e(g)v*!17y(vx0ue_3'
_TEMPLATE_CONTEXT_PROCESSORS = ('django.contrib.auth.context_processors.auth', 'django.template.context_processors.i18n',
                                'django.template.context_processors.debug', 'django.template.context_processors.request',
                                'django.template.context_processors.media')
INTERNAL_IPS = ('127.0.0.1', )
MIDDLEWARE_CLASSES = ('django.contrib.sessions.middleware.SessionMiddleware', 'django.middleware.locale.LocaleMiddleware',
                      'django.middleware.common.CommonMiddleware', 'django.contrib.auth.middleware.AuthenticationMiddleware',
                      'django.contrib.messages.middleware.MessageMiddleware')
_TEMPLATE_DIRS = (
 os.path.join(PROJECT_DIR, 'templates'),)
CACHE_BACKEND = 'locmem:///?timeout=300&max_entries=6000'
INSTALLED_APPS = ('django.contrib.auth', 'django.contrib.contenttypes', 'django.contrib.sessions',
                  'django.contrib.admin', 'django.contrib.sites', 'django.contrib.sitemaps',
                  'templateaddons')
LANGUAGE_CODE = 'en-us'
TEMPLATES = [
 {'BACKEND': 'django.template.backends.django.DjangoTemplates', 
    'APP_DIRS': True, 
    'DIRS': _TEMPLATE_DIRS, 
    'OPTIONS': {'debug': DEBUG, 
                'context_processors': _TEMPLATE_CONTEXT_PROCESSORS}}]
COVERAGE_EXCLUDE_MODULES = ('templateaddons.tests.*', )
COVERAGE_HTML_REPORT = True
COVERAGE_BRANCH_COVERAGE = False
try:
    from local_settings import *
except ImportError:
    pass