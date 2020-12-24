# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/hedley/django/instances/django-form-renderers/form_renderers/tests/settings/111.py
# Compiled at: 2017-05-03 06:25:32
import os
DEBUG = True
DATABASES = {'default': {'ENGINE': 'django.db.backends.sqlite3'}}
INSTALLED_APPS = ('test_without_migrations', 'form_renderers', 'form_renderers.tests',
                  'django.contrib.contenttypes', 'django.contrib.sites')
CACHES = {'default': {'BACKEND': 'django.core.cache.backends.locmem.LocMemCache'}}
SITE_ID = 1
SECRET_KEY = 'SECRET_KEY'
FORM_RENDERERS = {'enable-bem-classes': True}