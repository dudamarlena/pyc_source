# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ikeda/.virtualenvs/rsyslog-monitor/django_spine/django-spine/tests/settings.py
# Compiled at: 2012-07-17 10:44:29
ADMINS = (('test@example.com', 'Test da'), )
DEBUG = True
TEMPLATE_DEBUG = DEBUG
DATABASE_ENGINE = 'sqlite3'
DATABASE_NAME = 'spine.db'
TEST_DATABASE_NAME = 'spine-test.db'
DATABASES = {'default': {'ENGINE': 'django.db.backends.%s' % DATABASE_ENGINE, 
               'NAME': DATABASE_NAME, 
               'TEST_NAME': TEST_DATABASE_NAME}}
SECRET_KEY = '7r33b34rd'
INSTALLED_APPS = [
 'subcommand',
 'spine']