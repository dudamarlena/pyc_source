# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/silly/dev/django-likes/likes/tests/settings/21.py
# Compiled at: 2018-12-18 06:15:07
# Size of source mod 2**32: 1798 bytes
import os
USE_TZ = True
TIME_ZONE = 'Africa/Johannesburg'
DATABASES = {'default': {'ENGINE':'django.db.backends.sqlite3', 
             'NAME':'skeleton.db', 
             'USER':'skeleton', 
             'PASSWORD':'skeleton', 
             'HOST':'', 
             'PORT':''}}
INSTALLED_APPS = ('likes.tests', 'likes', 'secretballot', 'django.contrib.auth', 'django.contrib.contenttypes',
                  'django.contrib.sessions')
ROOT_URLCONF = 'likes.urls'
MIDDLEWARE = ('django.middleware.common.CommonMiddleware', 'django.contrib.sessions.middleware.SessionMiddleware',
              'django.middleware.csrf.CsrfViewMiddleware', 'django.contrib.auth.middleware.AuthenticationMiddleware',
              'django.contrib.messages.middleware.MessageMiddleware', 'likes.middleware.SecretBallotUserIpUseragentMiddleware')
TEMPLATE_CONTEXT_PROCESSORS = ('django.contrib.auth.context_processors.auth', 'django.template.context_processors.debug',
                               'django.template.context_processors.i18n', 'django.template.context_processors.media',
                               'django.template.context_processors.static', 'django.template.context_processors.tz',
                               'django.template.context_processors.request', 'django.contrib.messages.context_processors.messages')
TEMPLATES = [
 {'BACKEND':'django.template.backends.django.DjangoTemplates', 
  'DIRS':[],  'APP_DIRS':True, 
  'OPTIONS':{'context_processors': TEMPLATE_CONTEXT_PROCESSORS}}]
STATIC_URL = '/static/'
SECRET_KEY = 'SECRET_KEY'
DEBUG = True