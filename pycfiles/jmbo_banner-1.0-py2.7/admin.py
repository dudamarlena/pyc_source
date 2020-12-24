# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/banner/admin.py
# Compiled at: 2018-01-09 13:54:21
from django.contrib import admin
from jmbo.admin import ImageInline, ModelBaseAdmin
from banner.models import Banner, Button

class ButtonAdminInline(admin.TabularInline):
    model = Banner.buttons.through
    verbose_name = 'Button'
    verbose_name_plural = 'Buttons'


class BannerAdmin(ModelBaseAdmin):
    inlines = [
     ImageInline, ButtonAdminInline]


admin.site.register(Banner, BannerAdmin)
admin.site.register(Button)