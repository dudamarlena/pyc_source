# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/garethr/Documents/Projects/src/network/configs/common/settings.py
# Compiled at: 2009-06-25 09:59:29
import os, django
DJANGO_ROOT = os.path.dirname(os.path.realpath(django.__file__))
SITE_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
DEBUG = True
TEMPLATE_DEBUG = DEBUG
ADMINS = ()
MANAGERS = ADMINS
DATABASE_ENGINE = 'sqlite3'
DATABASE_NAME = os.path.join(SITE_ROOT, 'db') + '/development.db'
TIME_ZONE = 'Europe/London'
LANGUAGE_CODE = 'en-gb'
SITE_ID = 1
USE_I18N = False
MEDIA_ROOT = os.path.join(SITE_ROOT, 'assets')
MEDIA_URL = ''
ADMIN_MEDIA_PREFIX = '/media/'
SECRET_KEY = 'yqci=(=-#y#_=-!#rl_9!0z+^n=+c+gb-#w1i6s7!knoc9b1oy'
TEMPLATE_LOADERS = ('django.template.loaders.filesystem.load_template_source', 'django.template.loaders.app_directories.load_template_source',
                    'django.template.loaders.eggs.load_template_source')
MIDDLEWARE_CLASSES = ('django.middleware.common.CommonMiddleware', 'django.contrib.sessions.middleware.SessionMiddleware',
                      'django.contrib.auth.middleware.AuthenticationMiddleware')
ROOT_URLCONF = 'network.configs.common.urls'
TEMPLATE_DIRS = os.path.join(SITE_ROOT, 'templates')
INSTALLED_APPS = ('django.contrib.auth', 'django.contrib.contenttypes', 'django.contrib.sessions',
                  'django.contrib.sites', 'django.contrib.admin', 'django.contrib.admindocs',
                  'django.contrib.humanize', 'registration', 'clue', 'tagging', 'profiles',
                  'home')
AUTH_PROFILE_MODULE = 'profiles.profile'
ACCOUNT_ACTIVATION_DAYS = 7
LOGIN_REDIRECT_URL = '/'
EMAIL_HOST = 'localhost'
EMAIL_PORT = 1025
DEFAULT_FROM_EMAIL = 'webmaster@localhost'
try:
    from local_settings import *
except ImportError:
    pass