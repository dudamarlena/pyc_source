# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/scaler/settings.py
# Compiled at: 2012-05-30 06:57:07
import os
DEBUG = True
TEMPLATE_DEBUG = DEBUG
DATABASES = {'default': {'ENGINE': 'django.db.backends.sqlite3', 
               'NAME': 'scaler'}}
ROOT_URLCONF = 'scaler.urls'
INSTALLED_APPS = ('scaler', 'django.contrib.auth', 'django.contrib.admin', 'django.contrib.contenttypes')
MIDDLEWARE_CLASSES = ('scaler.middleware.ScalerMiddleware', 'django.contrib.sessions.middleware.SessionMiddleware',
                      'django.contrib.auth.middleware.AuthenticationMiddleware')
TEMPLATE_CONTEXT_PROCESSORS = ('django.core.context_processors.debug', 'django.core.context_processors.i18n',
                               'django.core.context_processors.request')
DJANGO_SCALER = {'server_busy_url_name': 'server-busy', 
   'trend_size': 10, 
   'slow_threshold': 2.0, 
   'redirect_for': 60, 
   'redirect_n_slowest_function': lambda : 0}