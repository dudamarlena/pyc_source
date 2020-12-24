# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/banner/tests/settings/111.py
# Compiled at: 2018-01-09 13:54:21
DEBUG = True
DATABASES = {'default': {'ENGINE': 'django.db.backends.postgresql_psycopg2', 
               'NAME': 'test', 
               'USER': 'postgres', 
               'PASSWORD': '', 
               'HOST': '', 
               'PORT': ''}}
INSTALLED_APPS = ('banner', 'banner.tests', 'django_comments', 'jmbo', 'layers', 'link',
                  'photologue', 'category', 'likes', 'secretballot', 'preferences',
                  'sites_groups', 'django.contrib.admin', 'django.contrib.auth',
                  'django.contrib.contenttypes', 'django.contrib.sites', 'sortedm2m')
ROOT_URLCONF = 'banner.tests.urls'
MIDDLEWARE_CLASSES = ('django.middleware.common.CommonMiddleware', 'django.contrib.sessions.middleware.SessionMiddleware',
                      'django.middleware.csrf.CsrfViewMiddleware', 'django.contrib.auth.middleware.AuthenticationMiddleware',
                      'django.contrib.messages.middleware.MessageMiddleware', 'likes.middleware.SecretBallotUserIpUseragentMiddleware')
TEMPLATE_CONTEXT_PROCESSORS = ('django.contrib.auth.context_processors.auth', 'django.template.context_processors.debug',
                               'django.template.context_processors.i18n', 'django.template.context_processors.media',
                               'django.template.context_processors.static', 'django.template.context_processors.tz',
                               'django.template.context_processors.request', 'django.contrib.messages.context_processors.messages')
TEMPLATES = [
 {'BACKEND': 'django.template.backends.django.DjangoTemplates', 
    'DIRS': [], 'APP_DIRS': True, 
    'OPTIONS': {'context_processors': TEMPLATE_CONTEXT_PROCESSORS}}]
USE_TZ = True
SITE_ID = 1
STATIC_URL = '/static/'
SECRET_KEY = 'SECRET_KEY'