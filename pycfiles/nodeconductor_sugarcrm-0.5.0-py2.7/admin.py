# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/nodeconductor_sugarcrm/admin.py
# Compiled at: 2016-09-28 11:51:43
from django.contrib import admin, messages
from .backend import SugarCRMBackendError
from .models import SugarCRMServiceProjectLink, SugarCRMService, CRM
from nodeconductor.quotas.admin import QuotaInline
from nodeconductor.structure import admin as structure_admin

class CRMAdmin(structure_admin.PublishableResourceAdmin):
    actions = [
     'sync_quotas']
    inlines = [QuotaInline]

    def sync_quotas(self, request, queryset):
        successfully_synced = []
        for crm in queryset:
            if crm.state != CRM.States.ONLINE:
                message = 'Cannot sync quotas for CRM "%s" it is not ONLINE' % crm.name
                self.message_user(request, message, level=messages.WARNING)
                continue
            backend = crm.get_backend()
            try:
                backend.sync_user_quota()
            except SugarCRMBackendError as e:
                message = 'Cannot sync user quota for CRM "%s". Error: %s' % (crm.name, e)
                self.message_user(request, message, level=messages.ERROR)
                continue

            successfully_synced.append(crm)

        if successfully_synced:
            message = 'Quotas was successfully synced for CRMs: %s' % (', ').join([ crm.name for crm in successfully_synced ])
            self.message_user(request, message)

    sync_quotas.short_description = 'Sync quotas'


class SugarCRMServiceProjectLinkAdmin(structure_admin.ServiceProjectLinkAdmin):
    inlines = [
     QuotaInline]


admin.site.register(CRM, CRMAdmin)
admin.site.register(SugarCRMService, structure_admin.ServiceAdmin)
admin.site.register(SugarCRMServiceProjectLink, SugarCRMServiceProjectLinkAdmin)