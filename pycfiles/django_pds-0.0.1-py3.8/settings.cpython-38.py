# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/django_pds/middlewares/authentication/settings.py
# Compiled at: 2020-05-02 08:30:07
# Size of source mod 2**32: 314 bytes
from django.conf import settings

class Settings(object):

    @property
    def SESSION_MIDDLEWARE_EXEMPT_URLS(self):
        return getattr(settings, 'TOKEN_EXEMPT_URLS', [])

    @property
    def AUTH_NOT_REQUIRED_URLS(self):
        return getattr(settings, 'AUTH_NOT_REQUIRED_URLS', [])


conf = Settings()