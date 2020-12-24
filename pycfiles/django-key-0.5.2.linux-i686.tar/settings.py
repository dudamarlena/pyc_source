# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python2.7/site-packages/key/settings.py
# Compiled at: 2011-09-06 11:45:35
from django.conf import settings
DATABASES = {'default': {'ENGINE': 'django.db.backends.sqlite3', 
               'NAME': 'my_db'}}
INSTALLED_APPS = [
 'key', 'django.contrib.auth', 'django.contrib.contenttypes', 'django.contrib.sessions', 'django.contrib.admin']
ROOT_URLCONF = 'key.urls'
MAX_KEYS = getattr(settings, 'APIKEY_MAX_KEYS', -1)
KEY_SIZE = getattr(settings, 'APIKEY_KEY_SIZE', 32)
USE_API_GROUP = getattr(settings, 'APIKEY_USE_API_GROUP', False)
AUTH_HEADER = getattr(settings, 'APIKEY_AUTHORIZATION_HEADER', 'X-Api-Authorization')

def reload():
    global AUTH_HEADER
    global KEY_SIZE
    global MAX_KEYS
    global USE_API_GROUP
    MAX_KEYS = getattr(settings, 'APIKEY_MAX_KEYS', -1)
    KEY_SIZE = getattr(settings, 'APIKEY_KEY_SIZE', 32)
    USE_API_GROUP = getattr(settings, 'APIKEY_USE_API_GROUP', False)
    AUTH_HEADER = getattr(settings, 'APIKEY_AUTHORIZATION_HEADER', 'X-Api-Authorization')