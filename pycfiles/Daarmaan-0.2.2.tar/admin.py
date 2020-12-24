# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/lxsameer/src/daarmaan/daarmaan/server/admin.py
# Compiled at: 2012-09-03 13:37:08
from django.contrib import admin
from models import Service, Profile

class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'key', 'active', 'user')
    list_editable = ('active', )


class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', )


admin.site.register(Service, ServiceAdmin)
admin.site.register(Profile, ProfileAdmin)