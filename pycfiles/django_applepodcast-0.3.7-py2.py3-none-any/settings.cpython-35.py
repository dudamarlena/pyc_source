# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/Rich/Sites/django-applepodcast/podcast/tests/settings.py
# Compiled at: 2017-07-17 15:18:58
# Size of source mod 2**32: 658 bytes
from __future__ import unicode_literals
import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SECRET_KEY = 'fake-key'
INSTALLED_APPS = [
 'podcast']
DATABASES = {'default': {'ENGINE': 'django.db.backends.sqlite3', 
             'NAME': os.path.join(BASE_DIR, 'db.sqlite3'), 
             'TEST': {'NAME': None}}}
TEMPLATES = [
 {'BACKEND': 'django.template.backends.django.DjangoTemplates'}]
STATIC_URL = '/static/'
TIME_ZONE = 'UTC'
USE_TZ = True
ROOT_URLCONF = 'podcast.tests.urls'
import django
if hasattr(django, 'setup'):
    django.setup()