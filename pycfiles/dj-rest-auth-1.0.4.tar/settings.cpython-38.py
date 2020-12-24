# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/michael/Projects/dj-rest-auth/dj_rest_auth/tests/settings.py
# Compiled at: 2020-03-22 07:38:27
# Size of source mod 2**32: 2965 bytes
import logging, os, sys
PROJECT_ROOT = os.path.abspath(os.path.split(os.path.split(__file__)[0])[0])
logging.disable(logging.CRITICAL)
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
DATABASES = {'default': {'ENGINE':'django.db.backends.sqlite3', 
             'NAME':':memory:'}}
MIDDLEWARE = [
 'django.middleware.common.CommonMiddleware',
 'django.contrib.sessions.middleware.SessionMiddleware',
 'django.middleware.csrf.CsrfViewMiddleware',
 'django.contrib.auth.middleware.AuthenticationMiddleware',
 'django.contrib.messages.middleware.MessageMiddleware']
MIDDLEWARE_CLASSES = MIDDLEWARE
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
 {'BACKEND':'django.template.backends.django.DjangoTemplates', 
  'DIRS':[],  'APP_DIRS':True, 
  'OPTIONS':{'context_processors': TEMPLATE_CONTEXT_PROCESSORS}}]
REST_FRAMEWORK = {'DEFAULT_AUTHENTICATION_CLASSES': ('rest_framework.authentication.SessionAuthentication', 'dj_rest_auth.utils.JWTCookieAuthentication')}
INSTALLED_APPS = [
 'django.contrib.messages',
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
 'dj_rest_auth',
 'dj_rest_auth.registration']
SECRET_KEY = '38dh*skf8sjfhs287dh&^hd8&3hdg*j2&sd'
ACCOUNT_ACTIVATION_DAYS = 1
SITE_ID = 1
AUTHENTICATION_BACKENDS = ('django.contrib.auth.backends.ModelBackend', 'allauth.account.auth_backends.AuthenticationBackend')