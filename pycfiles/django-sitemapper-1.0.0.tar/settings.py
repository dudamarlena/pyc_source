# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/mhurt/Projects/django-sitemapper/docs/settings.py
# Compiled at: 2014-10-08 19:44:33
import os, sys
sys.path.insert(0, os.getcwd())
sys.path.insert(0, os.path.join(os.getcwd(), os.pardir))
SITE_ID = 303
DEBUG = True
TEMPLATE_DEBUG = DEBUG
DATABASES = {'default': {'NAME': ':memory:', 
               'ENGINE': 'django.db.backends.sqlite3', 
               'USER': '', 
               'PASSWORD': '', 
               'PORT': ''}}
SECRET_KEY = 'thisisnotasecret!'
INSTALLED_APPS = ('django.contrib.auth', 'django.contrib.contenttypes', 'django.contrib.sessions',
                  'django.contrib.sites', 'sitemapper')