# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/uranusjr/Documents/programming/python/django-sparkle-external/django-sparkle-external/sparkle/conf.py
# Compiled at: 2014-06-19 01:12:18
# Size of source mod 2**32: 126 bytes
from django.conf import settings
SYSTEM_PROFILES_VISIBLE = getattr(settings, 'SPARKLE_SYSTEM_PROFILES_VISIBLE', False)