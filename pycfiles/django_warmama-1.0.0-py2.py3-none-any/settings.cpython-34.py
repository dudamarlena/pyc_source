# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/alex/mgxrace/django-warmama/warmama/settings.py
# Compiled at: 2015-05-15 13:49:19
# Size of source mod 2**32: 727 bytes
from django.conf import settings
__all__ = ['settings']
USER_SETTINGS = getattr(settings, 'WARMAMA', {})
DEFAULTS = {'TICKET_EXPIRATION': 60, 
 'REMOTE_CLIENTAUTH': False, 
 'AUTH_URL': 'http://localhost:6000/getauth'}

class Settings(object):
    __doc__ = 'Settings object to map settings to properties'

    def __getattr__(self, attr):
        if attr not in DEFAULTS:
            raise AttributeError('Invalid setting %s' % attr)
        try:
            return USER_SETTINGS[attr]
        except KeyError:
            return DEFAULTS[attr]


settings = Settings()