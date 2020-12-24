# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/chris/workspace/slothauth/slothauth/apps.py
# Compiled at: 2016-02-01 18:16:07
# Size of source mod 2**32: 145 bytes
from django.apps import AppConfig

class SlothAuthConfig(AppConfig):
    name = 'slothauth'

    def ready(self):
        from . import signals