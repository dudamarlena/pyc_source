# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /hdd/dev/os/django-do/.env/lib/python3.6/site-packages/django_redo/settings.py
# Compiled at: 2018-10-05 04:07:46
# Size of source mod 2**32: 330 bytes
from django.conf import settings

class Settings(object):
    __doc__ = '\n    Module settings helper.\n    '
    prefix = 'REDO_'

    @staticmethod
    def get(key, default=None):
        key = '{}{}'.format(Settings.prefix, key)
        if not hasattr(settings, key):
            return default
        else:
            return getattr(settings, key)