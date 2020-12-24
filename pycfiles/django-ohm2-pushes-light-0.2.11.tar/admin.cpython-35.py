# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/tonra/ohm2/clients/ohm2/ohm2-dev-light/backend/webapp/backend/apps/ohm2_pushes_light/gateways/onesignal/admin.py
# Compiled at: 2018-09-28 10:56:32
# Size of source mod 2**32: 449 bytes
from django.contrib import admin
from . import models as onesignal_models

@admin.register(onesignal_models.Device)
class Device(admin.ModelAdmin):
    exclude = ('identity', 'last_update', 'code')

    def save_model(self, request, obj, form, change):
        obj = form.instance
        if not change or len(obj.identity) == 0:
            obj.identity = h_utils.db_unique_random(type(obj))
        super(type(self), self).save_model(request, obj, form, change)