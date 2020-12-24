# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/flanker/Developer/Github/PythonNest/pythonnest/defaults.py
# Compiled at: 2018-02-04 09:07:56
# Size of source mod 2**32: 814 bytes
from djangofloor.conf.callables import DefaultListenAddress
__author__ = 'Matthieu Gallet'
CACHES = {'default': {'BACKEND':'django.core.cache.backends.locmem.LocMemCache',  'LOCATION':'unique-snowflake'}}
WEBSOCKET_URL = None
DF_INDEX_VIEW = 'pythonnest.views.index'
DF_INSTALLED_APPS = ['pythonnest']
DF_URL_CONF = 'pythonnest.root_urls.urls'
READ_ONLY_MIRROR = True
USE_CELERY = False
FLOOR_INDEX = 'pythonnest.views.index'
LISTEN_ADDRESS = DefaultListenAddress(8130)
FLOOR_TEMPLATE_CONTEXT_PROCESSORS = ['pythonnest.context_processors.context_user']