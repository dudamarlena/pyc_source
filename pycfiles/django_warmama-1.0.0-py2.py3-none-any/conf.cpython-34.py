# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/alex/mgxrace/django-warmama/warmama/conf.py
# Compiled at: 2015-05-15 21:59:50
# Size of source mod 2**32: 822 bytes
from django.conf import settings as user_settings
__all__ = ['settings']
DEFAULTS = {'WARMAMA_TICKET_EXPIRATION': 60, 
 'WARMAMA_REMOTE_CLIENTAUTH': False, 
 'WARMAMA_AUTH_URL': 'http://remote.auth.server/getauth', 
 'WARMAMA_DEFAULT_SERVER_PORT': 44400}

class Settings(object):
    __doc__ = 'Settings object to map settings to properties'

    def __getattr__(self, attr):
        if attr not in DEFAULTS:
            raise AttributeError('Invalid setting %s' % attr)
        try:
            return getattr(user_settings, attr)
        except AttributeError:
            return DEFAULTS[attr]


settings = Settings()