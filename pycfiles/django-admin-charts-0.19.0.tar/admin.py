# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/petr/.local/share/virtualenvs/blenderhub_server-izvs0qj4/src/django-admin-charts/admin_tools_stats/admin.py
# Compiled at: 2020-04-02 04:48:24
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from admin_tools_stats.app_label_renamer import AppLabelRenamer
from admin_tools_stats.models import CriteriaToStatsM2M, DashboardStats, DashboardStatsCriteria
AppLabelRenamer(native_app_label='admin_tools_stats', app_label=_('Admin Tools Stats')).main()

class DashboardStatsCriteriaAdmin(admin.ModelAdmin):
    """
    Allows the administrator to view and modify certain attributes
    of a DashboardStats.
    """
    list_display = ('id', 'criteria_name', 'created_date')
    list_filter = ['created_date']
    search_fields = ('criteria_name', )
    ordering = ('id', )
    save_as = True


admin.site.register(DashboardStatsCriteria, DashboardStatsCriteriaAdmin)

class DashboardStatsCriteriaInline(admin.TabularInline):
    model = CriteriaToStatsM2M
    readonly_fields = ('criteria__dynamic_criteria_field_name', )
    fields = ('criteria', 'order', 'prefix', 'criteria__dynamic_criteria_field_name',
              'use_as')
    autocomplete_fields = ('criteria', )
    extra = 0

    def criteria__dynamic_criteria_field_name(self, obj):
        return obj.criteria.dynamic_criteria_field_name


class DashboardStatsAdmin(admin.ModelAdmin):
    """
    Allows the administrator to view and modify certain attributes
    of a DashboardStats.
    """
    list_display = ('id', 'graph_key', 'graph_title', 'model_name', 'distinct', 'type_operation_field_name',
                    'is_visible', 'created_date', 'date_field_name', 'operation_field_name',
                    'default_chart_type')
    list_filter = ['created_date']
    exclude = ('criteria', )
    inlines = [DashboardStatsCriteriaInline]
    ordering = ('id', )
    save_as = True


admin.site.register(DashboardStats, DashboardStatsAdmin)