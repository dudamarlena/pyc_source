# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/hedley/django/instances/mote/mote/apps.py
# Compiled at: 2016-12-01 10:32:24
import os
from importlib import import_module
from django.apps import AppConfig
from django.conf import settings
from mote import PROJECT_PATHS

class MoteConfig(AppConfig):
    name = 'mote'
    verbose_name = 'Mote'

    def ready(self):
        for name in settings.INSTALLED_APPS:
            mod = import_module(name)
            if name == 'mote.tests':
                pth = os.path.join(os.path.dirname(mod.__file__), 'mote', 'projects')
            else:
                pth = os.path.join(os.path.dirname(mod.__file__), '..', 'mote', 'projects')
            if os.path.exists(pth):
                for id in os.listdir(pth):
                    if not id.startswith('.'):
                        PROJECT_PATHS[id] = pth