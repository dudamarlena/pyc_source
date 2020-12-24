# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/nicolas/dev/feedpubsub/feedsubs/settings/dev.py
# Compiled at: 2018-12-13 14:13:37
# Size of source mod 2**32: 657 bytes
from .base import *
DEBUG = True
INSTALLED_APPS += [
 'debug_toolbar']
MIDDLEWARE = [
 'debug_toolbar.middleware.DebugToolbarMiddleware'] + MIDDLEWARE
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
INTERNAL_IPS = [
 '127.0.0.1']
ALLOWED_HOSTS = ['127.0.0.1']
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'
CACHES = {'default': {'BACKEND':'django.core.cache.backends.filebased.FileBasedCache', 
             'LOCATION':os.path.join(BASE_DIR, 'cache')}}