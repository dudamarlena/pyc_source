# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/site-packages/bootstrap3_wysihtml5x/tests/settings.py
# Compiled at: 2014-10-27 11:36:45
import os, tempfile
from django.core.files.storage import FileSystemStorage
DEBUG = True
TEMPLATE_DEBUG = DEBUG
ADMINS = ()
MANAGERS = ADMINS
DATABASES = {'default': {'ENGINE': 'django.db.backends.sqlite3', 
               'NAME': 'django_bootstrap3_wysihtml5x_test', 
               'USER': '', 
               'PASSWORD': '', 
               'HOST': '', 
               'PORT': ''}}
TIME_ZONE = 'Europe/Paris'
LANGUAGE_CODE = 'en-us'
SITE_ID = 1
USE_I18N = True
MEDIA_ROOT = ''
MEDIA_URL = ''
STATIC_URL = '/static/'
SECRET_KEY = 'v2824l&2-n+4zznbsk9c-ap5i)b3e8b+%*a=dxqlahm^%)68jn'
TEMPLATE_LOADERS = ('django.template.loaders.filesystem.Loader', 'django.template.loaders.app_directories.Loader')
MIDDLEWARE_CLASSES = ('django.middleware.common.CommonMiddleware', 'django.contrib.sessions.middleware.SessionMiddleware')
ROOT_URLCONF = 'bootstrap3_wysihtml5x.tests.urls'
TEMPLATE_DIRS = (
 os.path.join(os.path.dirname(__file__), '..', 'templates'),
 os.path.join(os.path.dirname(__file__), 'templates'))
INSTALLED_APPS = [
 'django.contrib.contenttypes',
 'django.contrib.sites',
 'bootstrap3_wysihtml5x',
 'bootstrap3_wysihtml5x.tests']
BOOTSTRAP3_WYSIHTML5X_TOOLBAR = {'foreColor': {'active': False}, 'createLink': {'active': False}}