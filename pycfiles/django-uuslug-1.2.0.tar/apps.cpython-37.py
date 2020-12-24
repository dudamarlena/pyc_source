# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/val/Projects/workon/mpro/uuslug/django-uuslug/uuslug/apps.py
# Compiled at: 2019-12-08 17:06:25
# Size of source mod 2**32: 302 bytes
import django.apps as apps
import django.apps as DjangoAppConfig
import django.utils.translation as _

class AppConfig(DjangoAppConfig):
    __doc__ = '\n    Configuration entry point for the uuslug app\n    '
    label = name = 'uuslug'
    verbose_name = _('uuslug app')