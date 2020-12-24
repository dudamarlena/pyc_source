# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ryanh/src/pynsot/tests/nsot_settings.py
# Compiled at: 2019-10-24 21:45:41
"""
This configuration file is just Python code. You may override any global
defaults by specifying them here.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""
from __future__ import absolute_import
from nsot.conf.settings import *
import os.path, django
CONF_ROOT = os.path.dirname(__file__)
DEBUG = False
DATABASES = {'default': {'ENGINE': 'django.db.backends.sqlite3', 
               'NAME': os.path.join(CONF_ROOT, 'nsot.sqlite3'), 
               'USER': 'nsot', 
               'PASSWORD': '', 
               'HOST': '', 
               'PORT': ''}}
NSOT_HOST = 'localhost'
NSOT_PORT = 8990
NSOT_NUM_WORKERS = 4
NSOT_WORKER_TIMEOUT = 30
SERVE_STATIC_FILES = True
SECRET_KEY = 'fMK68NKgazLCjjTXjDtthhoRUS8IV4lwD-9G7iVd2Xs='
USER_AUTH_HEADER = 'X-NSoT-Email'
AUTH_TOKEN_EXPIRY = 600
ALLOWED_HOSTS = [
 '*']
django.setup()