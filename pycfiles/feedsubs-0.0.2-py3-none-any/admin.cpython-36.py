# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/nicolas/dev/feedpubsub/um/admin.py
# Compiled at: 2018-08-29 16:52:52
# Size of source mod 2**32: 543 bytes
import pprint
from django.contrib import admin
from django.contrib.sessions.models import Session
from . import models

@admin.register(models.UMProfile)
class ProfileAdmin(admin.ModelAdmin):
    pass


@admin.register(Session)
class SessionAdmin(admin.ModelAdmin):

    def _session_data(self, obj):
        return pprint.pformat(obj.get_decoded())

    _session_data.allow_tags = True
    list_display = ['session_key', '_session_data', 'expire_date']
    readonly_fields = ['session_key', '_session_data']
    exclude = ['session_data']