# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/miltonln/Proyectos/django-menu-generator/menu_generator/apps.py
# Compiled at: 2018-01-31 09:25:36
# Size of source mod 2**32: 198 bytes
from django.apps import AppConfig

class MenuAppConfig(AppConfig):
    name = 'menu_generator'
    label = 'menu_generator'
    verbose_name = 'Menu Application'

    def ready(self):
        pass