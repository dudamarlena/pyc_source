# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /pmc/Work/kolotev/0git/.github/django-enumfield-named-choices/django_enumfield_named_choices/tests/test_settings.py
# Compiled at: 2019-08-20 18:04:03
# Size of source mod 2**32: 1424 bytes
import os
TEST_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASES = {'default': {'ENGINE':'django.db.backends.sqlite3',  'NAME':':memory:'}}
CACHES = {'default': {'BACKEND': 'django.core.cache.backends.locmem.LocMemCache'}}
INSTALLED_APPS = [
 'django.contrib.admin',
 'django.contrib.auth',
 'django.contrib.contenttypes',
 'django.contrib.sessions',
 'django.contrib.messages',
 'django.contrib.staticfiles',
 'django_enumfield_named_choices',
 'tests.models']
MIDDLEWARE = ('django.middleware.security.SecurityMiddleware', 'django_applog.AppLogMiddleware',
              'django.middleware.common.CommonMiddleware', 'django.middleware.csrf.CsrfViewMiddleware',
              'django.contrib.sessions.middleware.SessionMiddleware', 'django.contrib.auth.middleware.AuthenticationMiddleware',
              'django.contrib.messages.middleware.MessageMiddleware')
SECRET_KEY = 'iufoj=mibkpdz*%bob952x(%49rqgv8gg45k36kjcg76&-y5=!'
TEMPLATES = [
 {'BACKEND':'django.template.backends.django.DjangoTemplates', 
  'APP_DIRS':True, 
  'OPTIONS':{'context_processors': [
                          'django.template.context_processors.debug',
                          'django.template.context_processors.request',
                          'django.contrib.auth.context_processors.auth',
                          'django.contrib.messages.context_processors.messages']}}]