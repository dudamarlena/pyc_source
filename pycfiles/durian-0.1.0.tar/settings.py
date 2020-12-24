# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /opt/devel/durian/testproj/settings.py
# Compiled at: 2009-09-12 09:43:32
import os, sys
sys.path.insert(0, os.path.join(os.getcwd(), os.pardir))
SITE_ID = 301
DEBUG = True
TEMPLATE_DEBUG = DEBUG
ROOT_URLCONF = 'urls'
ADMINS = ()
TEST_RUNNER = 'celery.tests.runners.run_tests'
TEST_APPS = ('durian', )
AMQP_SERVER = 'localhost'
AMQP_PORT = 5672
AMQP_VHOST = '/'
AMQP_USER = 'guest'
AMQP_PASSWORD = 'guest'
TT_HOST = 'localhost'
TT_PORT = 1978
CELERY_AMQP_EXCHANGE = 'testdurian'
CELERY_AMQP_ROUTING_KEY = 'testdurian'
CELERY_AMQP_CONSUMER_QUEUE = 'testdurian'
MANAGERS = ADMINS
DATABASE_ENGINE = 'sqlite3'
DATABASE_NAME = 'testdb.sqlite'
DATABASE_USER = ''
DATABASE_PASSWORD = ''
DATABASE_HOST = ''
DATABASE_PORT = ''
INSTALLED_APPS = ('django.contrib.auth', 'django.contrib.contenttypes', 'django.contrib.sessions',
                  'django.contrib.sites', 'celery', 'durian')
try:
    import test_extensions
except ImportError:
    pass

SEND_CELERY_TASK_ERROR_EMAILS = False