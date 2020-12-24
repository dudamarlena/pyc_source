# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-jkXn_D/django-js-reverse/tests/settings.py
# Compiled at: 2018-07-11 18:15:31
import os
DATABASES = {'default': {'ENGINE': 'django.db.backends.sqlite3', 
               'NAME': ':memory:'}}
SECRET_KEY = 'wtf'
ROOT_URLCONF = None
USE_TZ = True
INSTALLED_APPS = ('django_js_reverse', )
ALLOWED_HOSTS = [
 'testserver']
MIDDLEWARE_CLASSES = ()
STATIC_ROOT = os.path.join(os.path.dirname(__file__), 'tmp')