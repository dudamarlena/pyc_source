# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ramusus/workspace/manufacture_old/env/src/django-facebook-pages-statistic/facebook_pages_statistic/admin.py
# Compiled at: 2015-03-06 07:16:08
from django.contrib import admin
from .models import PageStatistic

class PageStatisticAdmin(admin.ModelAdmin):
    search_fields = ('page', )
    list_display = ('page', 'likes_count', 'talking_about_count', 'updated_at')


admin.site.register(PageStatistic, PageStatisticAdmin)