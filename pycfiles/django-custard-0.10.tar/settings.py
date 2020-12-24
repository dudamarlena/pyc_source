# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/lucio/Projects/django-custard/custard/example/example/settings.py
# Compiled at: 2014-07-29 05:28:08
"""
Django settings for example project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
import sys
sys.path.append(os.path.dirname(BASE_DIR))
SECRET_KEY = '%gt7a3*l@a4-o3f-*v**0=jn38pvwpfrcy%a(t&4xb#6nix5&!'
DEBUG = True
TEMPLATE_DEBUG = True
ALLOWED_HOSTS = []
INSTALLED_APPS = ('django.contrib.admin', 'django.contrib.auth', 'django.contrib.contenttypes',
                  'django.contrib.sessions', 'django.contrib.messages', 'django.contrib.staticfiles',
                  'custard', 'example.demo')
MIDDLEWARE_CLASSES = ('django.contrib.sessions.middleware.SessionMiddleware', 'django.middleware.common.CommonMiddleware',
                      'django.middleware.csrf.CsrfViewMiddleware', 'django.contrib.auth.middleware.AuthenticationMiddleware',
                      'django.contrib.messages.middleware.MessageMiddleware', 'django.middleware.clickjacking.XFrameOptionsMiddleware')
ROOT_URLCONF = 'example.urls'
WSGI_APPLICATION = 'example.wsgi.application'
DATABASES = {'default': {'ENGINE': 'django.db.backends.sqlite3', 
               'NAME': os.path.join(BASE_DIR, 'db.sqlite3')}}
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True
STATIC_URL = '/static/'
try:
    import suit
    from django.conf.global_settings import TEMPLATE_CONTEXT_PROCESSORS as TCP
    INSTALLED_APPS = ('suit', ) + INSTALLED_APPS
    TEMPLATE_CONTEXT_PROCESSORS = TCP + ('django.core.context_processors.request', )
except ImportError:
    pass

CUSTOM_CONTENT_TYPES = ('example', 'user')