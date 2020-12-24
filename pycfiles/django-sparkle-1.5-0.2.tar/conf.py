# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/spielmann/prog/bitchest/server/env/src/django-sparkle/sparkle/conf.py
# Compiled at: 2013-07-23 03:15:20
import os
from django.conf import settings
SPARKLE_PRIVATE_KEY_PATH = getattr(settings, 'SPARKLE_PRIVATE_KEY_PATH', None)
UPLOAD_PREFIX = getattr(settings, 'SPARKLE_UPLOAD_PREFIX', 'sparkle/')