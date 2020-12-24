# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/germanoguerrini/Developer/github/django-maat/djangomaat/settings.py
# Compiled at: 2015-02-03 06:22:37
# Size of source mod 2**32: 102 bytes
from django.conf import settings
FLUSH_BATCH_SIZE = getattr(settings, 'MAAT_FLUSH_BATCH_SIZE', 1000)