# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/metro_tiny/admin.py
# Compiled at: 2012-03-16 11:31:32
from django.contrib import admin
from django.utils.translation import ugettext as _
from metro_tiny.models import MetroLine, MetroStation

class MetroStationInline(admin.TabularInline):
    model = MetroStation


class MetroLineAdmin(admin.ModelAdmin):
    list_display = ('name', 'city')
    search_fields = ('name', 'city__name')
    raw_id_fields = ('city', )
    inlines = (MetroStationInline,)
    save_on_top = True


admin.site.register(MetroLine, MetroLineAdmin)

class MetroStationAdmin(admin.ModelAdmin):
    list_display = ('name', 'display_city', 'line')
    search_fields = ('name', 'line__city__name')
    raw_id_fields = ('line', )
    readonly_fields = ('display_city', )

    def display_city(self, obj):
        return obj.line.city

    display_city.admin_order_field = 'line__city'
    display_city.short_description = _('City')


admin.site.register(MetroStation, MetroStationAdmin)