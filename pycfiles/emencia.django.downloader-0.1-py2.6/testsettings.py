# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/emencia/django/downloader/testsettings.py
# Compiled at: 2010-04-20 11:51:29
"""Test setting for emencia.django.emencia.django.downloader"""
import os
DATABASE_ENGINE = 'sqlite3'
DATABASE_NAME = '/tmp/emencia.django.downloader.db'
INSTALLED_APPS = ['emencia.django.downloader']
ROOT_URLCONF = 'emencia.django.downloader.urls'
MEDIA_ROOT = 'tests'
LANGUAGE_CODE = 'en'
LANGUAGES = (
 ('fr', 'French'),
 ('en', 'English'))
MIDDLEWARE_CLASSES = ('django.middleware.common.CommonMiddleware', 'django.contrib.sessions.middleware.SessionMiddleware',
                      'django.contrib.auth.middleware.AuthenticationMiddleware',
                      'django.middleware.doc.XViewMiddleware', 'django.middleware.locale.LocaleMiddleware')