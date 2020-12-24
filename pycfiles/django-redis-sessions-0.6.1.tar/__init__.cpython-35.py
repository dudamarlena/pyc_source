# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/martin/personal/django-redis-sessions/tests/__init__.py
# Compiled at: 2017-09-06 12:48:00
# Size of source mod 2**32: 101 bytes
from django.conf import settings
settings.configure(SESSION_ENGINE='redis_sessions.session')