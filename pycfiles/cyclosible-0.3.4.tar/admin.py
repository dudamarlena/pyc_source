# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/seraf/Cycloid/Cyclosible/cyclosible/appversion/admin.py
# Compiled at: 2015-12-22 05:07:25
from django.contrib import admin
from .models import AppVersion

class AppVersionAdmin(admin.ModelAdmin):
    list_display = ('playbook', 'application', 'version', 'env', 'deployed')


admin.site.register(AppVersion, AppVersionAdmin)