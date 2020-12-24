# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/panjing/dev/simplepro_demo/simpleui/apps.py
# Compiled at: 2019-12-08 23:38:16
# Size of source mod 2**32: 603 bytes
from django.apps import AppConfig

class SimpleApp(AppConfig):
    name = 'simpleui'

    def ready(self):
        try:
            import django
            version = django.get_version()
            if int(version.split('.')[0]) >= 3:
                from django.conf import settings
                mname = 'simpleui.middlewares.SimpleMiddleware'
                if mname not in settings.MIDDLEWARE:
                    settings.MIDDLEWARE.append(mname)
        except Exception as e:
            try:
                pass
            finally:
                e = None
                del e