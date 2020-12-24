# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/bas/dev/django-dmarc/dmarc/admin.py
# Compiled at: 2018-06-18 16:39:43
# Size of source mod 2**32: 961 bytes
"""
DMARC models for managing Aggregate Reports
http://dmarc.org/resources/specification/
"""
from django.contrib import admin
from dmarc.models import Report

class ReportAdmin(admin.ModelAdmin):
    __doc__ = 'Report display options'
    actions = []
    model = Report
    list_display = ['report_id', 'reporter', 'date_begin']
    list_filter = ['date_begin', 'reporter']
    readonly_fields = [
     'report_id', 'reporter',
     'date_begin', 'date_end', 'policy_domain',
     'policy_adkim', 'policy_aspf',
     'policy_p', 'policy_sp',
     'policy_pct',
     'report_xml']
    order = [
     '-id']

    def has_add_permission(self, request):
        return False


admin.site.register(Report, ReportAdmin)