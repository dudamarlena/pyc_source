# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/panjing/dev/simpleui_demo/simpleui/apps.py
# Compiled at: 2020-04-29 02:18:07
# Size of source mod 2**32: 644 bytes
from django.apps import AppConfig

class SimpleApp(AppConfig):
    name = 'simpleui'

    def ready(self):
        try:
            import django
            version = django.get_version()
            if int(version.split('.')[0]) >= 3:
                from django.conf import settings
                for index, item in enumerate(settings.MIDDLEWARE):
                    if item == 'django.middleware.clickjacking.XFrameOptionsMiddleware':
                        settings.MIDDLEWARE.pop(index)

        except Exception as e:
            try:
                pass
            finally:
                e = None
                del e