# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/gthomas/dev/management-server/managementserver/django_sql_dashboards/admin.py
# Compiled at: 2014-02-16 11:51:21
from django.contrib import admin
from models import DbConfig, Query, Dashboard

class DbConfigAdmin(admin.ModelAdmin):
    list_display = [
     'name', 'user', 'host', 'db']
    list_filter = ['host']
    search_fields = ['name']


admin.site.register(DbConfig, DbConfigAdmin)

class QueryAdmin(admin.ModelAdmin):
    pass


admin.site.register(Query, QueryAdmin)

class DashboardAdmin(admin.ModelAdmin):
    exclude = [
     'creator']
    list_display = ['title', 'creator']

    def save_model(self, request, obj, form, change):
        obj.creator = request.user
        obj.save()


admin.site.register(Dashboard, DashboardAdmin)