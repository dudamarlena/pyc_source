# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/val/Projects/.mpro-virenv/sf3/lib/python3.4/site-packages/pulseware/apps.py
# Compiled at: 2016-01-18 12:22:54
# Size of source mod 2**32: 576 bytes
from django.apps import apps
from django.db.models import signals
from django.apps import AppConfig as DjangoAppConfig
from django.utils.translation import ugettext_lazy as _

class AppConfig(DjangoAppConfig):
    __doc__ = '\n    Configuration entry point for the pulseware app\n    '
    label = name = 'pulseware'
    verbose_name = _('pulseware app')

    def ready(self):
        """
        Create one object
        """
        from . import receivers as rcvs
        signals.post_migrate.connect(rcvs.post_migrate_receiver, sender=apps.get_app_config(self.name))