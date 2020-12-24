# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/wojciech/.pyenv/versions/3.7.3/lib/python3.7/site-packages/django_password_validators/settings.py
# Compiled at: 2016-03-01 03:32:05
# Size of source mod 2**32: 325 bytes
from django.conf import settings
from django.utils.module_loading import import_string

def get_password_hasher():
    history_hasher = getattr(settings, 'DPV_DEFAULT_HISTORY_HASHER', 'django_password_validators.password_history.hashers.HistoryHasher')
    return import_string(history_hasher)