# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-intel/egg/meringue/settings.py
# Compiled at: 2015-08-17 17:37:49
import os
from django.conf import settings
from django.utils import timezone
PORT = getattr(settings, 'MERINGUE_SITE_PORT', None)
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
path = lambda *args: os.path.join(BASE_DIR, *args).replace('\\', '/')
START_YEAR = getattr(settings, 'MERINGUE_START_YEAR', timezone.now().year)
THUMBNAIL_CROP_MOTHOD = getattr(settings, 'MERINGUE_THUMBNAIL_CROP_MOTHOD', [
 'center', 'center'])
THUMBNAIL_RESIZE_MOTHOD = getattr(settings, 'MERINGUE_THUMBNAIL_RESIZE_MOTHOD', 'inscribe')
THUMBNAIL_QUALITY = getattr(settings, 'MERINGUE_THUMBNAIL_QUALITY', 100)
THUMBNAIL_COLOR = getattr(settings, 'MERINGUE_THUMBNAIL_COLOR', (255, 255, 255, 0))
THUMBNAIL_DIR = getattr(settings, 'MERINGUE_THUMBNAIL_DIR', os.path.join(settings.MEDIA_ROOT, 'temp'))
THUMBNAIL_URL = getattr(settings, 'MERINGUE_THUMBNAIL_URL', settings.MEDIA_URL + 'temp/')
DEFAULT_PHONE_LOCALIZATION = getattr(settings, 'MERINGUE_DEFAULT_PHONE_LOCALIZATION', 'RU')
LOAD_MINI = getattr(settings, 'MERINGUE_LOAD_MINI', not settings.DEBUG)