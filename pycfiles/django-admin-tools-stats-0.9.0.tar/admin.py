# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/areski/public_html/django/MyProjects/newfies-dialer/newfies/admin_tools_stats/admin.py
# Compiled at: 2015-12-13 06:29:13
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from admin_tools_stats.models import DashboardStatsCriteria, DashboardStats
from admin_tools_stats.app_label_renamer import AppLabelRenamer
AppLabelRenamer(native_app_label='admin_tools_stats', app_label=_('Admin Tools Stats')).main()

class DashboardStatsCriteriaAdmin(admin.ModelAdmin):
    """
    Allows the administrator to view and modify certain attributes
    of a DashboardStats.
    """
    list_display = ('id', 'criteria_name', 'created_date')
    list_filter = ['created_date']
    ordering = ('id', )


admin.site.register(DashboardStatsCriteria, DashboardStatsCriteriaAdmin)

class DashboardStatsAdmin(admin.ModelAdmin):
    """
    Allows the administrator to view and modify certain attributes
    of a DashboardStats.
    """
    list_display = ('id', 'graph_key', 'graph_title', 'model_name', 'is_visible', 'created_date')
    list_filter = ['created_date']
    ordering = ('id', )


admin.site.register(DashboardStats, DashboardStatsAdmin)