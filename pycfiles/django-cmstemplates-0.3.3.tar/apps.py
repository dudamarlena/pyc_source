# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/asyncee/git/django-cmstemplates/cmstemplates/apps.py
# Compiled at: 2016-02-24 04:35:30
from __future__ import print_function, unicode_literals
from django.apps import AppConfig

class DefaultConfig(AppConfig):
    name = b'cmstemplates'
    verbose_name = b'Шаблоны cmstemplates'

    def ready(self):
        from cmstemplates import signals