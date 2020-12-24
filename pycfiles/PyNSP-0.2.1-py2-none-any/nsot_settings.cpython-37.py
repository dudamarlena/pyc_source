# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/ryanh/src/pynsot/tests/nsot_settings.py
# Compiled at: 2019-10-23 13:20:33
# Size of source mod 2**32: 2653 bytes
__doc__ = '\nThis configuration file is just Python code. You may override any global\ndefaults by specifying them here.\n\nFor more information on this file, see\nhttps://docs.djangoproject.com/en/1.8/topics/settings/\n\nFor the full list of settings and their values, see\nhttps://docs.djangoproject.com/en/1.8/ref/settings/\n'
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