# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/hedley/django/instances/django-ultracache/ultracache/app.py
# Compiled at: 2018-09-10 07:18:29
# Size of source mod 2**32: 191 bytes
from django.apps import AppConfig

class UltracacheAppConfig(AppConfig):
    name = 'ultracache'
    verbose_name = 'Ultracache'

    def ready(self):
        from ultracache import signals