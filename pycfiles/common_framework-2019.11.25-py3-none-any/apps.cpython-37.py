# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
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