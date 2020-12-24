# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/demoproj/settings.py
# Compiled at: 2009-01-08 09:11:51
"""
settings.py

softwarefabrica wiki demo project django settings file.

@author: Marco Pantaleoni
@contact: Marco Pantaleoni <panta@elasticworld.org>
@contact: Marco Pantaleoni <marco.pantaleoni@gmail.com>
@copyright: Copyright (C) 2008 Marco Pantaleoni. All rights reserved.
"""
import os
PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
DEBUG = True
TEMPLATE_DEBUG = DEBUG
ADMINS = (('Demo User', 'demo@demo.test'), )
MANAGERS = ADMINS
DATABASE_ENGINE = 'sqlite3'
DATABASE_NAME = os.path.join(PROJECT_ROOT, 'demo.db')
DATABASE_USER = ''
DATABASE_PASSWORD = ''
DATABASE_HOST = ''
DATABASE_PORT = ''
DEFAULT_CHARSET = 'utf-8'
TIME_ZONE = 'UTC'
LANGUAGE_CODE = 'en-us'
SITE_ID = 1
USE_I18N = True
UPLOAD_MEDIA_DIR = os.path.join(PROJECT_ROOT, 'upload_media')
STATIC_MEDIA_DIR = os.path.join(PROJECT_ROOT, 'static_media')
ADMIN_MEDIA_DIR = os.path.join(PROJECT_ROOT, 'admin_media')
WEBSITE_URL = 'http://wiki.demo.test'
UPLOAD_MEDIA_URL = '/uploads/'
ADMIN_MEDIA_PREFIX = '/admin_media/'
UPLOAD_MEDIA_PREFIX = '/uploads'
STATIC_MEDIA_PREFIX = '/static'
MEDIA_ROOT = UPLOAD_MEDIA_DIR
MEDIA_URL = UPLOAD_MEDIA_URL
STATIC_ROOT = STATIC_MEDIA_DIR
STATIC_URL = STATIC_MEDIA_PREFIX + '/'
ADMIN_MEDIA_PREFIX = ADMIN_MEDIA_PREFIX
LOGIN_URL = '/login'
SECRET_KEY = '95a5G32%!6@rhfb7%^6ofud1&1#17^jKJ!&5#vb$!$dhg!6s23'
TEMPLATE_LOADERS = ('django.template.loaders.filesystem.load_template_source', 'django.template.loaders.app_directories.load_template_source')
TEMPLATE_CONTEXT_PROCESSORS = ('django.core.context_processors.auth', 'django.core.context_processors.debug',
                               'django.core.context_processors.i18n', 'django.core.context_processors.media',
                               'django.core.context_processors.request', 'softwarefabrica.django.utils.viewshelpers.context_vars')
MIDDLEWARE_CLASSES = ('django.middleware.common.CommonMiddleware', 'django.contrib.sessions.middleware.SessionMiddleware',
                      'django.middleware.locale.LocaleMiddleware', 'django.contrib.auth.middleware.AuthenticationMiddleware',
                      'django.middleware.doc.XViewMiddleware')
ROOT_URLCONF = 'demoproj.urls'
TEMPLATE_DIRS = (
 os.path.join(PROJECT_ROOT, 'templates'),)
INSTALLED_APPS = ('django.contrib.auth', 'django.contrib.contenttypes', 'django.contrib.sessions',
                  'django.contrib.sites', 'django.contrib.admin', 'django.contrib.admindocs',
                  'django.contrib.markup', 'softwarefabrica.django.utils', 'softwarefabrica.django.forms',
                  'softwarefabrica.django.crud', 'softwarefabrica.django.wiki')