# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\yuuta\YCU-Programing\Code_Review\ura_1\django_press\apps.py
# Compiled at: 2020-02-11 06:35:03
# Size of source mod 2**32: 471 bytes
from django.apps import AppConfig
from django.db.models.signals import post_migrate

class DjangoPressConfig(AppConfig):
    name = 'django_press'

    def ready(self):
        from django_press.models.initialize import create_initial_context, create_initial_pages, create_super_user
        post_migrate.connect(create_initial_context, self)