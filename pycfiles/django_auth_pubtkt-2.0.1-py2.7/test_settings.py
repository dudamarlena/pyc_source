# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\tests\test_settings.py
# Compiled at: 2017-07-21 08:20:36
import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SECRET_KEY = 'fake-key'
INSTALLED_APPS = [
 'django.contrib.auth',
 'django.contrib.contenttypes',
 'django.contrib.sessions',
 'django.contrib.messages',
 'django.contrib.staticfiles',
 'django_auth_pubtkt',
 'tests']
ROOT_URLCONF = 'tests.urls'
TEMPLATES = [
 {'BACKEND': 'django.template.backends.django.DjangoTemplates', 
    'APP_DIRS': True, 
    'OPTIONS': {'context_processors': [
                                     'django.template.context_processors.debug',
                                     'django.template.context_processors.request',
                                     'django.contrib.auth.context_processors.auth',
                                     'django.contrib.messages.context_processors.messages']}}]
MIDDLEWARE = ('django.contrib.sessions.middleware.SessionMiddleware', 'django.middleware.common.CommonMiddleware',
              'django.middleware.csrf.CsrfViewMiddleware', 'django.contrib.auth.middleware.AuthenticationMiddleware',
              'django.contrib.auth.middleware.SessionAuthenticationMiddleware', 'django.contrib.messages.middleware.MessageMiddleware',
              'django.middleware.clickjacking.XFrameOptionsMiddleware', 'django.middleware.security.SecurityMiddleware',
              'django_auth_pubtkt.middleware.DjangoAuthPubtkt')
TKT_AUTH_PUBLIC_KEY = os.path.join(BASE_DIR, 'tests', 'dsakey', 'pubkey.pem')
TKT_AUTH_LOGIN_URL = '/login/'
DATABASES = {'default': {'ENGINE': 'django.db.backends.sqlite3', 
               'NAME': os.path.join(BASE_DIR, 'db.sqlite3')}}