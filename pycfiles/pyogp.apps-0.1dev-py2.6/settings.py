# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-universal/egg/pyogp/apps/web/django/pyogp_webbot/settings.py
# Compiled at: 2009-12-22 03:50:08
import os
DEBUG = True
TEMPLATE_DEBUG = DEBUG
ADMINS = ()
MANAGERS = ADMINS
DATABASE_ENGINE = ''
DATABASE_NAME = ''
DATABASE_USER = ''
DATABASE_PASSWORD = ''
DATABASE_HOST = ''
DATABASE_PORT = ''
TIME_ZONE = 'America/Chicago'
LANGUAGE_CODE = 'en-us'
SITE_ID = 1
USE_I18N = True
MEDIA_ROOT = ''
MEDIA_URL = ''
ADMIN_MEDIA_PREFIX = '/media/'
SECRET_KEY = '^*2mu-s($ntsm=j5&b+*gcew*&dzdy0483)!_op#a+-ps%w^ln'
TEMPLATE_LOADERS = ('django.template.loaders.filesystem.load_template_source', 'django.template.loaders.app_directories.load_template_source')
MIDDLEWARE_CLASSES = ('django.middleware.common.CommonMiddleware', 'django.contrib.sessions.middleware.SessionMiddleware',
                      'django.contrib.auth.middleware.AuthenticationMiddleware')
ROOT_URLCONF = 'pyogp_webbot.urls'
TEMPLATE_DIRS = os.path.join(os.path.dirname(__file__), 'login/templates/')
INSTALLED_APPS = ('django.contrib.auth', 'django.contrib.contenttypes', 'django.contrib.sessions',
                  'django.contrib.sites', 'pyogp_webbot.login')