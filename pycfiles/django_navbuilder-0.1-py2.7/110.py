# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/navbuilder/tests/settings/110.py
# Compiled at: 2017-07-06 08:35:55
DEBUG = True
DATABASES = {'default': {'ENGINE': 'django.db.backends.sqlite3'}}
ROOT_URLCONF = 'navbuilder.tests.urls'
INSTALLED_APPS = [
 'test_without_migrations',
 'link',
 'navbuilder',
 'navbuilder.tests',
 'ultracache',
 'django.contrib.admin',
 'django.contrib.auth',
 'django.contrib.contenttypes',
 'django.contrib.sessions',
 'django.contrib.sites',
 'django.contrib.messages',
 'django.contrib.staticfiles']
MIDDLEWARE_CLASSES = [
 'django.middleware.security.SecurityMiddleware',
 'django.contrib.sessions.middleware.SessionMiddleware',
 'django.middleware.common.CommonMiddleware',
 'django.middleware.csrf.CsrfViewMiddleware',
 'django.contrib.auth.middleware.AuthenticationMiddleware',
 'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
 'django.contrib.messages.middleware.MessageMiddleware',
 'django.middleware.clickjacking.XFrameOptionsMiddleware']
TEMPLATES = [
 {'BACKEND': 'django.template.backends.django.DjangoTemplates', 
    'DIRS': [], 'APP_DIRS': True, 
    'OPTIONS': {'context_processors': [
                                     'django.template.context_processors.debug',
                                     'django.template.context_processors.request',
                                     'django.contrib.auth.context_processors.auth',
                                     'django.contrib.messages.context_processors.messages']}}]
SITE_ID = 1
STATIC_URL = '/static/'
SECRET_KEY = 'SECRET_KEY'