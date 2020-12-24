# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ryanh/src/pynsot/tests/nsot_settings.py
# Compiled at: 2019-10-23 13:20:33
# Size of source mod 2**32: 2653 bytes
"""
This configuration file is just Python code. You may override any global
defaults by specifying them here.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""
SECRET_KEY = 'fMK68NKgazLCjjTXjDtthhoRUS8IV4lwD-9G7iVd2Xs='
from nsot.conf.settings import *
import os.path
CONF_ROOT = os.path.dirname(__file__)
DEBUG = False
DATABASES = {'default': {'ENGINE':'django.db.backends.sqlite3', 
             'NAME':os.path.join(CONF_ROOT, 'nsot.sqlite3'), 
             'USER':'nsot', 
             'PASSWORD':'', 
             'HOST':'', 
             'PORT':''}}
NSOT_HOST = 'localhost'
NSOT_PORT = 8990
NSOT_NUM_WORKERS = 4
NSOT_WORKER_TIMEOUT = 30
SERVE_STATIC_FILES = True
USER_AUTH_HEADER = 'X-NSoT-Email'
AUTH_TOKEN_EXPIRY = 600
ALLOWED_HOSTS = [
 '*']