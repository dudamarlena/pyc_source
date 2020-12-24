# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/marc/Git/common-framework/common/apps.py
# Compiled at: 2018-02-03 12:24:20
# Size of source mod 2**32: 500 bytes
from django.apps import AppConfig
import django.utils.translation as _

class CommonConfig(AppConfig):
    name = 'common'
    verbose_name = _('Common Framework')

    def ready(self):
        from django.db.models import CharField, TextField
        from common.fields import CustomUnaccent
        CharField.register_lookup(CustomUnaccent)
        TextField.register_lookup(CustomUnaccent)