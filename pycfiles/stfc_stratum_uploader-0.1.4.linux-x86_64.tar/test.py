# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/vwa13376/workspace/uploader/archer/settings/test.py
# Compiled at: 2013-08-20 06:49:48
import os
from configurations import importer
importer.install()
from archer.settings.common import Common

class Test(Common):
    DEBUG = True
    TEMPLATE_DEBUG = DEBUG
    DATABASES = {'default': {'ENGINE': 'django.db.backends.sqlite3', 
                   'NAME': ':memory:', 
                   'TEST_NAME': ':memory:'}}
    SOUTH_TESTS_MIGRATE = False
    INSTALLED_APPS = Common.INSTALLED_APPS + ('django_nose', )
    TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'
    PASSWORD_HASHERS = ('django.contrib.auth.hashers.MD5PasswordHasher', )
    DEFAULT_FILE_STORAGE = 'inmemorystorage.InMemoryStorage'


class PostgresCI(Test):
    DEBUG = True
    DATABASES = {'default': {'ENGINE': 'django.db.backends.postgresql_psycopg2', 
                   'NAME': 'uploader_ci_test', 
                   'USER': 'postgres', 
                   'PASSWORD': '', 
                   'HOST': '127.0.0.1', 
                   'PORT': ''}}


class SqliteCI(Test):
    DEBUG = True
    DATABASES = {'default': {'ENGINE': 'django.db.backends.sqlite3', 
                   'NAME': ':memory:', 
                   'TEST_NAME': ':memory:'}}