# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ../tests/settings.py
# Compiled at: 2011-11-29 10:38:59
import os, sys
sys.path.insert(0, os.getcwd())
sys.path.insert(0, os.path.join(os.getcwd(), os.pardir))
SITE_ID = 300
DEBUG = True
TEMPLATE_DEBUG = DEBUG
ROOT_URLCONF = 'tests.urls'
ADMINS = ()
TEST_RUNNER = 'django_nose.run_tests'
here = os.path.abspath(os.path.dirname(__file__))
COVERAGE_EXCLUDE_MODULES = ('cyme.tests.*', )
NOSE_ARGS = [
 os.path.join(here, os.pardir, 'cyme', 'tests'),
 os.environ.get('NOSE_VERBOSE') and '--verbose' or '',
 '--cover3-package=cyme',
 '--cover3-branch',
 '--cover3-exclude=%s' % (',').join(COVERAGE_EXCLUDE_MODULES)]
BROKER_HOST = 'localhost'
BROKER_PORT = 5672
BROKER_VHOST = '/'
BROKER_USER = 'guest'
BROKER_PASSWORD = 'guest'
TT_HOST = 'localhost'
TT_PORT = 1978
CELERY_DEFAULT_EXCHANGE = 'test.cyme'
CELERY_DEFAULT_ROUTING_KEY = 'test.cyme'
CELERY_DEFAULT_QUEUE = 'test.cyme'
CELERY_QUEUES = {'test.cyme': {'binding_key': 'test.cyme'}}
MANAGERS = ADMINS
DATABASES = {'default': {'ENGINE': 'django.db.backends.sqlite3', 
               'NAME': 'cyme-test.db'}}
INSTALLED_APPS = ('django.contrib.auth', 'django.contrib.contenttypes', 'django.contrib.sessions',
                  'django.contrib.sites', 'django_nose', 'cyme', 'cyme.api')
CELERY_SEND_TASK_ERROR_EMAILS = False