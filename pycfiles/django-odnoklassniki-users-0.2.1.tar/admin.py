# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ramusus/workspace/manufacture_old/env/src/django-odnoklassniki-users/odnoklassniki_users/admin.py
# Compiled at: 2015-03-06 07:16:55
from django.contrib import admin
from django.utils.translation import ugettext as _
from odnoklassniki_api.admin import OdnoklassnikiModelAdmin
from models import User

class UserAdmin(OdnoklassnikiModelAdmin):

    def image_preview(self, obj):
        return '<a href="%s"><img src="%s" height="30" /></a>' % (obj.pic1024x768, obj.pic50x50)

    image_preview.short_description = 'Аватар'
    image_preview.allow_tags = True
    list_display = ('image_preview', 'name', 'ok_link', 'gender', 'birthday', 'city',
                    'country', 'has_email')
    list_display_links = ('name', )
    list_filter = ('gender', 'has_email')
    search_fields = ('first_name', 'last_name')


admin.site.register(User, UserAdmin)