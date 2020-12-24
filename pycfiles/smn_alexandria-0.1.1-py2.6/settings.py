# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-x86_64/egg/alexandria/sessions/db/settings.py
# Compiled at: 2011-04-12 08:16:41
import os
from os.path import join, abspath, dirname
DEBUG = True
APP_ROOT = abspath(join(dirname(__file__), '..'))
DATABASES = {'default': {'ENGINE': 'django.db.backends.sqlite3', 
               'NAME': join(APP_ROOT, 'db', 'sqlite3', 'alexandria_dev.db'), 
               'USER': '', 
               'PASSWORD': '', 
               'PORT': ''}}
if DATABASES['default']['ENGINE'].endswith('sqlite3'):
    DISABLE_TRANSACTION_MANAGEMENT = True
INSTALLED_APPS = 'alexandria.sessions.db'
TEMPLATE_DIRS = join(APP_ROOT, 'db/templates')
MEDIA_ROOT = join(APP_ROOT, 'db', 'media')
MEDIA_URL = '/static/'
ROOT_URLCONF = 'alexandria.sessions.db.urls'
INSTALLED_APPS = ('django.contrib.admin', 'django.contrib.contenttypes', 'alexandria.sessions.db')
TEST_RUNNER = 'django_nose.run_tests'