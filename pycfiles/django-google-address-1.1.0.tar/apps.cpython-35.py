# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/arroyo/projects/cpmd/server/api/django-google-address/google_address/apps.py
# Compiled at: 2017-05-03 16:51:02
# Size of source mod 2**32: 154 bytes
from django.apps import AppConfig

class GoogleAddressConfig(AppConfig):
    name = 'google_address'

    def ready(self):
        import google_address.signals