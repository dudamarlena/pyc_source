# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/val/Projects/workon/mpro/doozdev/backend/restful-backend/apps/geoware/apps.py
# Compiled at: 2017-01-27 09:53:00
# Size of source mod 2**32: 314 bytes
from django.apps import apps
from django.apps import AppConfig as DjangoAppConfig
from django.utils.translation import ugettext_lazy as _

class AppConfig(DjangoAppConfig):
    __doc__ = '\n    Configuration entry point for the geoware app.\n    '
    label = name = 'geoware'
    verbose_name = _('GEOWARE.APPLICATION')