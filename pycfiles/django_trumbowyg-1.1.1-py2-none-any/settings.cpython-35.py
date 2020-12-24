# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/est/src/django-trumbowyg/trumbowyg/settings.py
# Compiled at: 2017-04-26 00:18:45
# Size of source mod 2**32: 275 bytes
from django.conf import settings
UPLOAD_PATH = getattr(settings, 'TRUMBOWYG_UPLOAD_PATH', 'uploads/')
THUMBNAIL_SIZE = getattr(settings, 'TRUMBOWYG_THUMBNAIL_SIZE', None)
TRANSLITERATE_FILENAME = getattr(settings, 'TRUMBOWYG_TRANSLITERATE_FILENAME', False)