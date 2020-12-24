# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jamie/code/django-enforce-hostname/enforce_host/tests/settings.py
# Compiled at: 2017-11-24 11:32:21
# Size of source mod 2**32: 570 bytes
from django.conf import global_settings
DATABASES = {'default': {'ENGINE':'django.db.backends.sqlite3', 
             'NAME':':memory:'}}
ROOT_URLCONF = 'enforce_host.tests.urls'
SECRET_KEY = 'abcde12345'
ALLOWED_HOSTS = [
 'original.com', 'enforced.com', 'enforced2.com']
if hasattr(global_settings, 'MIDDLEWARE'):
    print('hi')
    MIDDLEWARE = [
     'enforce_host.EnforceHostMiddleware']
else:
    MIDDLEWARE_CLASSES = ['enforce_host.EnforceHostMiddleware']
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')