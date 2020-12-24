# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ramusus/workspace/manufacture/env/src/django-vkontakte-groups/vkontakte_groups/admin.py
# Compiled at: 2015-11-01 17:29:28
from django.contrib import admin
from vkontakte_api.admin import VkontakteModelAdmin
from models import Group

class GroupAdmin(VkontakteModelAdmin):

    def image_preview(self, obj):
        return '<a href="%s"><img src="%s" height="30" /></a>' % (obj.photo_big, obj.photo)

    image_preview.short_description = 'Картинка'
    image_preview.allow_tags = True
    search_fields = ('name', )
    list_display = ('image_preview', 'name', 'screen_name', 'type')
    list_display_links = ('name', 'screen_name')
    list_filter = ('type', 'is_closed', 'is_admin')
    exclude = ('members', )


admin.site.register(Group, GroupAdmin)