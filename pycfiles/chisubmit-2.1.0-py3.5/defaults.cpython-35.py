# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/chisubmit/backend/settings/defaults.py
# Compiled at: 2018-10-02 19:35:34
# Size of source mod 2**32: 1778 bytes
import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INSTALLED_APPS = ('django.contrib.admin', 'django.contrib.auth', 'django.contrib.contenttypes',
                  'django.contrib.sessions', 'django.contrib.messages', 'django.contrib.staticfiles',
                  'rest_framework', 'rest_framework.authtoken', 'chisubmit.backend.api')
MIDDLEWARE = [
 'django.middleware.security.SecurityMiddleware',
 'django.contrib.sessions.middleware.SessionMiddleware',
 'django.middleware.common.CommonMiddleware',
 'django.middleware.csrf.CsrfViewMiddleware',
 'django.contrib.auth.middleware.AuthenticationMiddleware',
 'django.contrib.messages.middleware.MessageMiddleware',
 'django.middleware.clickjacking.XFrameOptionsMiddleware']
ROOT_URLCONF = 'chisubmit.backend.urls'
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True
TEMPLATES = [
 {'BACKEND': 'django.template.backends.django.DjangoTemplates', 
  'DIRS': [], 
  'APP_DIRS': True, 
  'OPTIONS': {'context_processors': [
                                     'django.template.context_processors.debug',
                                     'django.template.context_processors.request',
                                     'django.contrib.auth.context_processors.auth',
                                     'django.contrib.messages.context_processors.messages']}}]
STATIC_URL = '/static/'
REST_FRAMEWORK = {'DEFAULT_AUTHENTICATION_CLASSES': ('rest_framework.authentication.TokenAuthentication', ), 
 
 'DEFAULT_PERMISSION_CLASSES': ('rest_framework.permissions.IsAuthenticated', )}