# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/yuji/Projects/Grove/grove_project/grove/../grove/website/redirects/admin.py
# Compiled at: 2012-05-30 14:25:51
from django.contrib import admin
from grove.website.redirects.models import Redirect, RedirectGroup

class RedirectAdmin(admin.ModelAdmin):
    list_display = ('group', 'match_path', 'match_type')
    list_display_links = list_display
    list_filter = ('group', )


admin.site.register(Redirect, RedirectAdmin)
admin.site.register(RedirectGroup)