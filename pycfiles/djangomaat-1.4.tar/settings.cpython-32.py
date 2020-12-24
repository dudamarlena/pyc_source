# uncompyle6 version 3.7.4
# Python bytecode 3.2 (3180)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/germanoguerrini/Developer/github/django-maat/djangomaat/settings.py
# Compiled at: 2015-02-03 06:22:37
from django.conf import settings
FLUSH_BATCH_SIZE = getattr(settings, 'MAAT_FLUSH_BATCH_SIZE', 1000)