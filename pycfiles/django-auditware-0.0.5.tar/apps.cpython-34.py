# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/val/Projects/workon/mpro/sf3/apps/django-auditware/auditware/apps.py
# Compiled at: 2016-04-05 16:17:06
# Size of source mod 2**32: 484 bytes
from django.apps import apps
from django.apps import AppConfig as DjangoAppConfig
from django.utils.translation import ugettext_lazy as _

class AppConfig(DjangoAppConfig):
    __doc__ = '\n    Configuration entry point for the auditware app\n    '
    label = name = 'auditware'
    verbose_name = _('auditware app')

    def ready(self):
        """
        App is imported and ready, so bootstrap it.
        """
        from .receivers import latch_to_signals
        latch_to_signals()