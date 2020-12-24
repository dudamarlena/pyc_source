# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.8-intel/egg/rdflib_django/testsettings.py
# Compiled at: 2012-10-25 06:19:50
"""
Settings for testing the application.
"""
import os
DEBUG = True
DJANGO_RDFLIB_DEVELOP = True
DB_PATH = os.path.abspath(os.path.join(__file__, '..', '..', '..', 'rdflib_django.db'))
DATABASES = {'default': {'ENGINE': 'django.db.backends.sqlite3', 
               'NAME': DB_PATH, 
               'USER': '', 
               'PASSWORD': '', 
               'HOST': '', 
               'PORT': ''}}
SITE_ID = 1
STATIC_URL = '/static/'
INSTALLED_APPS = ('django.contrib.auth', 'django.contrib.contenttypes', 'django.contrib.sessions',
                  'django.contrib.sites', 'django.contrib.messages', 'django.contrib.staticfiles',
                  'django.contrib.admin', 'django.contrib.admindocs', 'rdflib_django')
ROOT_URLCONF = 'rdflib_django.urls'
LOGGING = {'version': 1, 
   'disable_existing_loggers': True, 
   'formatters': {'simple': {'format': '%(levelname)s %(message)s'}}, 
   'handlers': {'console': {'level': 'DEBUG', 
                            'class': 'logging.StreamHandler', 
                            'formatter': 'simple'}}, 
   'loggers': {'': {'handlers': [
                               'console'], 
                    'propagate': True, 
                    'level': 'INFO'}}}