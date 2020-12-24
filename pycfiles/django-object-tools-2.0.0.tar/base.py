# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/silly/dev/django-object-tools/object_tools/tests/settings/base.py
# Compiled at: 2018-12-21 02:57:07
DEBUG = True
DATABASE_ENGINE = 'sqlite3'
DATABASES = {'default': {'ENGINE': 'django.db.backends.sqlite3', 
               'NAME': ':memory:'}}
SECRET_KEY = '123'
INSTALLED_APPS = [
 'django.contrib.auth',
 'django.contrib.contenttypes',
 'django.contrib.sessions',
 'object_tools',
 'django.contrib.admin',
 'object_tools.tests']
ROOT_URLCONF = 'object_tools.tests.urls'
STATIC_URL = '/static/'
TEMPLATES = [
 {'BACKEND': 'django.template.backends.django.DjangoTemplates', 
    'DIRS': [], 'OPTIONS': {'context_processors': [
                                     'django.contrib.auth.context_processors.auth',
                                     'django.template.context_processors.debug',
                                     'django.template.context_processors.i18n',
                                     'django.template.context_processors.media',
                                     'django.template.context_processors.static',
                                     'django.template.context_processors.tz',
                                     'django.template.context_processors.request',
                                     'django.contrib.messages.context_processors.messages'], 
                'loaders': [
                          'django.template.loaders.filesystem.Loader',
                          'django.template.loaders.app_directories.Loader']}}]
MIDDLEWARE = [
 'django.contrib.sessions.middleware.SessionMiddleware',
 'django.contrib.auth.middleware.AuthenticationMiddleware',
 'django.contrib.messages.middleware.MessageMiddleware']