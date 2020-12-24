# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/javed/Work/Dinette/forum/settings.py
# Compiled at: 2013-07-02 04:51:32
import os
DEBUG = True
TEMPLATE_DEBUG = DEBUG
PROJECT_DIR = os.path.dirname(__file__)
ADMINS = ()
MANAGERS = ADMINS
DATABASES = {'default': {'ENGINE': 'django.db.backends.sqlite3', 
               'NAME': 'dinette.db', 
               'USER': '', 
               'PASSWORD': '', 
               'HOST': '', 
               'PORT': ''}}
TIME_ZONE = 'America/Chicago'
LANGUAGE_CODE = 'en-us'
SITE_ID = 1
USE_I18N = True
USE_L10N = True
MEDIA_ROOT = 'dinette/media/'
MEDIA_URL = '/site_media/'
ADMIN_MEDIA_PREFIX = '/media/'
SECRET_KEY = '9oezy17)u&_!3n%@qb^iqz%ur2%v(5=0uas@@#4)=n@5xy3m1j'
TEMPLATE_LOADERS = ('django.template.loaders.filesystem.Loader', 'django.template.loaders.app_directories.Loader')
MIDDLEWARE_CLASSES = ('django.middleware.common.CommonMiddleware', 'django.contrib.sessions.middleware.SessionMiddleware',
                      'django.middleware.csrf.CsrfViewMiddleware', 'django.contrib.auth.middleware.AuthenticationMiddleware',
                      'django.contrib.messages.middleware.MessageMiddleware', 'pagination.middleware.PaginationMiddleware')
ROOT_URLCONF = 'urls'
TEMPLATE_DIRS = os.path.join(PROJECT_DIR, 'templates')
TEMPLATE_CONTEXT_PROCESSORS = ('django.contrib.auth.context_processors.auth', 'django.core.context_processors.debug',
                               'django.core.context_processors.i18n', 'django.core.context_processors.media',
                               'django.contrib.messages.context_processors.messages',
                               'django.core.context_processors.request', 'django.core.context_processors.static')
INSTALLED_APPS = ('django.contrib.auth', 'django.contrib.contenttypes', 'django.contrib.sessions',
                  'django.contrib.sites', 'django.contrib.messages', 'django.contrib.admin',
                  'django.contrib.staticfiles', 'dinette', 'compressor', 'google_analytics',
                  'sorl.thumbnail', 'openid_consumer', 'pagination', 'accounts')
STATIC_URL = '/static/'
from localsettings import *