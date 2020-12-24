# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/val/Projects/.mpro-virenv/bizdir/lib/python3.4/site-packages/menuware/apps.py
# Compiled at: 2016-08-18 14:52:30
# Size of source mod 2**32: 186 bytes
from django.apps import AppConfig

class MenuAppConfig(AppConfig):
    name = 'menuware'
    label = 'menuware'
    verbose_name = 'Menu Application'

    def ready(self):
        pass