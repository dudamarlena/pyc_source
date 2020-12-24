# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/site-packages/tests/settings.py
# Compiled at: 2016-11-01 11:12:10
import django
__doc__ = 'Minimal django settings to run manage.py test command'
DATABASES = {'default': {'ENGINE': 'django.db.backends.sqlite3', 
               'NAME': __name__}}
BROKER_BACKEND = 'memory'
ROOT_URLCONF = 'tests.urls'
from celery import current_app
CELERY_ALWAYS_EAGER = True
CELERY_EAGER_PROPAGATES_EXCEPTIONS = True
current_app.conf.CELERY_ALWAYS_EAGER = True
current_app.conf.CELERY_EAGER_PROPAGATES_EXCEPTIONS = True
CELERY_EAGER_TRANSACTION = True
MIDDLEWARE_CLASSES = ()
INSTALLED_APPS = ('django.contrib.auth', 'django.contrib.contenttypes', 'umeboshi')
USE_TZ = True
SECRET_KEY = 'django_tests_secret_key'
TIME_ZONE = 'America/New_York'
LANGUAGE_CODE = 'en-us'
ADMIN_MEDIA_PREFIX = '/static/admin/'
STATICFILES_DIRS = ()
if django.VERSION < (1, 6):
    TEST_RUNNER = 'django.test.simple.DjangoTestSuiteRunner'
else:
    TEST_RUNNER = 'django.test.runner.DiscoverRunner'