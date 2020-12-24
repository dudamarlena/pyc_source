# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/shodh/Projects/django_ginger/ginger/apps.py
# Compiled at: 2015-11-11 23:19:32
# Size of source mod 2**32: 270 bytes
from django.apps import AppConfig
from ginger.template import prep

class GingerConfig(AppConfig):
    name = 'ginger'
    verbose_name = 'ginger'
    _GingerConfig__once = False

    def ready(self):
        if not self._GingerConfig__once:
            self._GingerConfig__once = True
        prep.setup()