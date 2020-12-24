# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/yash/Desktop/django-query-profiler/tests/testapp/sqlite_settings.py
# Compiled at: 2020-01-07 01:57:47
# Size of source mod 2**32: 1714 bytes
import os
from django_query_profiler.settings import *
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INSTALLED_APPS = ('django.contrib.admin', 'django.contrib.auth', 'django.contrib.contenttypes',
                  'django.contrib.sessions', 'django.contrib.messages', 'django.contrib.staticfiles',
                  'django_query_profiler', 'tests.testapp.food')
SECRET_KEY = 'dummy'
ROOT_URLCONF = 'tests.testapp.urls'
DATABASES = {'default': {'ENGINE':'django_query_profiler.django.db.backends.sqlite3', 
             'NAME':os.path.join(BASE_DIR, 'db.sqlite3')}}
MIDDLEWARE = [
 'django_query_profiler.client.middleware.QueryProfilerMiddleware',
 'django.middleware.security.SecurityMiddleware',
 'django.contrib.sessions.middleware.SessionMiddleware',
 'django.middleware.common.CommonMiddleware',
 'django.middleware.csrf.CsrfViewMiddleware',
 'django.contrib.auth.middleware.AuthenticationMiddleware',
 'django.contrib.messages.middleware.MessageMiddleware',
 'django.middleware.clickjacking.XFrameOptionsMiddleware']
TEMPLATES = [
 {'BACKEND':'django.template.backends.django.DjangoTemplates', 
  'DIRS':[
   os.path.join(BASE_DIR, 'templates')], 
  'APP_DIRS':True, 
  'OPTIONS':{'context_processors': [
                          'django.template.context_processors.debug',
                          'django.template.context_processors.request',
                          'django.contrib.auth.context_processors.auth',
                          'django.contrib.messages.context_processors.messages']}}]