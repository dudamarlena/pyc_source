# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/project/settings_live_base.py
# Compiled at: 2015-09-02 09:05:45
from project.settings import *
DEBUG = False
TEMPLATE_DEBUG = DEBUG
DATABASES = {'default': {'ENGINE': 'django.db.backends.postgresql_psycopg2', 
               'NAME': 'skeleton', 
               'USER': 'skeleton', 
               'PASSWORD': 'skeleton', 
               'HOST': 'localhost', 
               'PORT': '5432'}}
MEDIA_ROOT = abspath('..', 'skeleton-media')
STATIC_ROOT = abspath('..', 'skeleton-static')
CKEDITOR_UPLOAD_PATH = os.path.join(MEDIA_ROOT, 'uploads')
CACHES = {'default': {'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache', 
               'LOCATION': '127.0.0.1:11211', 
               'KEY_PREFIX': 'skeleton_live'}}
COMPRESS_ENABLED = True
SENTRY_DSN = 'ENTER_YOUR_SENTRY_DSN_HERE'
SENTRY_CLIENT = 'raven.contrib.django.celery.CeleryClient'
RAVEN_CONFIG = {'dsn': 'ENTER_YOUR_SENTRY_DSN_HERE'}
ALLOWED_HOSTS = [
 '*']