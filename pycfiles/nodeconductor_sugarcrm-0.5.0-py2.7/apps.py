# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/nodeconductor_sugarcrm/apps.py
# Compiled at: 2016-09-28 11:51:43
from django.apps import AppConfig

class SugarCRMConfig(AppConfig):
    name = 'nodeconductor_sugarcrm'
    verbose_name = 'NodeConductor SugarCRM'
    service_name = 'SugarCRM'

    def ready(self):
        from nodeconductor.quotas.fields import LimitAggregatorQuotaField
        from nodeconductor.structure import SupportedServices
        from .backend import SugarCRMBackend
        SupportedServices.register_backend(SugarCRMBackend)
        from nodeconductor.structure.models import ServiceSettings
        from . import handlers, signals as sugarcrm_signals
        CRM = self.get_model('CRM')
        SugarCRMServiceProjectLink = self.get_model('SugarCRMServiceProjectLink')
        sugarcrm_signals.user_post_save.connect(handlers.log_user_post_save, sender=CRM, dispatch_uid='nodeconductor_sugarcrm.handlers.log_user_post_save')
        sugarcrm_signals.user_post_delete.connect(handlers.log_user_post_delete, sender=CRM, dispatch_uid='nodeconductor_sugarcrm.handlers.log_user_post_delete')
        ServiceSettings.add_quota_field(name='sugarcrm_user_count', quota_field=LimitAggregatorQuotaField(creation_condition=lambda service_settings: service_settings.type == SugarCRMConfig.service_name, get_children=lambda service_settings: SugarCRMServiceProjectLink.objects.filter(service__settings=service_settings), child_quota_name='user_limit_count'))