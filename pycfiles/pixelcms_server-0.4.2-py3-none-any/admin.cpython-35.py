# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/mw/dev/pixelcms-server/cms/settings/admin.py
# Compiled at: 2016-08-19 10:04:16
# Size of source mod 2**32: 446 bytes
from django.contrib import admin
from .models import Settings

@admin.register(Settings)
class SettingsAdmin(admin.ModelAdmin):
    list_display = ('language', 'site_name', 'meta_description', 'meta_robots')
    fieldsets = [
     (
      None,
      {'fields': ('language', 'site_name', ('page_title_site_name_suffix', 'suffix_separator'), 'meta_description',
 'meta_robots')})]