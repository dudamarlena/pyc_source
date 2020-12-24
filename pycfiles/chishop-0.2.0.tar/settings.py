# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /opt/devel/chishop/chishop/settings.py
# Compiled at: 2009-03-21 16:57:11
import os
DEBUG = True
TEMPLATE_DEBUG = True
LOCAL_DEVELOPMENT = True
ADMINS = ()
MANAGERS = ADMINS
DATABASE_ENGINE = 'sqlite3'
DATABASE_NAME = 'devdatabase.db'
DATABASE_USER = ''
DATABASE_PASSWORD = ''
DATABASE_HOST = ''
DATABASE_PORT = ''
TIME_ZONE = 'America/Chicago'
LANGUAGE_CODE = 'en-us'
SITE_ID = 1
USE_I18N = True
here = os.path.abspath(os.path.dirname(__file__))
MEDIA_ROOT = os.path.join(here, 'media')
MEDIA_URL = 'media/'
MEDIA_PREFIX = '/media/'
ADMIN_MEDIA_PREFIX = '/admin-media/'
SECRET_KEY = 'w_#0r2hh)=!zbynb*gg&969@)sy#^-^ia3m*+sd4@lst$zyaxu'
TEMPLATE_LOADERS = ('django.template.loaders.filesystem.load_template_source', 'django.template.loaders.app_directories.load_template_source')
MIDDLEWARE_CLASSES = ('django.middleware.common.CommonMiddleware', 'django.contrib.sessions.middleware.SessionMiddleware',
                      'django.contrib.auth.middleware.AuthenticationMiddleware')
ROOT_URLCONF = 'urls'
TEMPLATE_DIRS = ()
INSTALLED_APPS = ('django.contrib.auth', 'django.contrib.contenttypes', 'django.contrib.sessions',
                  'django.contrib.sites', 'django.contrib.admin', 'djangopypi')