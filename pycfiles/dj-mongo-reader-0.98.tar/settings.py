# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/fanfei/Documents/Code/dj-mongo-reader/example/sampleapp/sampleapp/settings.py
# Compiled at: 2015-03-09 23:11:56
"""
Django settings for sampleapp project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
SECRET_KEY = 'pm@k_+_%t4$@8z6cv)+e%t83toeis^j2ditncsh3px#@j8li*-'
DEBUG = False if os.getenv('MONGOLAB_URI', None) else True
TEMPLATE_DEBUG = True
ALLOWED_HOSTS = [
 '*']
INSTALLED_APPS = ('django.contrib.admin', 'django.contrib.auth', 'django.contrib.contenttypes',
                  'django.contrib.sessions', 'django.contrib.messages', 'django.contrib.staticfiles',
                  'djmongoreader')
MIDDLEWARE_CLASSES = ('django.contrib.sessions.middleware.SessionMiddleware', 'django.middleware.common.CommonMiddleware',
                      'django.middleware.csrf.CsrfViewMiddleware', 'django.contrib.auth.middleware.AuthenticationMiddleware',
                      'django.contrib.messages.middleware.MessageMiddleware', 'django.middleware.clickjacking.XFrameOptionsMiddleware')
ROOT_URLCONF = 'sampleapp.urls'
WSGI_APPLICATION = 'sampleapp.wsgi.application'
DATABASES = {}
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATIC_URL = '/static/'
STATICFILES_STORAGE = 'whitenoise.django.GzipManifestStaticFilesStorage'
TEMPLATE_DIRS = (
 os.path.join(BASE_DIR, 'templates'),)
MONGO_READER_SETTINGS = {'conn_str': os.getenv('MONGOLAB_URI', 'mongodb://127.0.0.1:27017/db1'), 'perm_check_func': 'sampleapp.security.my_mongocall_perm_check'}