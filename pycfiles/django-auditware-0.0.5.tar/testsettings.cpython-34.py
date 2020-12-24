# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/val/Projects/workon/mpro/sf3/apps/django-auditware/auditware/tests/testsettings.py
# Compiled at: 2016-04-05 16:17:06
# Size of source mod 2**32: 321 bytes
DATABASES = {'default': {'ENGINE': 'django.db.backends.sqlite3', 
             'NAME': ':memory:'}}
SECRET_KEY = 'un33k'
INSTALLED_APPS = ('django.contrib.auth', 'django.contrib.admin', 'django.contrib.contenttypes',
                  'django.contrib.sessions', 'auditware')
MIDDLEWARE_CLASSES = []