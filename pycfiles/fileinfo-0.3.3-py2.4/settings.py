# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.5-i386/egg/fileinfo/guidjango/settings.py
# Compiled at: 2007-11-06 13:51:50
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
SECRET_KEY = '_*0+wx1-b214*6a$sh3tgp-4e2#c=mt5!he#li=mlc7*xzlt1+'
TEMPLATE_LOADERS = ('django.template.loaders.filesystem.load_template_source', 'django.template.loaders.app_directories.load_template_source')
MIDDLEWARE_CLASSES = ('django.middleware.common.CommonMiddleware', 'django.contrib.sessions.middleware.SessionMiddleware',
                      'django.contrib.auth.middleware.AuthenticationMiddleware',
                      'django.middleware.doc.XViewMiddleware')
ROOT_URLCONF = 'guidjango.urls'
from os.path import dirname, join
path = join(dirname(__file__), 'templates')
TEMPLATE_DIRS = (
 path,)
INSTALLED_APPS = ('django.contrib.auth', 'django.contrib.contenttypes', 'django.contrib.sessions',
                  'django.contrib.sites')