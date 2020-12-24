# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/mikehearing/GIT/django-hats/django_hats/apps.py
# Compiled at: 2016-07-25 16:50:55
from django.apps import AppConfig
from django_hats.bootstrap import Bootstrapper

class DjangoHatsConfig(AppConfig):
    name = 'django_hats'

    def ready(self):
        Bootstrapper.load()