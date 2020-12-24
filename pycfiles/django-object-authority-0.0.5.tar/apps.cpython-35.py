# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/tomeu/workspace/wdna/django-object-authority/django_object_authority/apps.py
# Compiled at: 2017-06-09 03:36:21
# Size of source mod 2**32: 587 bytes
from django.apps import AppConfig
from django.db.models.signals import post_migrate
from django.utils.translation import ugettext_lazy as _
from .utils import create_update_permissions

class DjangoObjectAuthorityConfig(AppConfig):
    name = 'django_object_authority'
    verbose_name = _('Django object authority')

    def ready(self):
        """Register all available authorization from modules."""
        super().ready()
        self.module.autodiscover()
        post_migrate.connect(create_update_permissions, sender=self)