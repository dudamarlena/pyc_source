# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-x86_64/egg/settings/base.py
# Compiled at: 2015-09-02 20:59:23
"""
Base settings for UBCPI.
"""
import os, sys
DEBUG = True
TEMPLATE_DEBUG = DEBUG
ADMINS = (('admin', 'admin'), )
MANAGERS = ADMINS
DATABASES = {'default': {'ENGINE': 'django.db.backends.sqlite3', 
               'NAME': 'ubcpi.db', 
               'USER': '', 
               'PASSWORD': '', 
               'HOST': '', 
               'PORT': ''}}
TIME_ZONE = 'America/Vancouver'
LANGUAGE_CODE = 'en-us'
SITE_ID = 1
USE_I18N = True
USE_L10N = True
USE_TZ = True
MEDIA_ROOT = ''
MEDIA_URL = ''
STATIC_ROOT = ''
STATIC_URL = '/static/'
STATICFILES_DIRS = ()
STATICFILES_FINDERS = ('django.contrib.staticfiles.finders.FileSystemFinder', 'django.contrib.staticfiles.finders.AppDirectoriesFinder')
SECRET_KEY = 'as90890sugiolkn3241jj3209ufdaljfk90u234lkgdknlajfslaf324098dfs'
TEMPLATE_LOADERS = ('django.template.loaders.filesystem.Loader', 'django.template.loaders.app_directories.Loader')
MIDDLEWARE_CLASSES = ('django.middleware.common.CommonMiddleware', 'django.contrib.sessions.middleware.SessionMiddleware',
                      'django.middleware.csrf.CsrfViewMiddleware', 'django.contrib.auth.middleware.AuthenticationMiddleware',
                      'django.contrib.messages.middleware.MessageMiddleware')
ROOT_URLCONF = 'urls'
INSTALLED_APPS = ('django.contrib.auth', 'django.contrib.contenttypes', 'django.contrib.sessions',
                  'django.contrib.sites', 'django.contrib.messages', 'django.contrib.staticfiles',
                  'django.contrib.admin', 'django.contrib.admindocs', 'django_extensions',
                  'south', 'workbench', 'submissions', 'ubcpi')
WORKBENCH = {'reset_state_on_restart': False}
CACHES = {'default': {'BACKEND': 'django.core.cache.backends.locmem.LocMemCache', 
               'LOCATION': 'default_loc_mem'}}
BASE_DIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))