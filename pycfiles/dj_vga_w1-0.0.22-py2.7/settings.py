# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/dpl1_main/DPL1/settings.py
# Compiled at: 2014-02-28 04:35:41
"""
Django settings for DPL1 project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
SECRET_KEY = 'z**2kk-)t8s%w6q+^&ojrmetqlrvirisg5#p@7o6ee_ptxzf&4'
DEBUG = True
TEMPLATE_DEBUG = True
ALLOWED_HOSTS = []
INSTALLED_APPS = ('django.contrib.admin', 'django.contrib.auth', 'django.contrib.contenttypes',
                  'django.contrib.sessions', 'django.contrib.messages', 'django.contrib.staticfiles',
                  'dpl1_main.testing_app', 'south')
MIDDLEWARE_CLASSES = ('django.contrib.sessions.middleware.SessionMiddleware', 'django.middleware.common.CommonMiddleware',
                      'django.middleware.csrf.CsrfViewMiddleware', 'django.contrib.auth.middleware.AuthenticationMiddleware',
                      'django.contrib.messages.middleware.MessageMiddleware', 'django.middleware.clickjacking.XFrameOptionsMiddleware')
ROOT_URLCONF = 'dpl1_main.DPL1.urls'
WSGI_APPLICATION = 'dpl1_main.DPL1.wsgi.application'
DATABASES = {'default': {'ENGINE': 'django.db.backends.sqlite3', 
               'NAME': 'default.sqlite3'}}
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True
STATIC_URL = '/static/'
TEMPLATE_DIRS = (
 os.path.join(BASE_DIR, 'testing_app/templates'),)
SESSION_ENGINE = 'django.contrib.sessions.backends.signed_cookies'
SESSION_COOKIE_HTTPONLY = True
SESSION_SAVE_EVERY_REQUEST = True