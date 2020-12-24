# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/emencia/django/links/testsettings.py
# Compiled at: 2010-01-14 11:17:33
import os
SITE_ID = 1
DATABASE_ENGINE = 'sqlite3'
DATABASE_NAME = '/tmp/links.db'
INSTALLED_APPS = ['django.contrib.auth',
 'django.contrib.contenttypes',
 'django.contrib.sessions',
 'django.contrib.sites',
 'emencia.django.links']
ROOT_URLCONF = 'emencia.django.links.urls'
LANGUAGE_CODE = 'en'
LANGUAGES = (
 ('fr', 'French'),
 ('en', 'English'))
MIDDLEWARE_CLASSES = ('django.middleware.common.CommonMiddleware', 'django.contrib.sessions.middleware.SessionMiddleware',
                      'django.contrib.auth.middleware.AuthenticationMiddleware',
                      'django.middleware.doc.XViewMiddleware', 'django.middleware.locale.LocaleMiddleware')