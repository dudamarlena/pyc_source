# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ramusus/workspace/manufacture_old/env/src/django-odnoklassniki-groups/odnoklassniki_groups/admin.py
# Compiled at: 2015-03-06 07:16:49
from django.contrib import admin
from django.utils.translation import ugettext as _
from django import forms
from odnoklassniki_api.admin import OdnoklassnikiModelAdmin
from models import Group

class GroupAdmin(OdnoklassnikiModelAdmin):

    def image_preview(self, obj):
        return '<a href="%s"><img src="%s" height="30" /></a>' % (obj.pic640x480, obj.pic50x50)

    image_preview.short_description = 'Картинка'
    image_preview.allow_tags = True
    search_fields = ('name', )
    list_display = ('image_preview', 'name', 'shortname', 'ok_link', 'premium')
    list_display_links = ('name', 'shortname')
    list_filter = ('premium', 'private', 'shop_visible_admin', 'shop_visible_public')
    exclude = ('users', )


admin.site.register(Group, GroupAdmin)