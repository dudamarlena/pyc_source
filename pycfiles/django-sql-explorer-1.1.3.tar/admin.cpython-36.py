# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/muhammadelias/grove_core/django-sql-explorer/explorer/admin.py
# Compiled at: 2019-07-02 16:47:10
# Size of source mod 2**32: 377 bytes
from django.contrib import admin
from explorer.models import Query
from explorer.actions import generate_report_action

class QueryAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'created_by_user')
    list_filter = ('title', )
    raw_id_fields = ('created_by_user', )
    actions = [
     generate_report_action()]


admin.site.register(Query, QueryAdmin)