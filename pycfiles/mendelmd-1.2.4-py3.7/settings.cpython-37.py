# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/mendelmd/settings.py
# Compiled at: 2019-07-26 11:01:46
# Size of source mod 2**32: 5585 bytes
"""
Django settings for mendelmd project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""
import sys, os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
SECRET_KEY = '*efl#$$!@93)8397wwf8hy387"&^%3&ad8h7d2w-yus5mzcx&@'
DEBUG = True
ALLOWED_HOSTS = [
 '*']
INSTALLED_APPS = [
 'django.contrib.admin',
 'django.contrib.auth',
 'django.contrib.contenttypes',
 'django.contrib.sessions',
 'django.contrib.messages',
 'django.contrib.staticfiles',
 'django.contrib.sites',
 'django.contrib.humanize',
 'allauth',
 'allauth.account',
 'allauth.socialaccount',
 'allauth.socialaccount.providers.google',
 'crispy_forms',
 'django_select2',
 'celery',
 'django_celery_results',
 'dashboard',
 'individuals',
 'variants',
 'diseases',
 'genes',
 'pagination',
 'cases',
 'filter_analysis',
 'pathway_analysis',
 'stats',
 'databases',
 'projects',
 'files',
 'samples',
 'upload',
 'settings',
 'tasks',
 'workers',
 'analyses',
 'formtools',
 'mapps',
 'django_gravatar']
MIDDLEWARE = [
 'django.middleware.security.SecurityMiddleware',
 'django.contrib.sessions.middleware.SessionMiddleware',
 'django.middleware.common.CommonMiddleware',
 'django.middleware.csrf.CsrfViewMiddleware',
 'django.contrib.auth.middleware.AuthenticationMiddleware',
 'django.contrib.messages.middleware.MessageMiddleware',
 'django.middleware.clickjacking.XFrameOptionsMiddleware']
ROOT_URLCONF = 'mendelmd.urls'
WSGI_APPLICATION = 'mendelmd.wsgi.application'
DATABASES = {'default': {'ENGINE':'django.db.backends.sqlite3', 
             'NAME':'mendelmd.db'}}
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = False
USE_L10N = False
USE_TZ = False
STATIC_URL = '/static/'
STATICFILES_DIRS = [
 os.path.join(BASE_DIR, 'static')]
TEMPLATES = [
 {'BACKEND':'django.template.backends.django.DjangoTemplates', 
  'DIRS':[
   os.path.join(BASE_DIR, 'templates')], 
  'APP_DIRS':True, 
  'OPTIONS':{'context_processors': [
                          'django.contrib.auth.context_processors.auth',
                          'django.template.context_processors.request',
                          'django.template.context_processors.debug',
                          'django.template.context_processors.i18n',
                          'django.template.context_processors.media',
                          'django.template.context_processors.static',
                          'django.template.context_processors.tz',
                          'django.contrib.messages.context_processors.messages']}}]
AUTHENTICATION_BACKENDS = [
 'django.contrib.auth.backends.ModelBackend',
 'allauth.account.auth_backends.AuthenticationBackend']
SITE_ID = 1
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
LOGIN_REDIRECT_URL = 'dashboard'
CRISPY_TEMPLATE_PACK = 'bootstrap3'
INTERNAL_IPS = [
 '127.0.0.1']
CELERY_RESULT_BACKEND = 'django-db'
CELERY_RESULT_BACKEND = 'django-cache'
CELERY_IMPORTS = ('analyses.tasks', 'tasks.tasks', 'workers.tasks', 'individuals.tasks')
CELERYBEAT_SCHEDULE = {'check_queue': {'task':'workers.tasks.check_queue', 
                 'schedule':30.0}}
ALLOWED_HOSTS = [
 'localhost', '127.0.0.1', '*']
try:
    from .local_settings import *
except ImportError:
    pass

FILE_UPLOAD_PERMISSIONS = 511
from datetime import timedelta
DATA_UPLOAD_MAX_NUMBER_FIELDS = 100000
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_AUTHENTICATION_METHOD = 'username_email'
ACCOUNT_SESSION_REMEMBER = True
SOCIALACCOUNT_AUTO_SIGNUP = True
SOCIALACCOUNT_QUERY_EMAIL = True