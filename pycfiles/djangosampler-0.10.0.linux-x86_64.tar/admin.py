# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/vagrant/envs/conversocial/lib/python2.7/site-packages/djangosampler/admin.py
# Compiled at: 2015-11-17 05:08:04
from django.contrib import admin
from .models import Query, Stack, Sample

class QueryAdmin(admin.ModelAdmin):
    list_display = ('hash', 'created_dt')
    list_filter = ('created_dt', 'query_type')
    readonly_fields = ('created_dt', )


class StackAdmin(admin.ModelAdmin):
    list_display = ('hash', 'created_dt')
    list_filter = ('created_dt', )
    readonly_fields = ('created_dt', )


class SampleAdmin(admin.ModelAdmin):
    list_display = ('created_dt', )
    list_filter = ('created_dt', )
    readonly_fields = ('created_dt', )


admin.site.register(Query, QueryAdmin)
admin.site.register(Stack, StackAdmin)
admin.site.register(Sample, SampleAdmin)