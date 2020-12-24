# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/nodeconductor_paas_oracle/admin.py
# Compiled at: 2016-12-16 07:39:01
from django.contrib import admin
from nodeconductor.structure import admin as structure_admin
from .models import OracleService, OracleServiceProjectLink, Flavor, Deployment

class FlavorAdmin(admin.ModelAdmin):
    list_display = ('name', 'cores', 'ram', 'disk')


admin.site.register(Flavor, FlavorAdmin)
admin.site.register(Deployment, structure_admin.ResourceAdmin)
admin.site.register(OracleService, structure_admin.ServiceAdmin)
admin.site.register(OracleServiceProjectLink, structure_admin.ServiceProjectLinkAdmin)