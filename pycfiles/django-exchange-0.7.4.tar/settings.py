# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/zekus/devel/projects/metglobal/django-exchange/test_project/settings.py
# Compiled at: 2015-05-27 08:55:19
INSTALLED_APPS = [
 'exchange']
DATABASES = {'default': {'ENGINE': 'django.db.backends.sqlite3', 
               'NAME': 'test.db'}}
TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'
OPENEXCHANGERATES_API_KEY = '<DUMMY_KEY>'