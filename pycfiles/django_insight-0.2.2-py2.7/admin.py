# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insight/admin.py
# Compiled at: 2014-09-10 07:58:57
from django.contrib import admin
from django.contrib.sites.models import Site
from insight.models import Origin, OriginGroup, QuerystringParameter

class OriginAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'origin_group', 'url', 'number_of_registrations')

    def url(self, origin):
        url = '%s%s' % (Site.objects.get_current().domain,
         origin.get_absolute_url())
        return '<a href="//%s">%s</a>' % (url, url)

    url.allow_tags = True


class QuerystringParameterAdmin(admin.ModelAdmin):
    list_display = ('origin', 'identifier', 'value', 'number_of_registrations')


admin.site.register(Origin, OriginAdmin)
admin.site.register(QuerystringParameter, QuerystringParameterAdmin)
admin.site.register(OriginGroup)