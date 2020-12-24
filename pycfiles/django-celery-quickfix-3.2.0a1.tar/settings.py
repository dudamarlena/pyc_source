# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/bharadwaj/Desktop/django-celery/tests/settings.py
# Compiled at: 2016-04-14 07:01:52
import warnings
warnings.filterwarnings('error', 'DateTimeField received a naive datetime', RuntimeWarning, 'django\\.db\\.models\\.fields')
import os, sys
sys.path.insert(0, os.getcwd())
sys.path.insert(0, os.path.join(os.getcwd(), os.pardir))
import djcelery
djcelery.setup_loader()
NO_NOSE = os.environ.get('DJCELERY_NO_NOSE', False)
SITE_ID = 300
DEBUG = True
TEMPLATE_DEBUG = DEBUG
ROOT_URLCONF = 'tests.urls'
SECRET_KEY = 'skskqlqlaskdsd'
ADMINS = ()
AUTOCOMMIT = True
if not NO_NOSE:
    TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'
here = os.path.abspath(os.path.dirname(__file__))
COVERAGE_EXCLUDE_MODULES = ('djcelery', 'djcelery.tests.*', 'djcelery.management.*',
                            'djcelery.contrib.*')
NOSE_ARGS = [
 os.path.join(here, os.pardir, 'djcelery', 'tests'),
 os.environ.get('NOSE_VERBOSE') and '--verbose' or '']
BROKER_URL = 'amqp://'
TT_HOST = 'localhost'
TT_PORT = 1978
CELERY_DEFAULT_EXCHANGE = 'testcelery'
CELERY_DEFAULT_ROUTING_KEY = 'testcelery'
CELERY_DEFAULT_QUEUE = 'testcelery'
CELERY_QUEUES = {'testcelery': {'binding_key': 'testcelery'}}
CELERY_ACCEPT_CONTENT = [
 'pickle', 'json']
CELERY_TASK_SERIALIZER = 'pickle'
CELERY_RESULT_SERIALIZER = 'pickle'
MANAGERS = ADMINS
DATABASES = {'default': {'NAME': 'djcelery-test-db', 
               'ENGINE': 'django.db.backends.sqlite3', 
               'USER': '', 
               'PASSWORD': '', 
               'PORT': ''}}
INSTALLED_APPS = ('django.contrib.auth', 'django.contrib.contenttypes', 'django.contrib.sessions',
                  'django.contrib.sites', 'djcelery', 'someapp', 'someappwotask')
if not NO_NOSE:
    INSTALLED_APPS = INSTALLED_APPS + ('django_nose', )
CELERY_SEND_TASK_ERROR_EMAILS = False
USE_TZ = True
TIME_ZONE = 'UTC'
CACHES = {'default': {'BACKEND': 'django.core.cache.backends.locmem.LocMemCache'}, 
   'django.core.cache.backends.dummy.DummyCache': {'BACKEND': 'django.core.cache.backends.dummy.DummyCache'}}
MIDDLEWARE_CLASSES = []