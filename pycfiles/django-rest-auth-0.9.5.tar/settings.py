# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: rest_auth/tests/settings.py
# Compiled at: 2017-08-29 01:32:18
import os, sys
PROJECT_ROOT = os.path.abspath(os.path.split(os.path.split(__file__)[0])[0])
ROOT_URLCONF = 'urls'
STATIC_URL = '/static/'
STATIC_ROOT = '%s/staticserve' % PROJECT_ROOT
STATICFILES_DIRS = (
 (
  'global', '%s/static' % PROJECT_ROOT),)
UPLOADS_DIR_NAME = 'uploads'
MEDIA_URL = '/%s/' % UPLOADS_DIR_NAME
MEDIA_ROOT = os.path.join(PROJECT_ROOT, '%s' % UPLOADS_DIR_NAME)
IS_DEV = False
IS_STAGING = False
IS_PROD = False
IS_TEST = 'test' in sys.argv or 'test_coverage' in sys.argv
DATABASES = {'default': {'ENGINE': 'django.db.backends.sqlite3', 
               'NAME': ':memory:'}}
MIDDLEWARE_CLASSES = [
 'django.middleware.common.CommonMiddleware',
 'django.contrib.sessions.middleware.SessionMiddleware',
 'django.middleware.csrf.CsrfViewMiddleware',
 'django.contrib.auth.middleware.AuthenticationMiddleware',
 'django.contrib.messages.middleware.MessageMiddleware']
TEMPLATE_CONTEXT_PROCESSORS = [
 'django.contrib.auth.context_processors.auth',
 'django.core.context_processors.debug',
 'django.core.context_processors.media',
 'django.core.context_processors.request',
 'django.contrib.messages.context_processors.messages',
 'django.core.context_processors.static',
 'allauth.account.context_processors.account',
 'allauth.socialaccount.context_processors.socialaccount']
TEMPLATES = [
 {'BACKEND': 'django.template.backends.django.DjangoTemplates', 
    'DIRS': [], 'APP_DIRS': True, 
    'OPTIONS': {'context_processors': TEMPLATE_CONTEXT_PROCESSORS}}]
REST_FRAMEWORK = {'DEFAULT_AUTHENTICATION_CLASSES': ('rest_framework.authentication.SessionAuthentication', 'rest_framework_jwt.authentication.JSONWebTokenAuthentication')}
INSTALLED_APPS = [
 'django.contrib.admin',
 'django.contrib.auth',
 'django.contrib.humanize',
 'django.contrib.contenttypes',
 'django.contrib.sessions',
 'django.contrib.sites',
 'django.contrib.sitemaps',
 'django.contrib.staticfiles',
 'allauth',
 'allauth.account',
 'allauth.socialaccount',
 'allauth.socialaccount.providers.facebook',
 'allauth.socialaccount.providers.twitter',
 'rest_framework',
 'rest_framework.authtoken',
 'rest_auth',
 'rest_auth.registration',
 'rest_framework_jwt']
SECRET_KEY = '38dh*skf8sjfhs287dh&^hd8&3hdg*j2&sd'
ACCOUNT_ACTIVATION_DAYS = 1
SITE_ID = 1
AUTHENTICATION_BACKENDS = ('django.contrib.auth.backends.ModelBackend', 'allauth.account.auth_backends.AuthenticationBackend')