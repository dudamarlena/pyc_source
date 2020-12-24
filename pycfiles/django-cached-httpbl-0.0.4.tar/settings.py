# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Volumes/MacOSExt/Projects/django-apps/django_cached_httpbl/docs/example_app/example_app/settings.py
# Compiled at: 2016-04-05 07:35:51
"""
Django settings for example_app project.

For more information on this file, see
https://docs.djangoproject.com/en/dev/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/dev/ref/settings/
"""
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
SECRET_KEY = 'secretkey'
DEBUG = True
TEMPLATE_DEBUG = True
DEBUG_TOOLBAR = True
ALLOWED_HOSTS = []
SITE_ID = 1
INSTALLED_APPS = ('django.contrib.admin', 'django.contrib.auth', 'django.contrib.contenttypes',
                  'django.contrib.sessions', 'django.contrib.messages', 'django.contrib.staticfiles',
                  'django.contrib.sites')
MIDDLEWARE_CLASSES = ('django.contrib.sessions.middleware.SessionMiddleware', 'django.middleware.common.CommonMiddleware',
                      'django.middleware.csrf.CsrfViewMiddleware', 'django.contrib.auth.middleware.AuthenticationMiddleware',
                      'django.contrib.messages.middleware.MessageMiddleware', 'django.middleware.clickjacking.XFrameOptionsMiddleware',
                      'cached_httpbl.middleware.CachedHTTPBLViewMiddleware')
TEMPLATE_DIRS = tuple([ os.path.join(BASE_DIR, app_name, 'templates') for app_name in INSTALLED_APPS ])
TEMPLATE_DIRS += tuple([os.path.join(BASE_DIR, 'templates')])
TEMPLATE_CONTEXT_PROCESSORS = ('django.contrib.auth.context_processors.auth', 'django.core.context_processors.request',
                               'django.core.context_processors.debug', 'django.core.context_processors.i18n',
                               'django.core.context_processors.media', 'django.core.context_processors.static',
                               'django.core.context_processors.tz', 'django.contrib.messages.context_processors.messages')
ROOT_URLCONF = 'example_app.urls'
WSGI_APPLICATION = 'example_app.wsgi.application'
DATABASES = {'default': {'ENGINE': 'django.db.backends.sqlite3', 
               'NAME': os.path.join(BASE_DIR, 'db.sqlite3')}}
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True
gettext = lambda s: s
LANGUAGES = (
 (
  'en', gettext('English')),)
STATIC_URL = '/static/'
CACHED_HTTPBL_API_KEY = 'abcdefghijkl'