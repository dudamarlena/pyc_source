# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/fanfei/Documents/Code/dj-sso-server/example/djssoserverapp/djssoserverapp/settings.py
# Compiled at: 2015-03-09 21:16:19
"""
Django settings for djssoserverapp project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""
import os, dj_database_url
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
SECRET_KEY = '51nq+jny--lu9(xt%9o+@-439vy79xr(!_%1a@8^kmsy5hckvs'
DEBUG = False if os.getenv('DATABASE_URL ', None) else True
TEMPLATE_DEBUG = True
ALLOWED_HOSTS = [
 '*']
INSTALLED_APPS = ('django.contrib.admin', 'django.contrib.auth', 'django.contrib.contenttypes',
                  'django.contrib.sessions', 'django.contrib.messages', 'django.contrib.staticfiles',
                  'djapiauth', 'djssoserver')
MIDDLEWARE_CLASSES = ('django.contrib.sessions.middleware.SessionMiddleware', 'django.middleware.common.CommonMiddleware',
                      'django.middleware.csrf.CsrfViewMiddleware', 'django.contrib.auth.middleware.AuthenticationMiddleware',
                      'django.contrib.messages.middleware.MessageMiddleware', 'django.middleware.clickjacking.XFrameOptionsMiddleware')
ROOT_URLCONF = 'djssoserverapp.urls'
WSGI_APPLICATION = 'djssoserverapp.wsgi.application'
DATABASES = {'default': {'ENGINE': 'django.db.backends.sqlite3', 
               'NAME': os.path.join(BASE_DIR, 'db.sqlite3')}}
if not DEBUG:
    DATABASES['default'] = dj_database_url.config()
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True
STATIC_URL = '/static/'
TEMPLATE_DIRS = (
 os.path.join(BASE_DIR, 'templates'),)
LOGIN_REDIRECT_URL = '/'
redistogo_url = os.getenv('REDISTOGO_URL', None)
REDIS_PWD = None
REDIS_HOST = '127.0.0.1:6379'
if redistogo_url:
    redis_url = redistogo_url
    redis_url = redis_url.split('redis://redistogo:')[1]
    redis_url = redis_url.split('/')[0]
    REDIS_PWD, REDIS_HOST = redis_url.split('@', 1)
CACHES = {'default': {'BACKEND': 'redis_cache.RedisCache', 
               'LOCATION': REDIS_HOST, 
               'OPTIONS': {'CONNECTION_POOL_CLASS': 'redis.BlockingConnectionPool', 
                           'CONNECTION_POOL_CLASS_KWARGS': {'PASSWORD': REDIS_PWD, 
                                                            'max_connections': 50, 
                                                            'timeout': 20}}}}