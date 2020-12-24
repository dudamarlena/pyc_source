# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\demo_site\admin.py
# Compiled at: 2018-10-03 09:43:19
# Size of source mod 2**32: 407 bytes
from django.contrib import admin
from .models import DemoSiteSettings, AccessToken

class DemoSiteSettingsAdmin(admin.ModelAdmin):
    __doc__ = '\n\n    '

    def has_add_permission(self, request, obj=None):
        return False


admin.site.register(DemoSiteSettings, DemoSiteSettingsAdmin)

class AccessTokenAdmin(admin.ModelAdmin):
    __doc__ = '\n\n    '


admin.site.register(AccessToken, AccessTokenAdmin)