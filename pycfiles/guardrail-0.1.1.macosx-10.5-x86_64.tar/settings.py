# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jmcarp/miniconda/envs/guardian/lib/python2.7/site-packages/examples/djanguard/settings.py
# Compiled at: 2015-03-26 14:06:46
"""
Django settings for djanguard project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
SECRET_KEY = '+e8*zp2y_d^6c)7z2o%&r&*ucz8%-r)4+qd@z-aqlt&8#1$pz4'
DEBUG = True
TEMPLATE_DEBUG = True
ALLOWED_HOSTS = []
import sys
sys.path.append('/Users/jmcarp/code/guardrail')
INSTALLED_APPS = ('django.contrib.admin', 'django.contrib.auth', 'django.contrib.contenttypes',
                  'django.contrib.sessions', 'django.contrib.messages', 'django.contrib.staticfiles',
                  'django_extensions', 'guardrail.ext.django', 'djanguard')
MIDDLEWARE_CLASSES = ('django.contrib.sessions.middleware.SessionMiddleware', 'django.middleware.common.CommonMiddleware',
                      'django.middleware.csrf.CsrfViewMiddleware', 'django.contrib.auth.middleware.AuthenticationMiddleware',
                      'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
                      'django.contrib.messages.middleware.MessageMiddleware', 'django.middleware.clickjacking.XFrameOptionsMiddleware')
ROOT_URLCONF = 'djanguard.urls'
WSGI_APPLICATION = 'djanguard.wsgi.application'
DATABASES = {'default': {'ENGINE': 'django.db.backends.sqlite3', 
               'NAME': os.path.join(BASE_DIR, 'db.sqlite3')}}
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True
STATIC_URL = '/static/'
AUTH_USER_MODEL = 'djanguard.User'
AUTHENTICATION_BACKENDS = ('django.contrib.auth.backends.ModelBackend', 'guardian.ext.django.ObjectPermissionBackend')