# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /var/www/transmanager/transmanager/apps.py
# Compiled at: 2017-07-27 04:11:30
# Size of source mod 2**32: 1116 bytes
import uuid, sys
from .settings import TM_DISABLED
from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes.models import ContentType
from django.db.models.signals import pre_save
from hvad.models import BaseTranslationModel
from .signals import object_on_pre_save

class TransManagerConfig(AppConfig):
    name = 'transmanager'
    verbose_name = _('Gestor de traducciones')

    def ready(self):
        if 'test' in sys.argv:
            return
        if TM_DISABLED:
            return
        self.activate_pre_save_signal_for_models()

    @staticmethod
    def activate_pre_save_signal_for_models():
        try:
            for it in ContentType.objects.all():
                try:
                    if issubclass(it.model_class(), BaseTranslationModel):
                        pre_save.connect(object_on_pre_save, sender=it.model_class(), dispatch_uid=uuid.uuid4())
                except TypeError:
                    pass

        except Exception:
            pass