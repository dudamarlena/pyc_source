# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/chschw/Workspace/django/lab/django-cms/site/statify/settings.py
# Compiled at: 2013-04-24 04:02:44
import os
from django.conf import settings
STATIFY_BUILD_SETTINGS = getattr(settings, 'STATIFY_BUILD_SETTINGS', '')
STATIFY_USE_CMS = getattr(settings, 'STATIFY_USE_CMS', False)
STATIFY_PROJECT_DIR = getattr(settings, 'STATIFY_PROJECT_DIR', os.path.join(os.path.dirname(os.path.abspath(__file__)), '../'))
STATIFY_UPLOAD_PATH = getattr(settings, 'STATIFY_UPLOAD_PATH', os.path.join('statify/releases/'))
STATIFY_EXCLUDED_MEDIA = getattr(settings, 'STATIFY_EXCLUDED_MEDIA', ['admin', 'statify', 'tmp', 'root'])
STATIFY_ROOT_STATIC = getattr(settings, 'STATIFY_ROOT_STATIC', os.path.join(settings.MEDIA_ROOT, 'root'))
STATIFY_ROOT_STATIC_URL = getattr(settings, 'STATIFY_ROOT_STATIC_URL', settings.STATIC_URL + 'root/')