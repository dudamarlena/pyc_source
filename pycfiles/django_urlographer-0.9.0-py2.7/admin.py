# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/urlographer/admin.py
# Compiled at: 2013-06-26 14:11:51
from django.contrib import admin
from urlographer.models import URLMap, ContentMap

class URLMapAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'status_code', 'content_map')
    raw_id_fields = ('redirect', 'content_map')
    readonly_fields = ('hexdigest', )
    search_fields = ('path', )


admin.site.register(URLMap, URLMapAdmin)
admin.site.register(ContentMap)