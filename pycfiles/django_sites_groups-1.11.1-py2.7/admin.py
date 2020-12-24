# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/sites_groups/admin.py
# Compiled at: 2016-05-25 05:23:19
from django.contrib import admin
from sites_groups.models import SitesGroup

class SitesGroupAdmin(admin.ModelAdmin):
    list_display = ('title', '_sites')

    def _sites(self, obj):
        return (', ').join([ o.name for o in obj.sites.all() ])


admin.site.register(SitesGroup, SitesGroupAdmin)