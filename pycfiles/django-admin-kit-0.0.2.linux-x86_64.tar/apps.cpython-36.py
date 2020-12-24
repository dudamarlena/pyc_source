# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/rohan/Django/django-admin-kit/.venv/lib/python3.6/site-packages/admin_kit/apps.py
# Compiled at: 2017-11-30 08:43:33
# Size of source mod 2**32: 303 bytes
"""
    Admin Kit apps module.
    This autodiscovers modules

"""
from django.apps import AppConfig

class AdminKitConfig(AppConfig):
    __doc__ = '\n    App Config that auto discovers ajax module\n    '
    name = 'admin_kit'

    def ready(self):
        super().ready()
        self.module.autodiscover()