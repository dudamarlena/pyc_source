# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/tests/fixtures/sampledjango/settings2.py
# Compiled at: 2011-06-28 10:17:42
"""Django settings for sampledjango project."""
ADMINS = ()
MANAGERS = ADMINS
DATABASE_ENGINE = 'sqlite3'
DATABASE_NAME = 'data.db'
DATABASE_USER = ''
DATABASE_PASSWORD = ''
DATABASE_HOST = ''
DATABASE_PORT = ''
TIME_ZONE = 'Europe/London'
LANGUAGE_CODE = 'en-UK'
SITE_ID = 1
USE_I18N = False
MEDIA_ROOT = ''
MEDIA_URL = '/media/'
ADMIN_MEDIA_PREFIX = '/admin-media/'
SECRET_KEY = '1$=wr!0=j_ukk%h&#l-z7_@3pw0!g&$!-&e+*)x%^kc%bkk1y='
TEMPLATE_LOADERS = ('django.template.loaders.filesystem.load_template_source', 'django.template.loaders.app_directories.load_template_source')
MIDDLEWARE_CLASSES = ('django.middleware.common.CommonMiddleware', 'django.contrib.sessions.middleware.SessionMiddleware',
                      'django.contrib.auth.middleware.AuthenticationMiddleware')
ROOT_URLCONF = 'tests.fixtures.sampledjango.urls'
TEMPLATE_DIRS = ()
INSTALLED_APPS = ('django.contrib.auth', 'django.contrib.contenttypes', 'django.contrib.sessions',
                  'django.contrib.sites', 'tests.fixtures.sampledjango.app1', 'tests.fixtures.sampledjango.app2',
                  'tests.fixtures.sampledjango.unsecured_app')