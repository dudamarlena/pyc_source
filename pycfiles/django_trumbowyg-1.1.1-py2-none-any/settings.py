# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/est/src/django-trumbowyg/trumbowyg/settings.py
# Compiled at: 2017-03-11 05:37:45
from django.conf import settings
UPLOAD_PATH = getattr(settings, 'TRUMBOWYG_UPLOAD_PATH', 'uploads/')
THUMBNAIL_SIZE = getattr(settings, 'TRUMBOWYG_THUMBNAIL_SIZE', None)