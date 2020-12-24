# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/uranusjr/Documents/programming/python/django-sparkle-external/django-sparkle-external/sparkle/admin.py
# Compiled at: 2014-07-01 07:17:15
# Size of source mod 2**32: 1701 bytes
from django.contrib import admin
from .conf import SYSTEM_PROFILES_VISIBLE
from .models import Application, Channel, Version, SystemProfileReport, SystemProfileReportRecord
from .forms import VersionAdminForm

class ApplicationAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name', )}
    list_display = ('name', 'slug')
    list_display_links = list_display


class ChannelAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name', )}
    list_display = ('name', 'slug')
    list_display_links = list_display


class VersionAdmin(admin.ModelAdmin):
    form = VersionAdminForm
    list_display = ('title', 'version', 'short_version', 'application', 'publish_at')
    list_display_links = ('title', )
    list_filter = ('application', 'publish_at')
    filter_horizontal = ('channels', )
    readonly_fields = ('created_at', )


admin.site.register(Application, ApplicationAdmin)
admin.site.register(Channel, ChannelAdmin)
admin.site.register(Version, VersionAdmin)
if SYSTEM_PROFILES_VISIBLE:

    class SystemProfileReportRecordInline(admin.TabularInline):
        model = SystemProfileReportRecord
        extra = 0
        max_num = 0
        readonly_fields = ('key', 'value')
        can_delete = False


    class SystemProfileReportAdmin(admin.ModelAdmin):
        inlines = (
         SystemProfileReportRecordInline,)


    class SystemProfileReportRecordAdmin(admin.ModelAdmin):
        list_display = ('key', 'value')
        list_filter = ('key', )


    admin.site.register(SystemProfileReport, SystemProfileReportAdmin)
    admin.site.register(SystemProfileReportRecord, SystemProfileReportRecordAdmin)