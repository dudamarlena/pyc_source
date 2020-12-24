# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/anyit/djattributes/settings.py
# Compiled at: 2011-03-21 19:39:57
import os
DEBUG = True
TEMPLATE_DEBUG = DEBUG
STATIC_SERVE = True
ROOT_PATH = os.path.abspath(os.path.dirname(__file__))
ADMINS = (('jah', 'jah@example.de'), )
MANAGERS = ADMINS
DATABASES = {'default': {'ENGINE': 'django.db.backends.sqlite3', 
               'NAME': 'attr.db'}}
SECRET_KEY = 'anysecretkey'
TIME_ZONE = 'Europe/Berlin'
SITE_ID = 1
USE_I18N = True
MEDIA_ROOT = os.path.join(ROOT_PATH, 'static/media')
MEDIA_URL = 'http://127.0.0.1/site_media/'
ADMIN_MEDIA_PREFIX = '/admin_media/'
MIDDLEWARE_CLASSES = ()
TEMPLATE_LOADERS = ()
TEMPLATE_DIRS = ()
TEMPLATE_CONTEXT_PROCESSORS = ()
ROOT_URLCONF = 'djattributes.urls'
INSTALLED_APPS = ('django.contrib.contenttypes', 'attributes')
INTERNAL_IPS = [
 '127.0.0.1']
LANGUAGES = (('en', 'English'), )