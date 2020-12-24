# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/travis/build/smn/heatherr/heatherr/apps.py
# Compiled at: 2016-01-28 05:47:10
import os.path
from importlib import import_module
from django.apps import AppConfig, apps

class HeatherrConfig(AppConfig):
    name = 'heatherr'

    def ready(self):
        for app in apps.get_app_configs():
            if os.path.isfile(os.path.join(app.path, 'commands.py')):
                import_module('%s.commands' % (app.module.__name__,))