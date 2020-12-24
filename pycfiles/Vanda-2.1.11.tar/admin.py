# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/lxsameer/src/vanda/vanda/apps/page/admin.py
# Compiled at: 2013-01-07 03:52:15
from django.contrib import admin
from models import Page

class PageAdmin(admin.ModelAdmin):
    """
    Admin interface class for paeg model
    """
    list_display = ('title', 'slug', 'user', 'date', 'site', 'language')
    search_fields = ('title', 'content')
    list_filter = ('user', )
    prepopulated_fields = {'slug': ('title', )}

    def save_model(self, request, obj, form, change):
        obj.user = request.user
        obj.save()


admin.site.register(Page, PageAdmin)